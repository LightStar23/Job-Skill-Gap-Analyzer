# job_market.py
import json
import requests
from datetime import datetime, timedelta
import sqlite3
from typing import Dict, List, Optional
import os

class JobMarketPulse:
    def __init__(self):
        # API keys (you can get free API keys from these services)
        self.config = {
            'indeed': os.getenv('INDEED_API_KEY', ''),
            'linkedin': os.getenv('LINKEDIN_API_KEY', ''),
            'glassdoor': os.getenv('GLASSDOOR_API_KEY', '')
        }
        
        # Fallback data when APIs aren't available
        self.fallback_data = self.load_fallback_data()
        
        # Initialize database for caching job data
        self.init_database()
    
    def init_database(self):
        """Initialize job market database"""
        conn = sqlite3.connect('job_market.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_market_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill TEXT NOT NULL,
            location TEXT DEFAULT 'Worldwide',
            demand_level TEXT,
            avg_salary_min INTEGER,
            avg_salary_max INTEGER,
            job_count INTEGER,
            trend TEXT,  -- 'rising', 'stable', 'declining'
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            source TEXT,
            UNIQUE(skill, location)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            skill TEXT,
            growth_rate REAL,
            popularity_score INTEGER,
            week_start DATE,
            UNIQUE(category, skill, week_start)
        )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insert initial data if empty
        self.populate_initial_data()
    
    def load_fallback_data(self):
        """Load fallback job market data"""
        return {
            'Python': {
                'demand': 'very_high',
                'salary_range': [80000, 150000],
                'job_count': 45000,
                'trend': 'rising',
                'growth_rate': 15.5
            },
            'React': {
                'demand': 'high',
                'salary_range': [75000, 140000],
                'job_count': 32000,
                'trend': 'rising',
                'growth_rate': 22.3
            },
            'JavaScript': {
                'demand': 'very_high',
                'salary_range': [70000, 130000],
                'job_count': 52000,
                'trend': 'stable',
                'growth_rate': 8.7
            },
            'Java': {
                'demand': 'high',
                'salary_range': [85000, 160000],
                'job_count': 28000,
                'trend': 'stable',
                'growth_rate': 5.2
            },
            'SQL': {
                'demand': 'high',
                'salary_range': [65000, 120000],
                'job_count': 38000,
                'trend': 'rising',
                'growth_rate': 12.1
            },
            'AWS': {
                'demand': 'very_high',
                'salary_range': [90000, 170000],
                'job_count': 29000,
                'trend': 'rising',
                'growth_rate': 25.4
            },
            'Docker': {
                'demand': 'high',
                'salary_range': [95000, 160000],
                'job_count': 18000,
                'trend': 'rising',
                'growth_rate': 30.2
            },
            'Kubernetes': {
                'demand': 'high',
                'salary_range': [100000, 180000],
                'job_count': 12000,
                'trend': 'rising',
                'growth_rate': 42.7
            }
        }
    
    def populate_initial_data(self):
        """Populate initial job market data"""
        conn = sqlite3.connect('job_market.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM job_market_data")
        count = cursor.fetchone()[0]
        
        if count == 0:
            for skill, data in self.fallback_data.items():
                cursor.execute('''
                INSERT OR REPLACE INTO job_market_data 
                (skill, demand_level, avg_salary_min, avg_salary_max, job_count, trend, source)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    skill,
                    data['demand'],
                    data['salary_range'][0],
                    data['salary_range'][1],
                    data['job_count'],
                    data['trend'],
                    'fallback'
                ))
            
            # Add some trend data
            trends = [
                ('AI/ML', 'Machine Learning', 45.2, 95),
                ('AI/ML', 'TensorFlow', 38.7, 88),
                ('Web Development', 'React', 22.3, 92),
                ('Web Development', 'Vue.js', 18.9, 78),
                ('DevOps', 'Kubernetes', 42.7, 94),
                ('DevOps', 'Docker', 30.2, 89),
                ('Cloud', 'AWS', 25.4, 96),
                ('Cloud', 'Azure', 19.8, 85)
            ]
            
            for category, skill, growth, popularity in trends:
                cursor.execute('''
                INSERT INTO job_trends (category, skill, growth_rate, popularity_score, week_start)
                VALUES (?, ?, ?, ?, ?)
                ''', (category, skill, growth, popularity, datetime.now().date()))
            
            conn.commit()
        
        conn.close()
    
    def get_skill_demand(self, skill_name: str, location: str = "Worldwide") -> Dict:
        """Get demand data for a specific skill"""
        conn = sqlite3.connect('job_market.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Try to get from database first
        cursor.execute('''
        SELECT * FROM job_market_data 
        WHERE skill = ? AND location = ?
        ''', (skill_name, location))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Convert row to dict
            data = dict(row)
            
            # Calculate additional metrics
            data['hotness_score'] = self.calculate_hotness_score(data)
            data['demand_icon'] = self.get_demand_icon(data['demand_level'])
            data['trend_icon'] = self.get_trend_icon(data['trend'])
            
            return data
        
        # If not in DB, use fallback or fetch from API
        return self.fetch_from_api_or_fallback(skill_name, location)
    
    def calculate_hotness_score(self, data: Dict) -> int:
        """Calculate hotness score (0-100) for a skill"""
        score = 0
        
        # Demand level scoring
        demand_scores = {
            'very_high': 40,
            'high': 30,
            'medium': 20,
            'low': 10,
            'very_low': 5
        }
        score += demand_scores.get(data['demand_level'], 15)
        
        # Salary scoring (higher salary = higher score)
        avg_salary = (data['avg_salary_min'] + data['avg_salary_max']) / 2
        if avg_salary > 150000:
            score += 30
        elif avg_salary > 100000:
            score += 20
        elif avg_salary > 70000:
            score += 15
        elif avg_salary > 50000:
            score += 10
        else:
            score += 5
        
        # Job count scoring
        if data['job_count'] > 30000:
            score += 30
        elif data['job_count'] > 10000:
            score += 20
        elif data['job_count'] > 5000:
            score += 15
        elif data['job_count'] > 1000:
            score += 10
        else:
            score += 5
        
        return min(100, score)
    
    def get_demand_icon(self, demand_level: str) -> str:
        """Get icon for demand level"""
        icons = {
            'very_high': '🔥🔥🔥',
            'high': '🔥🔥',
            'medium': '🔥',
            'low': '↘️',
            'very_low': '⬇️'
        }
        return icons.get(demand_level, '➡️')
    
    def get_trend_icon(self, trend: str) -> str:
        """Get icon for trend"""
        icons = {
            'rising': '📈',
            'stable': '➡️',
            'declining': '📉'
        }
        return icons.get(trend, '➡️')
    
    def fetch_from_api_or_fallback(self, skill_name: str, location: str) -> Dict:
        """Fetch data from APIs or use fallback"""
        # Try Indeed API first
        data = self.fetch_indeed_data(skill_name, location)
        
        if not data:
            # Try fallback
            if skill_name in self.fallback_data:
                fallback = self.fallback_data[skill_name]
                data = {
                    'skill': skill_name,
                    'location': location,
                    'demand_level': fallback['demand'],
                    'avg_salary_min': fallback['salary_range'][0],
                    'avg_salary_max': fallback['salary_range'][1],
                    'job_count': fallback['job_count'],
                    'trend': fallback['trend'],
                    'source': 'fallback',
                    'last_updated': datetime.now().isoformat()
                }
            else:
                # Generic data for unknown skills
                data = {
                    'skill': skill_name,
                    'location': location,
                    'demand_level': 'medium',
                    'avg_salary_min': 60000,
                    'avg_salary_max': 110000,
                    'job_count': 1000,
                    'trend': 'stable',
                    'source': 'estimated',
                    'last_updated': datetime.now().isoformat()
                }
        
        # Calculate additional metrics
        data['hotness_score'] = self.calculate_hotness_score(data)
        data['demand_icon'] = self.get_demand_icon(data['demand_level'])
        data['trend_icon'] = self.get_trend_icon(data['trend'])
        
        # Save to database for future use
        self.save_to_database(data)
        
        return data
    
    def fetch_indeed_data(self, skill_name: str, location: str) -> Optional[Dict]:
        """Fetch data from Indeed API (mock for now)"""
        # Mock API response - in production, you'd use real API
        # Example: requests.get(f"https://api.indeed.com/jobs?q={skill_name}&l={location}")
        
        # Simulate API call with mock data
        mock_responses = {
            'Python': {
                'demand_level': 'very_high',
                'salary_range': [85000, 160000],
                'job_count': 51234,
                'trend': 'rising'
            },
            'React': {
                'demand_level': 'high',
                'salary_range': [80000, 145000],
                'job_count': 34567,
                'trend': 'rising'
            }
        }
        
        if skill_name in mock_responses:
            mock = mock_responses[skill_name]
            return {
                'skill': skill_name,
                'location': location,
                'demand_level': mock['demand_level'],
                'avg_salary_min': mock['salary_range'][0],
                'avg_salary_max': mock['salary_range'][1],
                'job_count': mock['job_count'],
                'trend': mock['trend'],
                'source': 'indeed_api',
                'last_updated': datetime.now().isoformat()
            }
        
        return None
    
    def save_to_database(self, data: Dict):
        """Save job market data to database"""
        conn = sqlite3.connect('job_market.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO job_market_data 
        (skill, location, demand_level, avg_salary_min, avg_salary_max, job_count, trend, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['skill'],
            data.get('location', 'Worldwide'),
            data['demand_level'],
            data['avg_salary_min'],
            data['avg_salary_max'],
            data['job_count'],
            data['trend'],
            data['source']
        ))
        
        conn.commit()
        conn.close()
    
    def get_multiple_skills_demand(self, skills: List[str], location: str = "Worldwide") -> Dict:
        """Get demand data for multiple skills"""
        result = {
            'skills': {},
            'summary': {},
            'trending_skills': self.get_trending_skills(),
            'highest_demand': [],
            'salary_comparison': []
        }
        
        for skill in skills:
            result['skills'][skill] = self.get_skill_demand(skill, location)
        
        # Calculate summary statistics
        if result['skills']:
            skills_data = list(result['skills'].values())
            
            result['summary'] = {
                'total_skills': len(skills),
                'avg_hotness_score': sum(s['hotness_score'] for s in skills_data) / len(skills_data),
                'highest_demand_skill': max(skills_data, key=lambda x: x['hotness_score'])['skill'],
                'highest_salary_skill': max(skills_data, key=lambda x: x['avg_salary_max'])['skill'],
                'total_jobs': sum(s['job_count'] for s in skills_data)
            }
            
            # Get top 3 highest demand skills
            result['highest_demand'] = sorted(
                skills_data,
                key=lambda x: x['hotness_score'],
                reverse=True
            )[:3]
            
            # Salary comparison
            result['salary_comparison'] = sorted(
                skills_data,
                key=lambda x: x['avg_salary_max'],
                reverse=True
            )
        
        return result
    
    def get_trending_skills(self, category: str = None) -> List[Dict]:
        """Get trending skills in the market"""
        conn = sqlite3.connect('job_market.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if category:
            cursor.execute('''
            SELECT * FROM job_trends 
            WHERE category = ? 
            ORDER BY growth_rate DESC 
            LIMIT 5
            ''', (category,))
        else:
            cursor.execute('''
            SELECT * FROM job_trends 
            ORDER BY growth_rate DESC 
            LIMIT 10
            ''')
        
        trends = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        # Add emojis based on growth rate
        for trend in trends:
            if trend['growth_rate'] > 30:
                trend['trend_emoji'] = '🚀'
            elif trend['growth_rate'] > 20:
                trend['trend_emoji'] = '🔥'
            elif trend['growth_rate'] > 10:
                trend['trend_emoji'] = '📈'
            else:
                trend['trend_emoji'] = '➡️'
        
        return trends
    
    def get_salary_estimate(self, skill: str, experience_years: int = 3, location: str = "Worldwide") -> Dict:
        """Get salary estimate based on experience"""
        skill_data = self.get_skill_demand(skill, location)
        
        # Adjust salary based on experience
        base_min = skill_data['avg_salary_min']
        base_max = skill_data['avg_salary_max']
        
        if experience_years <= 1:
            adj_min = base_min * 0.7
            adj_max = base_max * 0.8
            level = "Entry Level"
        elif experience_years <= 3:
            adj_min = base_min * 0.9
            adj_max = base_max * 1.0
            level = "Junior"
        elif experience_years <= 5:
            adj_min = base_min * 1.1
            adj_max = base_max * 1.2
            level = "Mid Level"
        elif experience_years <= 8:
            adj_min = base_min * 1.3
            adj_max = base_max * 1.4
            level = "Senior"
        else:
            adj_min = base_min * 1.5
            adj_max = base_max * 1.7
            level = "Expert"
        
        return {
            'skill': skill,
            'experience_years': experience_years,
            'level': level,
            'salary_min': int(adj_min),
            'salary_max': int(adj_max),
            'salary_avg': int((adj_min + adj_max) / 2),
            'location': location,
            'currency': 'USD'
        }
    
    def get_market_report(self, user_skills: List[str], target_skills: List[str], location: str = "Worldwide") -> Dict:
        """Generate comprehensive market report"""
        all_skills = list(set(user_skills + target_skills))
        
        # Get demand for all skills
        demand_data = self.get_multiple_skills_demand(all_skills, location)
        
        # Calculate market value
        user_market_value = self.calculate_market_value(user_skills, location)
        target_market_value = self.calculate_market_value(target_skills, location)
        
        # Get trending skills in relevant categories
        categories = self.detect_categories(all_skills)
        trending_by_category = {}
        for category in categories:
            trending_by_category[category] = self.get_trending_skills(category)
        
        return {
            'demand_analysis': demand_data,
            'market_values': {
                'current_skills_value': user_market_value,
                'target_skills_value': target_market_value,
                'potential_increase': target_market_value - user_market_value,
                'percentage_increase': ((target_market_value - user_market_value) / user_market_value * 100) if user_market_value > 0 else 100
            },
            'trending_skills': trending_by_category,
            'recommendations': self.generate_recommendations(user_skills, target_skills, demand_data),
            'report_generated': datetime.now().isoformat(),
            'location': location
        }
    
    def calculate_market_value(self, skills: List[str], location: str = "Worldwide") -> int:
        """Calculate estimated market value for a set of skills"""
        if not skills:
            return 0
        
        total_value = 0
        for skill in skills:
            data = self.get_skill_demand(skill, location)
            # Weighted by demand level and salary
            weight = {
                'very_high': 1.5,
                'high': 1.2,
                'medium': 1.0,
                'low': 0.8,
                'very_low': 0.5
            }.get(data['demand_level'], 1.0)
            
            avg_salary = (data['avg_salary_min'] + data['avg_salary_max']) / 2
            total_value += avg_salary * weight
        
        return int(total_value / len(skills))
    
    def detect_categories(self, skills: List[str]) -> List[str]:
        """Detect categories from skills"""
        skill_categories = {
            'Python': 'AI/ML',
            'Machine Learning': 'AI/ML',
            'TensorFlow': 'AI/ML',
            'React': 'Web Development',
            'JavaScript': 'Web Development',
            'Vue.js': 'Web Development',
            'Kubernetes': 'DevOps',
            'Docker': 'DevOps',
            'AWS': 'Cloud',
            'Azure': 'Cloud',
            'SQL': 'Database',
            'MongoDB': 'Database'
        }
        
        categories = set()
        for skill in skills:
            if skill in skill_categories:
                categories.add(skill_categories[skill])
        
        return list(categories) or ['General Tech']
    
    def generate_recommendations(self, user_skills: List[str], target_skills: List[str], demand_data: Dict) -> List[str]:
        """Generate market-based recommendations"""
        recommendations = []
        
        missing_skills = set(target_skills) - set(user_skills)
        
        for skill in missing_skills:
            if skill in demand_data['skills']:
                skill_data = demand_data['skills'][skill]
                if skill_data['hotness_score'] > 70:
                    recommendations.append(
                        f"🚨 **High Priority**: {skill} has high market demand (Score: {skill_data['hotness_score']}/100) with {skill_data['job_count']:,} jobs"
                    )
                elif skill_data['hotness_score'] > 50:
                    recommendations.append(
                        f"⚠️ **Good Opportunity**: {skill} has moderate demand (Score: {skill_data['hotness_score']}/100)"
                    )
        
        # Check for trending skills user doesn't have
        trending = self.get_trending_skills()
        for trend in trending[:3]:
            if trend['skill'] not in user_skills and trend['skill'] not in target_skills:
                recommendations.append(
                    f"📈 **Emerging Skill**: {trend['skill']} is trending with {trend['growth_rate']}% growth"
                )
        
        return recommendations

# Create global instance
job_market = JobMarketPulse()