import sqlite3
import json
from datetime import datetime

def setup_database():
    """Create database and tables with sample data"""
    
    # Connect to SQLite database (creates file if doesn't exist)
    conn = sqlite3.connect('skill_analyzer.db')
    cursor = conn.cursor()
    
    print("🚀 Setting up Skill Analyzer Database...")
    print("=" * 50)
    
    # ========== TABLE 1: skill_recommendations ==========
    print("\n📊 Creating 'skill_recommendations' table...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS skill_recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT NOT NULL,
        skill_level TEXT DEFAULT 'beginner',
        category TEXT,
        
        -- JSON data stored as TEXT
        free_resources TEXT,
        paid_resources TEXT,
        project_ideas TEXT,
        certifications TEXT,
        
        -- Time estimates (in hours)
        time_to_beginner INTEGER DEFAULT 20,
        time_to_intermediate INTEGER DEFAULT 50,
        time_to_advanced INTEGER DEFAULT 100,
        
        -- Metadata
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        popularity_score INTEGER DEFAULT 0,
        average_rating REAL DEFAULT 0.0
    )
    ''')
    
    # Create indexes for faster searches
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_skill_name ON skill_recommendations(skill_name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_skill_level ON skill_recommendations(skill_level)')
    
    print("✅ Created skill_recommendations table")
    
    # ========== TABLE 2: user_gap_plans ==========
    print("\n📝 Creating 'user_gap_plans' table...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_gap_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        missing_skill TEXT NOT NULL,
        
        -- Selected items (JSON stored as TEXT)
        selected_resources TEXT,
        selected_projects TEXT,
        selected_certifications TEXT,
        
        -- Progress tracking
        start_date DATE,
        target_completion_date DATE,
        current_progress INTEGER DEFAULT 0,  -- percentage 0-100
        
        -- Time commitment
        weekly_hours_commitment INTEGER DEFAULT 5,
        estimated_completion_date DATE,
        
        -- Status
        status TEXT DEFAULT 'not_started',  -- not_started, in_progress, completed, paused
        notes TEXT,
        
        -- Timestamps
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON user_gap_plans(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_skill ON user_gap_plans(user_id, missing_skill)')
    
    print("✅ Created user_gap_plans table")
    
    # ========== INSERT SAMPLE DATA ==========
    print("\n📥 Inserting sample skill data...")
    
    # Sample skills with detailed JSON data
    sample_skills = [
        {
            "skill_name": "React",
            "category": "Frontend Development",
            "free_resources": json.dumps([
                {
                    "name": "React Official Tutorial",
                    "url": "https://reactjs.org/tutorial/tutorial.html",
                    "type": "Interactive Tutorial",
                    "rating": 4.9,
                    "duration_hours": 10,
                    "difficulty": "Beginner"
                },
                {
                    "name": "FreeCodeCamp React Course",
                    "url": "https://www.freecodecamp.org/learn/front-end-libraries/react/",
                    "type": "Interactive Course",
                    "rating": 4.8,
                    "duration_hours": 300,
                    "difficulty": "Beginner to Intermediate"
                },
                {
                    "name": "Scrimba React Tutorial",
                    "url": "https://scrimba.com/learn/learnreact",
                    "type": "Video Tutorial",
                    "rating": 4.7,
                    "duration_hours": 15,
                    "difficulty": "Beginner"
                }
            ]),
            "paid_resources": json.dumps([
                {
                    "name": "React - The Complete Guide (incl Hooks, React Router, Redux)",
                    "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
                    "provider": "Udemy",
                    "price": 89.99,
                    "rating": 4.7,
                    "duration_hours": 48,
                    "difficulty": "Beginner to Advanced"
                }
            ]),
            "project_ideas": json.dumps([
                {
                    "title": "Todo List Application",
                    "description": "Build a todo app with add, edit, delete, and filter functionalities using React Hooks",
                    "complexity": "Beginner",
                    "estimated_time": 8,
                    "skills_covered": ["React Hooks", "State Management", "Component Design"]
                },
                {
                    "title": "Weather Dashboard",
                    "description": "Create a weather app that fetches data from an API and displays forecasts with charts",
                    "complexity": "Intermediate",
                    "estimated_time": 15,
                    "skills_covered": ["API Integration", "React Hooks", "Chart Libraries", "Async Operations"]
                },
                {
                    "title": "E-commerce Product Filter",
                    "description": "Build a product listing page with advanced filtering, sorting, and cart functionality",
                    "complexity": "Intermediate",
                    "estimated_time": 20,
                    "skills_covered": ["React Context", "Filtering Logic", "State Management", "UI/UX Design"]
                }
            ]),
            "certifications": json.dumps([
                {
                    "name": "Meta Front-End Developer Professional Certificate",
                    "provider": "Meta via Coursera",
                    "url": "https://www.coursera.org/professional-certificates/meta-front-end-developer",
                    "cost": "Monthly subscription",
                    "duration": "7 months",
                    "recognition": "Industry-recognized"
                },
                {
                    "name": "React Developer Certificate",
                    "provider": "W3Schools",
                    "url": "https://www.w3schools.com/react/react_exercises.asp",
                    "cost": "Free",
                    "duration": "Self-paced",
                    "recognition": "Learning verification"
                }
            ]),
            "time_to_beginner": 40,
            "time_to_intermediate": 70,
            "time_to_advanced": 120
        },
        {
            "skill_name": "Python",
            "category": "Backend Development",
            "free_resources": json.dumps([
                {
                    "name": "Python for Everybody",
                    "url": "https://www.py4e.com/",
                    "type": "University Course",
                    "rating": 4.8,
                    "duration_hours": 20,
                    "difficulty": "Beginner"
                },
                {
                    "name": "Automate the Boring Stuff with Python",
                    "url": "https://automatetheboringstuff.com/",
                    "type": "Book/Online Course",
                    "rating": 4.7,
                    "duration_hours": 15,
                    "difficulty": "Beginner to Intermediate"
                }
            ]),
            "project_ideas": json.dumps([
                {
                    "title": "Automated File Organizer",
                    "description": "Script that organizes files in a directory by type, date, or size",
                    "complexity": "Beginner",
                    "estimated_time": 5,
                    "skills_covered": ["File I/O", "OS Operations", "Basic Scripting"]
                },
                {
                    "title": "Web Scraper",
                    "description": "Extract data from websites and save to CSV/Excel",
                    "complexity": "Intermediate",
                    "estimated_time": 10,
                    "skills_covered": ["Requests", "BeautifulSoup", "Data Processing", "CSV Operations"]
                }
            ]),
            "time_to_beginner": 30,
            "time_to_intermediate": 60,
            "time_to_advanced": 100
        },
        {
            "skill_name": "JavaScript",
            "category": "Frontend Development",
            "free_resources": json.dumps([
                {
                    "name": "MDN JavaScript Guide",
                    "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
                    "type": "Documentation",
                    "rating": 4.9,
                    "duration_hours": 25,
                    "difficulty": "Beginner to Advanced"
                }
            ]),
            "time_to_beginner": 35,
            "time_to_intermediate": 65,
            "time_to_advanced": 110
        }
    ]
    
    # Insert sample skills
    for skill in sample_skills:
        cursor.execute('''
        INSERT OR IGNORE INTO skill_recommendations 
        (skill_name, category, free_resources, paid_resources, project_ideas, certifications, 
         time_to_beginner, time_to_intermediate, time_to_advanced)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            skill["skill_name"],
            skill["category"],
            skill.get("free_resources", "[]"),
            skill.get("paid_resources", "[]"),
            skill.get("project_ideas", "[]"),
            skill.get("certifications", "[]"),
            skill["time_to_beginner"],
            skill["time_to_intermediate"],
            skill["time_to_advanced"]
        ))
    
    print(f"✅ Inserted {len(sample_skills)} sample skills")
    
    # ========== VERIFY DATA ==========
    print("\n🔍 Verifying database setup...")
    
    # Count skills
    cursor.execute("SELECT COUNT(*) FROM skill_recommendations")
    skill_count = cursor.fetchone()[0]
    print(f"   Total skills in database: {skill_count}")
    
    # List skills
    cursor.execute("SELECT skill_name, category, time_to_beginner FROM skill_recommendations")
    skills = cursor.fetchall()
    print("   Sample skills:")
    for skill in skills:
        print(f"   • {skill[0]} ({skill[1]}) - {skill[2]} hours to beginner")
    
    # Show table info
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\n📋 Tables created: {', '.join([t[0] for t in tables])}")
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 50)
    print("🎉 Database setup completed successfully!")
    print("📁 Database file: 'skill_analyzer.db'")
    print("💡 Next: Integrate with your skill analyzer code")

# Helper functions for your analyzer
def get_skill_bridge(skill_name):
    """Fetch gap bridge data for a specific skill"""
    conn = sqlite3.connect('skill_analyzer.db')
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM skill_recommendations WHERE skill_name = ?", 
        (skill_name,)
    )
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        # Map row to dictionary
        return {
            'skill_name': row[1],
            'category': row[3],
            'free_resources': json.loads(row[4]) if row[4] else [],
            'paid_resources': json.loads(row[5]) if row[5] else [],
            'project_ideas': json.loads(row[6]) if row[6] else [],
            'certifications': json.loads(row[7]) if row[7] else [],
            'time_to_beginner': row[8],
            'time_to_intermediate': row[9],
            'time_to_advanced': row[10]
        }
    return None

def create_user_plan(user_id, missing_skill, selected_items):
    """Create a personalized gap bridge plan for user"""
    conn = sqlite3.connect('skill_analyzer.db')
    cursor = conn.cursor()
    
    # Calculate estimated completion date (assuming 5 hours/week)
    from datetime import datetime, timedelta
    skill_data = get_skill_bridge(missing_skill)
    
    if skill_data:
        total_hours = skill_data['time_to_beginner']
        weeks_needed = total_hours / 5  # 5 hours/week default
        estimated_date = datetime.now() + timedelta(weeks=weeks_needed)
        
        cursor.execute('''
        INSERT INTO user_gap_plans 
        (user_id, missing_skill, selected_resources, estimated_completion_date, status)
        VALUES (?, ?, ?, ?, 'not_started')
        ''', (
            user_id,
            missing_skill,
            json.dumps(selected_items),
            estimated_date.date()
        ))
        
        plan_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return plan_id
    
    conn.close()
    return None

if __name__ == '__main__':
    setup_database()
    
    # Test the helper functions
    print("\n🧪 Testing helper functions...")
    
    # Test getting a skill bridge
    react_plan = get_skill_bridge("React")
    if react_plan:
        print(f"✓ Fetched React skill bridge")
        print(f"  - {len(react_plan['free_resources'])} free resources")
        print(f"  - {len(react_plan['project_ideas'])} project ideas")
        print(f"  - {react_plan['time_to_beginner']} hours to beginner level")
    
    # Test creating a user plan
    test_user_id = 123
    test_selected = {
        "resources": ["React Official Tutorial", "FreeCodeCamp React Course"],
        "projects": ["Todo List Application"]
    }
    
    plan_id = create_user_plan(test_user_id, "React", test_selected)
    if plan_id:
        print(f"✓ Created user gap plan (ID: {plan_id})")