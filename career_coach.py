# career_coach.py
"""
AI Career Coach: Personalized learning path generator based on skill gaps and learner profile.
Integrates with OpenAI LLM for intelligent recommendations with rule-based fallback.
"""

import json
import os
from typing import Dict, List, Any, Optional
import re
from datetime import datetime
from dotenv import load_dotenv

# Try to import OpenAI; fallback to rule-based if unavailable
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

load_dotenv()


class AICareerCoach:
    """Generates personalized career coaching plans based on learner profile and skill gaps."""
    
    # Curated resource database organized by skill/topic
    RESOURCE_DATABASE = {
        "python": {
            "projects": [
                {"title": "Build a CLI Tool", "url": "https://github.com/topics/cli", "cost": "free"},
                {"title": "Data Processing Pipeline", "url": "https://github.com/topics/data-pipeline", "cost": "free"},
                {"title": "Web Scraper", "url": "https://docs.scrapy.org/", "cost": "free"},
            ],
            "courses": [
                {"title": "Python for Everybody", "url": "https://www.py4e.com/", "cost": "free"},
                {"title": "Real Python", "url": "https://realpython.com/", "cost": "paid"},
                {"title": "Codecademy Python", "url": "https://www.codecademy.com/learn/learn-python", "cost": "paid"},
            ],
            "videos": [
                {"title": "Corey Schafer Python Tutorials", "url": "https://www.youtube.com/@coreyms", "cost": "free"},
                {"title": "Tech With Tim", "url": "https://www.youtube.com/@TechWithTim", "cost": "free"},
            ]
        },
        "machine learning": {
            "projects": [
                {"title": "Iris Classification", "url": "https://kaggle.com/datasets/uciml/iris", "cost": "free"},
                {"title": "Titanic Prediction", "url": "https://kaggle.com/competitions/titanic", "cost": "free"},
                {"title": "House Price Prediction", "url": "https://kaggle.com/competitions/house-prices-advanced-regression-techniques", "cost": "free"},
            ],
            "courses": [
                {"title": "Andrew Ng's ML Course", "url": "https://www.coursera.org/learn/machine-learning", "cost": "free"},
                {"title": "Fast.ai", "url": "https://www.fast.ai/", "cost": "free"},
                {"title": "Google ML Crash Course", "url": "https://developers.google.com/machine-learning/crash-course", "cost": "free"},
            ],
            "books": [
                {"title": "Hands-On ML with Scikit-Learn, Keras, TensorFlow", "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/", "cost": "paid"},
            ]
        },
        "react": {
            "projects": [
                {"title": "Todo App", "url": "https://react.dev/learn", "cost": "free"},
                {"title": "Weather App", "url": "https://openweathermap.org/api", "cost": "free"},
                {"title": "E-commerce Cart", "url": "https://github.com/topics/react-ecommerce", "cost": "free"},
            ],
            "courses": [
                {"title": "React Official Tutorial", "url": "https://react.dev/learn", "cost": "free"},
                {"title": "Scrimba React Course", "url": "https://scrimba.com/learn/react", "cost": "free"},
                {"title": "Udemy React Course", "url": "https://www.udemy.com/course/react-the-complete-guide/", "cost": "paid"},
            ]
        },
        "docker": {
            "projects": [
                {"title": "Dockerize a Flask App", "url": "https://docs.docker.com/language/python/build-images/", "cost": "free"},
                {"title": "Multi-container Setup", "url": "https://docs.docker.com/compose/", "cost": "free"},
            ],
            "courses": [
                {"title": "Docker Official Docs", "url": "https://docs.docker.com/", "cost": "free"},
                {"title": "Play with Docker", "url": "https://www.docker.com/play", "cost": "free"},
            ]
        },
        "aws": {
            "projects": [
                {"title": "Deploy Flask App on EC2", "url": "https://aws.amazon.com/ec2/", "cost": "free"},
                {"title": "S3 File Storage", "url": "https://aws.amazon.com/s3/", "cost": "free"},
            ],
            "courses": [
                {"title": "AWS Free Tier", "url": "https://aws.amazon.com/free/", "cost": "free"},
                {"title": "A Cloud Guru", "url": "https://acloudguru.com/", "cost": "paid"},
            ]
        },
        "sql": {
            "projects": [
                {"title": "SQL Zoo", "url": "https://sqlzoo.net/", "cost": "free"},
                {"title": "LeetCode SQL", "url": "https://leetcode.com/tag/database/", "cost": "free"},
            ],
            "courses": [
                {"title": "SQL Tutorial", "url": "https://www.w3schools.com/sql/", "cost": "free"},
                {"title": "Mode SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "cost": "free"},
            ]
        },
        "git": {
            "projects": [
                {"title": "Learn Git Branching", "url": "https://learngitbranching.js.org/", "cost": "free"},
                {"title": "GitHub Flow", "url": "https://guides.github.com/introduction/flow/", "cost": "free"},
            ],
            "courses": [
                {"title": "Git Official Docs", "url": "https://git-scm.com/doc", "cost": "free"},
            ]
        },
        "communication": {
            "courses": [
                {"title": "Toastmasters Public Speaking", "url": "https://www.toastmasters.org/", "cost": "low"},
                {"title": "Coursera Communication Skills", "url": "https://www.coursera.org/search?query=communication", "cost": "free"},
            ],
            "videos": [
                {"title": "TED Talks", "url": "https://www.ted.com/", "cost": "free"},
            ]
        },
        "leadership": {
            "courses": [
                {"title": "Coursera Leadership", "url": "https://www.coursera.org/search?query=leadership", "cost": "free"},
                {"title": "LinkedIn Learning", "url": "https://www.linkedin.com/learning/", "cost": "paid"},
            ]
        },
    }
    
    # Emerging trends mapping (tech field)
    EMERGING_TRENDS = [
        {
            "trend": "AI/ML Integration in Backend",
            "impact_on_roles": ["Backend Developer", "ML Engineer", "Data Scientist"],
            "why": "LLMs and ML are becoming standard in modern applications",
            "verification_signals": ["job-posting-trend", "github-stars", "conference-talks"]
        },
        {
            "trend": "TypeScript over JavaScript",
            "impact_on_roles": ["Frontend Developer", "Full Stack Developer"],
            "why": "Type safety reduces bugs in large codebases; 70%+ of new projects use TS",
            "verification_signals": ["npm-download-trends", "github-language-stats"]
        },
        {
            "trend": "Rust for Systems Programming",
            "impact_on_roles": ["Systems Engineer", "DevOps Engineer"],
            "why": "Memory safety without GC; adoption in AWS, blockchain, cli tools",
            "verification_signals": ["stackoverflow-survey", "github-language-trends"]
        },
        {
            "trend": "Serverless & Edge Computing",
            "impact_on_roles": ["Backend Developer", "DevOps Engineer", "Cloud Architect"],
            "why": "Cost reduction and global latency improvements drive adoption",
            "verification_signals": ["aws-announcements", "job-postings", "tech-conferences"]
        },
        {
            "trend": "LLM Prompt Engineering",
            "impact_on_roles": ["AI Engineer", "Data Scientist", "Product Manager"],
            "why": "New critical skill for interacting with GPT-based APIs and tools",
            "verification_signals": ["course-launches", "linkedin-posts", "github-projects"]
        },
    ]
    
    # Obsolete/Low-Return Skills
    OBSOLETE_SKILLS = {
        "jquery": {
            "reason": "jQuery is outdated; modern frameworks (React, Vue) handle DOM manipulation better",
            "suggested_alternatives": ["React", "Vue", "Vanilla JS ES6+"]
        },
        "flash": {
            "reason": "Deprecated; browsers no longer support Flash",
            "suggested_alternatives": ["HTML5", "Canvas", "WebGL"]
        },
        "cobol": {
            "reason": "Legacy language with shrinking job market; very niche",
            "suggested_alternatives": ["Python", "Java", "C#"]
        },
        "silverlight": {
            "reason": "Deprecated Microsoft technology",
            "suggested_alternatives": ["React", "ASP.NET Core", "Azure"]
        },
        "perl": {
            "reason": "Low demand in modern tech job market; scripting moved to Python/Bash",
            "suggested_alternatives": ["Python", "Bash", "Go"]
        },
    }
    
    def __init__(self):
        """Initialize the AI Career Coach."""
        self.openai_client = None
        if OPENAI_AVAILABLE:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.openai_client = OpenAI(api_key=api_key)
    
    def generate_coaching_plan(self, user_profile: Dict[str, Any], skill_gap: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive coaching plan.
        
        Args:
            user_profile: User profile with target_role, experience_years, availability, learning_style, budget
            skill_gap: Skill gap analysis with score, gaps list, strengths list
        
        Returns:
            Complete coaching plan JSON following the required schema
        """
        # Validate inputs
        if not user_profile.get("target_role"):
            return {"error": "target_role is required"}
        
        # Get basic coaching framework
        plan = self._build_base_plan(user_profile, skill_gap)
        
        # Enhance with LLM if available
        if self.openai_client:
            plan = self._enhance_with_llm(plan, user_profile, skill_gap)
        
        return plan
    
    def _build_base_plan(self, user_profile: Dict[str, Any], skill_gap: Dict[str, Any]) -> Dict[str, Any]:
        """Build base coaching plan using rule-based logic."""
        target_role = user_profile.get("target_role", "Unknown")
        experience_years = user_profile.get("experience_years", 0)
        availability_hours = user_profile.get("availability_per_week_hours", 10)
        learning_style = user_profile.get("preferred_learning_style", "projects")
        budget = user_profile.get("budget_level", "free")
        
        # Extract gaps
        gaps = skill_gap.get("gaps", [])
        strengths = skill_gap.get("strengths", [])
        score = skill_gap.get("score", 0)
        
        # Generate human message
        human_message = self._generate_human_message(target_role, score, experience_years)
        
        # Generate summary
        if gaps:
            top_gap = gaps[0]["skill"] if isinstance(gaps[0], dict) else gaps[0]
            summary = f"You're {score}% aligned. Focus: master {top_gap}. Timeline: 12 weeks."
        else:
            summary = f"You're {score}% aligned with {target_role}. Consolidate strengths & expand emerging skills."
        
        # Build prioritized path
        prioritized_path = self._build_prioritized_path(gaps, target_role, learning_style, budget)
        
        # Identify obsolete skills
        obsolete = self._identify_obsolete_skills(gaps)
        
        # Get relevant emerging trends
        trends = self._get_emerging_trends_for_role(target_role)
        
        # Build study schedule
        schedule = self._build_study_schedule(availability_hours, prioritized_path)
        
        # Next actions
        next_actions = self._generate_next_actions_72h(gaps, target_role)
        
        # Calculate confidence
        confidence = min(1.0, (score / 100) * 0.5 + 0.5)  # Higher gaps = lower confidence in plan
        
        explainability = self._generate_explainability(gaps, strengths, target_role, score)
        
        return {
            "human_message": human_message,
            "summary": summary,
            "prioritized_path": prioritized_path,
            "obsolete_skills": obsolete,
            "emerging_trends": trends,
            "study_schedule": schedule,
            "next_actions_72h": next_actions,
            "confidence": confidence,
            "explainability": explainability,
            "tracking_hooks": {
                "progress_metric_ids": [f"metric_{i}" for i in range(len(prioritized_path))],
                "suggested_check_in_frequency_days": 7
            }
        }
    
    def _generate_human_message(self, target_role: str, score: float, experience_years: int) -> str:
        """Generate a friendly opening message."""
        if score >= 80:
            return f"Great news! You're well-positioned for {target_role}. Let's fine-tune your skills and stay ahead of emerging trends. I've prioritized the highest-impact learning areas for your timeline."
        elif score >= 50:
            return f"You have a solid foundation for {target_role}. Let's close the skill gaps strategically. I've mapped a focused path that respects your time and budget."
        else:
            return f"You're starting your journey toward {target_role}. No worries—I've designed a step-by-step plan focused on quick wins and foundational skills first."
    
    def _build_prioritized_path(self, gaps: List[Any], target_role: str, learning_style: str, budget: str) -> List[Dict[str, Any]]:
        """Build a prioritized learning path with milestones."""
        path = []
        
        # Normalize gaps
        normalized_gaps = []
        for gap in gaps[:5]:  # Top 5 gaps
            if isinstance(gap, dict):
                normalized_gaps.append(gap)
            else:
                normalized_gaps.append({"skill": gap, "gap": 5, "importance": 0.8})
        
        for idx, gap in enumerate(normalized_gaps, 1):
            skill = gap.get("skill", "Unknown")
            importance = gap.get("importance", 0.8)
            current_level = gap.get("current_level", 0)
            gap_size = gap.get("gap", 5)
            
            # Estimate time based on gap size (rough: 1 week per gap level, min 2 weeks)
            time_estimate = max(2, gap_size // 2)
            
            milestone = {
                "milestone_id": f"m{idx}",
                "title": self._generate_milestone_title(skill, idx),
                "skills_targeted": [skill],
                "why": f"High priority for {target_role}: {importance*100:.0f}% importance, current level {current_level}/10",
                "time_estimate_weeks": time_estimate,
                "practice_tasks": self._generate_practice_tasks(skill, current_level, learning_style),
                "resources": self._get_resources_for_skill(skill, learning_style, budget),
                "validation": self._generate_validation_metric(skill)
            }
            path.append(milestone)
        
        return path
    
    def _generate_milestone_title(self, skill: str, idx: int) -> str:
        """Generate a milestone title."""
        titles = {
            "python": "Python Fundamentals & Best Practices",
            "machine learning": "ML Fundamentals: Data → Predictions",
            "react": "React Mastery: Components to Production",
            "aws": "AWS Essentials: Deploy & Scale",
            "docker": "Containerization with Docker",
            "communication": "Clear & Confident Communication",
            "leadership": "Technical Leadership Skills",
            "typescript": "TypeScript for Type-Safe Development",
            "kubernetes": "Kubernetes Orchestration",
        }
        return titles.get(skill.lower(), f"Master {skill.title()}")
    
    def _generate_practice_tasks(self, skill: str, current_level: int, learning_style: str) -> List[Dict[str, Any]]:
        """Generate practice tasks based on skill and learning style."""
        tasks_map = {
            "python": [
                {"task": "Build a CLI calculator tool", "acceptance_criteria": "Handles +,-,*,/ and persists history", "est_hours": 4},
                {"task": "Refactor existing code with type hints", "acceptance_criteria": "100% type coverage, mypy pass", "est_hours": 3},
                {"task": "Contribute to open-source Python project", "acceptance_criteria": "PR merged", "est_hours": 8},
            ],
            "machine learning": [
                {"task": "Build Iris classifier", "acceptance_criteria": ">90% accuracy on test set", "est_hours": 6},
                {"task": "Train regression model on real dataset", "acceptance_criteria": "RMSE < threshold, documented", "est_hours": 8},
                {"task": "Deploy model as API", "acceptance_criteria": "API returns predictions, logged", "est_hours": 6},
            ],
            "react": [
                {"task": "Build interactive Todo app", "acceptance_criteria": "CRUD ops work, localStorage persists", "est_hours": 5},
                {"task": "Refactor class component to hooks", "acceptance_criteria": "Tests pass, no warnings", "est_hours": 4},
                {"task": "Integrate 3rd-party API", "acceptance_criteria": "Real data fetched, error handling", "est_hours": 6},
            ],
            "communication": [
                {"task": "Record 3-min technical explanation", "acceptance_criteria": "Clear, <30 seconds per concept", "est_hours": 2},
                {"task": "Give practice talk on your project", "acceptance_criteria": "Video reviewed, feedback applied", "est_hours": 3},
                {"task": "Write technical blog post", "acceptance_criteria": ">500 words, proofread, published", "est_hours": 4},
            ],
        }
        
        default_tasks = [
            {"task": f"Complete beginner tutorial on {skill}", "acceptance_criteria": "Finish course, quiz >80%", "est_hours": 4},
            {"task": f"Build small project using {skill}", "acceptance_criteria": "Working code on GitHub, documented", "est_hours": 6},
            {"task": f"Practice problems on {skill}", "acceptance_criteria": "Solve 10+ problems, share solutions", "est_hours": 5},
        ]
        
        return tasks_map.get(skill.lower(), default_tasks)
    
    def _get_resources_for_skill(self, skill: str, learning_style: str, budget: str) -> List[Dict[str, Any]]:
        """Fetch curated resources for a skill."""
        resources = []
        skill_lower = skill.lower()
        
        # Get from database
        if skill_lower in self.RESOURCE_DATABASE:
            db = self.RESOURCE_DATABASE[skill_lower]
            
            # Prioritize by learning style
            type_priority = {
                "projects": ["projects", "courses", "videos", "books", "article"],
                "videos": ["videos", "courses", "projects", "article"],
                "text": ["courses", "books", "article", "videos"],
                "mentorship": ["courses", "videos", "projects"],
            }
            
            types_to_fetch = type_priority.get(learning_style, ["projects", "courses"])
            
            for resource_type in types_to_fetch:
                if resource_type in db and len(resources) < 5:
                    for res in db[resource_type]:
                        if len(resources) < 5:
                            # Filter by budget
                            if budget == "free" and res.get("cost") == "paid":
                                continue
                            resources.append({
                                "type": resource_type,
                                "title": res["title"],
                                "url": res.get("url"),
                                "cost": res.get("cost", "free")
                            })
        
        # Fallback: generic resources
        if len(resources) < 5:
            resources.extend([
                {
                    "type": "course",
                    "title": f"{skill} Fundamentals Course",
                    "url": f"https://www.udemy.com/search/?q={skill.replace(' ', '+')}",
                    "cost": budget
                },
                {
                    "type": "project",
                    "title": f"GitHub Projects tagged #{skill.lower().replace(' ', '-')}",
                    "url": f"https://github.com/topics/{skill.lower().replace(' ', '-')}",
                    "cost": "free"
                }
            ])
        
        return resources[:5]
    
    def _generate_validation_metric(self, skill: str) -> Dict[str, Any]:
        """Generate validation metrics for learning."""
        metrics_map = {
            "python": {"metric": "GitHub repo with 3+ projects", "threshold": "All projects run without errors, documented"},
            "machine learning": {"metric": "Kaggle competition or project", "threshold": "Model >85% accuracy, blog post written"},
            "react": {"metric": "Deploy working React app", "threshold": "App live, >80% lighthouse score"},
            "communication": {"metric": "Technical talk or blog post", "threshold": "Peer review score >8/10"},
            "leadership": {"metric": "Lead a small team project", "threshold": "Team feedback: clear direction & support"},
        }
        
        return metrics_map.get(skill.lower(), {
            "metric": f"Complete {skill} project",
            "threshold": "Code reviewed, documented, and tested"
        })
    
    def _identify_obsolete_skills(self, gaps: List[Any]) -> List[Dict[str, Any]]:
        """Identify obsolete or low-return skills in the gap list."""
        obsolete = []
        for gap in gaps:
            skill = gap.get("skill", gap) if isinstance(gap, dict) else gap
            skill_lower = skill.lower().strip()
            
            if skill_lower in self.OBSOLETE_SKILLS:
                obs = self.OBSOLETE_SKILLS[skill_lower]
                obsolete.append({
                    "skill": skill,
                    "reason": obs["reason"],
                    "suggested_alternatives": obs["suggested_alternatives"]
                })
        
        return obsolete
    
    def _get_emerging_trends_for_role(self, target_role: str) -> List[Dict[str, Any]]:
        """Get emerging trends relevant to the target role."""
        role_lower = target_role.lower()
        trends = []
        
        for trend in self.EMERGING_TRENDS:
            if any(role in trend["impact_on_roles"] for role in [target_role, role_lower]):
                trends.append({
                    "trend": trend["trend"],
                    "impact_on_role": "increase",
                    "why": trend["why"],
                    "verification_signals": trend["verification_signals"]
                })
        
        # Add generic trends
        if len(trends) == 0:
            trends = [
                {
                    "trend": "AI/ML Integration",
                    "impact_on_role": "increase",
                    "why": "Most modern roles benefit from LLM and ML capabilities",
                    "verification_signals": ["job-posting-trend", "github-stars"]
                }
            ]
        
        return trends[:3]
    
    def _build_study_schedule(self, availability_hours: int, prioritized_path: List[Dict]) -> Dict[str, Any]:
        """Build a 12-week study schedule."""
        total_weeks = 12
        weeks_plan = []
        
        # Distribute milestones across weeks
        milestone_idx = 0
        weeks_per_milestone = max(1, total_weeks // len(prioritized_path)) if prioritized_path else 4
        
        for week in range(1, total_weeks + 1):
            current_milestone_idx = min((week - 1) // weeks_per_milestone, len(prioritized_path) - 1) if prioritized_path else 0
            
            if current_milestone_idx < len(prioritized_path):
                milestone = prioritized_path[current_milestone_idx]
                focus = milestone.get("skills_targeted", [])
                tasks = [t["task"] for t in milestone.get("practice_tasks", [])[:2]]
            else:
                focus = ["Review & Practice"]
                tasks = ["Consolidate learning", "Build portfolio project"]
            
            weeks_plan.append({
                "week": week,
                "hours": availability_hours,
                "focus": focus,
                "tasks": tasks
            })
        
        return {
            "duration_weeks": total_weeks,
            "weekly_plan": weeks_plan
        }
    
    def _generate_next_actions_72h(self, gaps: List[Any], target_role: str) -> List[str]:
        """Generate 3 immediate micro tasks for next 72 hours."""
        actions = []
        
        # Action 1: Assessment
        if gaps:
            top_skill = gaps[0].get("skill", gaps[0]) if isinstance(gaps[0], dict) else gaps[0]
            actions.append(f"Assess your current {top_skill} level: complete free online quiz or do a quick code challenge (30 min)")
        else:
            actions.append(f"Research current job market for {target_role} on LinkedIn & GitHub (30 min)")
        
        # Action 2: Curated resource
        actions.append("Find and bookmark 3 recommended resources for your top priority skill (20 min)")
        
        # Action 3: Setup
        actions.append("Set up learning environment: GitHub repo, IDE, learning tracker (30 min)")
        
        return actions
    
    def _generate_explainability(self, gaps: List[Any], strengths: List[str], target_role: str, score: float) -> str:
        """Generate explainability notes on prioritization."""
        top_gap_count = min(3, len(gaps))
        explanation = f"• Prioritized top {top_gap_count} skill gaps by importance weight and frequency in {target_role} roles. "
        explanation += f"• Current match score: {score}%. "
        
        if strengths:
            explanation += f"• Your strengths ({', '.join(strengths[:2])}+) provide foundation to build on. "
        
        explanation += "• Schedule assumes 12-week timeline; adjust if timeframe differs. "
        explanation += "• Resources filtered by budget and learning style preference. "
        explanation += "• Milestones include real practice tasks to validate skill, not just passive learning."
        
        return explanation
    
    def _enhance_with_llm(self, base_plan: Dict[str, Any], user_profile: Dict[str, Any], skill_gap: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance plan with LLM-generated insights (OpenAI)."""
        try:
            prompt = self._build_llm_prompt(user_profile, skill_gap, base_plan)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert career coach for tech professionals."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500,
            )
            
            llm_insights = response.choices[0].message.content
            
            # Parse and integrate LLM insights
            # This is flexible; you can enhance specific fields
            base_plan["llm_insights"] = llm_insights
            base_plan["confidence"] = min(1.0, base_plan.get("confidence", 0.5) + 0.15)  # Boost confidence with LLM
            
            return base_plan
        except Exception as e:
            # Graceful fallback
            print(f"LLM enhancement failed (will use rule-based plan): {str(e)}")
            return base_plan
    
    def _build_llm_prompt(self, user_profile: Dict[str, Any], skill_gap: Dict[str, Any], base_plan: Dict[str, Any]) -> str:
        """Build a prompt for LLM enhancement."""
        target_role = user_profile.get("target_role", "Unknown")
        experience = user_profile.get("experience_years", 0)
        availability = user_profile.get("availability_per_week_hours", 10)
        
        gaps_str = ", ".join([g.get("skill", g) if isinstance(g, dict) else g for g in skill_gap.get("gaps", [])[:5]])
        
        prompt = f"""
        I'm a career coach helping {user_profile.get('name', 'a professional')} transition to {target_role}.
        
        Profile:
        - Current role: {user_profile.get('current_role', 'Not specified')}
        - Experience: {experience} years
        - Available: {availability} hrs/week for learning
        - Learning style: {user_profile.get('preferred_learning_style', 'mixed')}
        - Budget: {user_profile.get('budget_level', 'free')}
        
        Current gaps: {gaps_str}
        Current match score: {skill_gap.get('score', 0)}%
        
        Based on this profile and the base coaching plan above, provide 2-3 specific, actionable coaching insights that:
        1. Highlight the highest-ROI skill to focus on first
        2. Suggest a realistic timeline adjustment if needed
        3. Flag any red flags or accelerators in their profile
        
        Keep it conversational and encouraging. Max 200 words.
        """
        return prompt
    
    def update_milestone_progress(self, coaching_plan_id: int, milestone_id: str, task_index: int, 
                                  status: str, validation_evidence: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Update progress on a specific milestone/task.
        
        Args:
            coaching_plan_id: ID of the coaching plan
            milestone_id: e.g., "m1", "m2"
            task_index: Index of practice task (0-based)
            status: "not_started", "in_progress", "completed"
            validation_evidence: Dict with evidence (e.g., {"project_link": "...", "test_score": 85})
        
        Returns:
            Updated progress dict
        """
        # This will be used in the database layer to persist progress
        return {
            "coaching_plan_id": coaching_plan_id,
            "milestone_id": milestone_id,
            "task_index": task_index,
            "status": status,
            "validation_evidence": validation_evidence or {},
            "updated_at": datetime.utcnow().isoformat()
        }
    
    def calculate_overall_progress(self, coaching_plan_data: Dict[str, Any], completed_milestones: List[str]) -> Dict[str, Any]:
        """
        Calculate overall progress percentage and next recommended milestone.
        
        Args:
            coaching_plan_data: Full coaching plan JSON
            completed_milestones: List of completed milestone IDs (e.g., ["m1", "m2"])
        
        Returns:
            Progress summary
        """
        path = coaching_plan_data.get("prioritized_path", [])
        total_milestones = len(path)
        
        if total_milestones == 0:
            return {"progress_percentage": 0, "next_milestone": None}
        
        completion_percentage = int((len(completed_milestones) / total_milestones) * 100)
        
        # Find next milestone
        next_milestone = None
        for milestone in path:
            if milestone.get("milestone_id") not in completed_milestones:
                next_milestone = milestone
                break
        
        return {
            "progress_percentage": completion_percentage,
            "completed_milestones": completed_milestones,
            "total_milestones": total_milestones,
            "next_milestone": next_milestone,
            "estimated_completion_weeks": (total_milestones - len(completed_milestones)) * 2
        }
