# skill_analyzer.py - COMPLETE WORKING VERSION
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
import json
from job_market import job_market

class SkillGapAnalyzer:
    def __init__(self):
        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Enhanced skill database
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
    
    def get_gap_bridge(self, skill_name):
        """Get gap bridge data for a skill from SQLite database"""
        try:
            conn = sqlite3.connect('skill_analyzer.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT skill_name, free_resources, project_ideas, time_to_beginner FROM skill_recommendations WHERE skill_name = ?", 
                (skill_name,)
            )
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                # Parse JSON data
                free_resources = json.loads(row['free_resources']) if row['free_resources'] else []
                project_ideas = json.loads(row['project_ideas']) if row['project_ideas'] else []
                
                return {
                    'skill': row['skill_name'],
                    'resources': free_resources[:3],  # Top 3 resources
                    'projects': project_ideas[:2],     # Top 2 projects
                    'time_required': row['time_to_beginner'],
                    'weeks_needed': round(row['time_to_beginner'] / 5, 1)
                }
        except Exception as e:
            print(f"Note: Error getting gap bridge for {skill_name}: {e}")
            # If skill not in database, return basic plan
        
        # Fallback plan if skill not found
        return {
            'skill': skill_name,
            'resources': [
                {'name': f'Learn {skill_name} - Documentation', 'url': f'https://www.google.com/search?q=learn+{skill_name}'},
                {'name': f'{skill_name} Tutorial', 'url': f'https://www.youtube.com/results?search_query={skill_name}+tutorial'}
            ],
            'projects': [
                {'title': f'Basic {skill_name} Project', 'description': f'Create a simple project using {skill_name}'},
                {'title': f'Advanced {skill_name} Application', 'description': f'Build a complete application with {skill_name}'}
            ],
            'time_required': 30,
            'weeks_needed': 6
        }
    
    def analyze_gap(self, job_description, resume_text):
        """Main analysis function - compares JD vs Resume"""
        # Extract skills
        jd_skills = self.extract_skills(job_description)
        resume_skills = self.extract_skills(resume_text)
        
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
        
        # NEW: Generate gap bridge plans
        gap_bridge_plans = []
        for skill in missing_skills:
            plan = self.get_gap_bridge(skill)
            gap_bridge_plans.append(plan)
        
        # Calculate summary
        if gap_bridge_plans:
            total_hours = sum(p['time_required'] for p in gap_bridge_plans)
            total_weeks = sum(p['weeks_needed'] for p in gap_bridge_plans)
            gap_summary = {
                'total_skills': len(gap_bridge_plans),
                'total_hours': total_hours,
                'total_weeks': round(total_weeks, 1),
                'weekly_commitment': 5
            }
        else:
            gap_summary = None
        
        return {
            "match_score": match_score,
            "jd_skills": jd_skills,
            "resume_skills": resume_skills,
            "matching_skills": list(matching_skills),
            "missing_skills": list(missing_skills),
            "categorized_gaps": categorized_gaps,
            "gap_bridge_plans": gap_bridge_plans,
            "gap_summary": gap_summary,
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
    
    # Add at the top of skill_analyzer.py
from job_market import job_market

# Then in the SkillGapAnalyzer class, add this method:
def analyze_with_market_pulse(self, job_description, resume_text, location="Worldwide"):
    """Analyze skills with job market insights"""
    # Get basic analysis
    basic_analysis = self.analyze_gap(job_description, resume_text)
    
    # Get job market data for all skills found
    all_skills = list(set(basic_analysis['jd_skills'] + basic_analysis['resume_skills']))
    
    if all_skills:
        market_data = job_market.get_multiple_skills_demand(all_skills, location)
        
        # Add market data to results
        basic_analysis['job_market_pulse'] = {
            'demand_data': market_data,
            'salary_estimates': {},
            'trending_skills': job_market.get_trending_skills(),
            'market_insights': self.generate_market_insights(basic_analysis, market_data)
        }
        
        # Add salary estimates for matching skills
        for skill in basic_analysis['matching_skills']:
            basic_analysis['job_market_pulse']['salary_estimates'][skill] = \
                job_market.get_salary_estimate(skill, experience_years=3, location=location)
    
    return basic_analysis

def generate_market_insights(self, analysis, market_data):
    """Generate market insights from analysis"""
    insights = []
    
    # Insight 1: High demand missing skills
    for skill in analysis['missing_skills']:
        if skill in market_data['skills']:
            skill_data = market_data['skills'][skill]
            if skill_data['hotness_score'] > 70:
                insights.append({
                    'type': 'high_demand_gap',
                    'skill': skill,
                    'message': f"🔥 {skill} is in HIGH demand ({skill_data['job_count']:,} jobs) - prioritize learning this!",
                    'priority': 'high'
                })
    
    # Insight 2: User's valuable skills
    for skill in analysis['matching_skills']:
        if skill in market_data['skills']:
            skill_data = market_data['skills'][skill]
            if skill_data['hotness_score'] > 80:
                insights.append({
                    'type': 'valuable_skill',
                    'skill': skill,
                    'message': f"💎 You have {skill} which is highly valuable (${skill_data['avg_salary_max']:,}+ potential)",
                    'priority': 'info'
                })
    
    # Insight 3: Market trends
    if market_data.get('trending_skills'):
        top_trend = market_data['trending_skills'][0]
        insights.append({
            'type': 'market_trend',
            'skill': top_trend['skill'],
            'message': f"📈 {top_trend['skill']} is trending ({top_trend['growth_rate']}% growth)",
            'priority': 'medium'
        })
    
    return insights

# ====== IMPORTANT: Create global analyzer instance ======
# This line creates the 'analyzer' variable that app.py imports
analyzer = SkillGapAnalyzer()

# Test function (optional - only runs if you run this file directly)
def test_analyzer():
    print("🧪 Testing Skill Gap Analyzer with Gap Bridge...")
    
    # Sample test data
    sample_jd = """
    We are looking for a Python developer with strong experience in web development using Django or Flask.
    Required skills: Python, Django, REST APIs, SQL, Git.
    Nice to have: JavaScript, React, AWS, Docker.
    """
    
    sample_resume = """
    Experienced software developer with 3 years in Python programming.
    Proficient in Flask framework and REST API development.
    Strong knowledge of Git version control and basic SQL.
    Some experience with JavaScript and web development.
    """
    
    results = analyzer.analyze_gap(sample_jd, sample_resume)
    
    print("\n" + "="*50)
    print("📊 ANALYSIS RESULTS")
    print("="*50)
    print(f"Overall Match Score: {results['match_score']}%")
    print(f"Interpretation: {results['match_interpretation']}")
    print(f"\n✅ Matching Skills: {results['matching_skills']}")
    print(f"❌ Missing Skills: {results['missing_skills']}")
    
    if results['gap_bridge_plans']:
        print("\n🚀 GAP BRIDGE PLANS GENERATED:")
        for plan in results['gap_bridge_plans']:
            print(f"\n📚 {plan['skill']}:")
            print(f"   Time needed: {plan['time_required']} hours ({plan['weeks_needed']} weeks)")
            print(f"   Resources: {len(plan['resources'])}")
            print(f"   Projects: {len(plan['projects'])}")
    
    print("\n📁 Categorized Skill Gaps:")
    for category, skills in results['categorized_gaps'].items():
        print(f"   {category.title()}: {skills}")

# Only run test if this file is executed directly
if __name__ == "__main__":
    test_analyzer()