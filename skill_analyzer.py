# skill_analyzer.py
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class SkillGapAnalyzer:
    def __init__(self):
        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Enhanced skill database - we'll start with this and expand later
        self.skill_database = {
            "programming": {"python", "java", "javascript", "c++", "c#", "ruby", "go", "rust", "swift", "kotlin"},
            "web_frameworks": {"django", "flask", "react", "angular", "vue", "spring", "express", "laravel"},
            "data_science": {"machine learning", "data analysis", "statistics", "pandas", "numpy", "tensorflow", "pytorch"},
            "databases": {"sql", "mysql", "postgresql", "mongodb", "redis", "oracle"},
            "cloud": {"aws", "azure", "google cloud", "docker", "kubernetes", "ci/cd"},
            "tools": {"git", "jenkins", "linux", "bash", "rest api", "graphql"},
            "soft_skills": {"communication", "leadership", "problem solving", "teamwork", "agile", "scrum"}
        }
        
        # Flatten all skills for easy lookup
        self.all_skills = set()
        for category in self.skill_database.values():
            self.all_skills.update(category)
    
    def extract_skills(self, text):
        """Extract skills from text using hybrid approach"""
        text = text.lower()
        found_skills = set()
        
        # Method 1: Direct matching with skill database
        for skill in self.all_skills:
            if skill in text:
                found_skills.add(skill)
        
        # Method 2: spaCy noun phrase extraction for potential skills
        doc = self.nlp(text)
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.lower().strip()
            # Look for multi-word skills or technical terms
            if len(chunk_text.split()) >= 2 and any(word in chunk_text for word in 
                                                   ['development', 'analysis', 'management', 'programming', 'framework']):
                found_skills.add(chunk_text)
        
        return list(found_skills)
    
    def analyze_gap(self, job_description, resume_text):
        """Main analysis function - compares JD vs Resume"""
        print("🔍 Extracting skills from Job Description...")
        jd_skills = self.extract_skills(job_description)
        print(f"   Found {len(jd_skills)} skills: {jd_skills}")
        
        print("🔍 Extracting skills from Resume...")
        resume_skills = self.extract_skills(resume_text)
        print(f"   Found {len(resume_skills)} skills: {resume_skills}")
        
        # Calculate match score using TF-IDF and Cosine Similarity
        if jd_skills or resume_skills:
            # Combine all skills for vectorizer
            all_documents = [
                " ".join(jd_skills),
                " ".join(resume_skills)
            ]
            
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer()
            try:
                tfidf_matrix = vectorizer.fit_transform(all_documents)
                
                # Calculate cosine similarity
                cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
                match_score = round(cosine_sim[0][0] * 100, 2)
            except:
                # Fallback if vectorization fails (empty documents)
                match_score = 0
        else:
            match_score = 0
        
        # Find gaps
        missing_skills = set(jd_skills) - set(resume_skills)
        matching_skills = set(jd_skills) & set(resume_skills)
        
        # Categorize missing skills
        categorized_gaps = {}
        for skill in missing_skills:
            for category, skills in self.skill_database.items():
                if skill in skills:
                    if category not in categorized_gaps:
                        categorized_gaps[category] = []
                    categorized_gaps[category].append(skill)
                    break
            else:
                if "other" not in categorized_gaps:
                    categorized_gaps["other"] = []
                categorized_gaps["other"].append(skill)
        
        return {
            "match_score": match_score,
            "jd_skills": jd_skills,
            "resume_skills": resume_skills,
            "matching_skills": list(matching_skills),
            "missing_skills": list(missing_skills),
            "categorized_gaps": categorized_gaps,
            "match_interpretation": self.interpret_match_score(match_score)
        }
    
    def interpret_match_score(self, score):
        """Provide interpretation of the match score"""
        if score >= 80:
            return "Excellent match! You're well-qualified for this position."
        elif score >= 60:
            return "Good match. You have most required skills."
        elif score >= 40:
            return "Moderate match. Consider developing some key missing skills."
        else:
            return "Low match. Significant skill development needed."



# # Test function
# def test_analyzer():
#     print("🧪 Testing Skill Gap Analyzer...")
    
#     analyzer = SkillGapAnalyzer()
    
    # # Sample test data
    # sample_jd = """
    # We are looking for a Python developer with strong experience in web development using Django or Flask.
    # Required skills: Python, Django, REST APIs, SQL, Git.
    # Nice to have: JavaScript, React, AWS, Docker.
    # """
    
    # sample_resume = """
    # Experienced software developer with 3 years in Python programming.
    # Proficient in Flask framework and REST API development.
    # Strong knowledge of Git version control and basic SQL.
    # Some experience with JavaScript and web development.
    # """
    
#     results = analyzer.analyze_gap(sample_jd, sample_resume)
    
#     print("\n" + "="*50)
#     print("📊 ANALYSIS RESULTS")
#     print("="*50)
#     print(f"Overall Match Score: {results['match_score']}%")
#     print(f"Interpretation: {results['match_interpretation']}")
#     print(f"\n✅ Matching Skills: {results['matching_skills']}")
#     print(f"❌ Missing Skills: {results['missing_skills']}")
    
#     print("\n📁 Categorized Skill Gaps:")
#     for category, skills in results['categorized_gaps'].items():
#         print(f"   {category.title()}: {skills}")

# if __name__ == "__main__":
#     test_analyzer()