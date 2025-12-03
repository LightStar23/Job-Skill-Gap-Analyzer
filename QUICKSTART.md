# AI Career Coach - Quick Start Guide

## 🚀 What's New

Your Job Skill Gap Analyzer now includes an **AI Career Coach** that transforms skill gap analysis into actionable, personalized learning plans. The coach generates:

- ✅ **Prioritized learning paths** with milestones and practice tasks
- ✅ **Curated resources** (projects, courses, videos, books) matching your budget & learning style
- ✅ **12-week study schedule** with weekly hour allocation
- ✅ **Progress tracking** with validation metrics
- ✅ **Trend alerts** for emerging skills that matter for your role
- ✅ **Obsolete skill warnings** to save you time on low-ROI learning
- ✅ **AI-enhanced insights** (optional LLM integration with OpenAI)

---

## 📋 Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment
```bash
cp .env.example .env
# Optional: Add your OpenAI API key for enhanced AI insights
# Edit .env and set: OPENAI_API_KEY=sk-your-key-here
```

### 3. Initialize Database
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### 4. Run the App
```bash
python app.py
```
Visit: http://localhost:5000

---

## 🎯 How It Works

### Workflow
1. **Login/Register** on the platform
2. **Analyze a job**: Use the existing skill gap analyzer to compare your resume against a job description
3. **Generate coaching plan**: Click "Get Coaching Plan" (or use `/api/coach/generate` endpoint)
4. **View your plan**: See milestones, resources, and study schedule
5. **Track progress**: Mark milestones complete as you learn

### Example: From Analysis to Coaching Plan

**Step 1: Perform Skill Gap Analysis**
- Upload resume and job description
- Get: Match score (65%), missing skills (Python, Docker, AWS), strengths (Git, Linux)

**Step 2: Generate Coaching Plan**
```bash
POST /api/coach/generate
{
  "target_role": "Backend Engineer",
  "current_role": "Junior Developer",
  "experience_years": 2,
  "availability_per_week_hours": 15,
  "preferred_learning_style": "projects",
  "budget_level": "free"
}
```

**Step 3: Receive Personalized Plan**
```json
{
  "coaching_plan_id": 5,
  "human_message": "Great! You have a solid foundation. Let's close your skill gaps in Python and Docker.",
  "prioritized_path": [
    {
      "milestone_id": "m1",
      "title": "Python Mastery: Functions to OOP",
      "skills_targeted": ["python"],
      "time_estimate_weeks": 3,
      "practice_tasks": [
        {
          "task": "Build a CLI tool with 3 features",
          "acceptance_criteria": "Works without errors, documented on GitHub",
          "est_hours": 6
        }
      ],
      "resources": [
        {
          "type": "project",
          "title": "Real Python Projects",
          "url": "https://realpython.com/projects/",
          "cost": "free"
        }
      ]
    }
  ],
  "study_schedule": {
    "duration_weeks": 12,
    "weekly_plan": [
      {
        "week": 1,
        "hours": 15,
        "focus": ["python"],
        "tasks": ["Complete Python basics", "Start first project"]
      }
    ]
  },
  "next_actions_72h": [
    "Assess your Python level (30 min)",
    "Bookmark 3 resources (20 min)",
    "Set up GitHub repo & IDE (30 min)"
  ]
}
```

**Step 4: Track Progress**
```bash
POST /api/coach/5/milestone/m1/progress
{
  "task_index": 0,
  "status": "completed",
  "validation_evidence": {
    "project_link": "https://github.com/user/cli-tool",
    "code_review_feedback": "Excellent structure, well-documented"
  }
}
```

---

## 🔗 API Endpoints

### Generate Coaching Plan
```
POST /api/coach/generate
Authorization: Required (Login)

Request:
{
  "target_role": "string",              // Required
  "current_role": "string",             // Optional
  "experience_years": int,              // Default: 0
  "availability_per_week_hours": int,   // Default: 10
  "preferred_learning_style": string,   // "projects"|"videos"|"text"|"mentorship"
  "budget_level": string,               // "free"|"low"|"medium"|"high"
  "analysis_id": int                    // Optional: link to existing analysis
}

Response: 201 Created
{
  "coaching_plan_id": int,
  "human_message": string,
  "prioritized_path": [...],
  "study_schedule": {...},
  "confidence": 0.85,
  ...
}
```

### Retrieve Coaching Plan
```
GET /api/coach/<plan_id>
Authorization: Required

Response: 200 OK
{
  "id": int,
  "coaching_plan": {...},
  "progress": {
    "progress_percentage": 0,
    "completed_milestones": [],
    "total_milestones": 4
  }
}
```

### Update Milestone Progress
```
POST /api/coach/<plan_id>/milestone/<milestone_id>/progress
Authorization: Required

Request:
{
  "task_index": 0,
  "status": "completed",                // "not_started"|"in_progress"|"completed"
  "validation_evidence": {...}          // Any relevant proof of completion
}

Response: 200 OK
{
  "status": "success",
  "milestone_id": "m1",
  "progress_status": "completed"
}
```

### List All Coaching Plans
```
GET /api/coach/list
Authorization: Required

Response: 200 OK
{
  "plans": [
    {
      "id": 5,
      "target_role": "Backend Engineer",
      "summary": "You're 65% aligned...",
      "progress_percentage": 25,
      "confidence": 0.85
    }
  ]
}
```

### View Coaching Plan (Browser)
```
GET /coach/<plan_id>
```
Beautiful HTML dashboard with all details, resources, and progress tracking.

---

## 💡 Key Features

### 1. **Smart Prioritization**
- Milestones ranked by skill importance × gap size
- Adjusts timeline based on availability
- Suggests quick wins first for motivation

### 2. **Resource Curation**
- 100+ handpicked resources (courses, projects, books)
- Filters by:
  - Learning style (visual learner? → videos)
  - Budget (student? → free tier)
  - Language preferences
- Fallback generation for unrecognized skills

### 3. **Progress Validation**
- Each milestone has acceptance criteria
- Collect evidence (project links, test scores, code reviews)
- Track completion with timestamps

### 4. **Trend Detection**
- Alerts for emerging skills (AI/ML, TypeScript, Rust, etc.)
- Warns about obsolete skills (jQuery, Flash, COBOL)
- Verification signals to confirm trends

### 5. **LLM Enhancement** (Optional)
- If OpenAI API key provided: conversational, contextualized insights
- Role-specific nuances & red flags
- Confidence score adjusted accordingly
- Cost: ~$0.02 per plan generation

### 6. **12-Week Study Plan**
- Hour-by-hour allocation
- Weekly focus areas
- Realistic timelines (adjustable)
- Checkpoints for reflection

---

## 🗂️ Database Schema

### New Tables

**CoachingPlan**
```
id, analysis_id, user_id, target_role, current_role, 
experience_years, availability_per_week_hours, 
preferred_learning_style, budget_level, 
coaching_data (JSON), confidence_score, 
current_milestone_id, milestones_completed (JSON)
```

**MilestoneProgress**
```
id, coaching_plan_id, milestone_id, task_index, 
status, completion_percentage, notes, 
validation_evidence (JSON), started_at, completed_at
```

---

## 📊 Example: Full Workflow

### User: Alice (Junior Developer → Backend Engineer)

**Initial Assessment:**
- Experience: 2 years
- Available: 15 hrs/week
- Budget: Free
- Style: Projects

**Skill Gap Analysis:**
- Match Score: 58%
- Missing: Python (gap 7), Docker (gap 8), Kubernetes (gap 9)
- Strengths: JavaScript, Git, Linux basics

**Generated Plan:**

| Milestone | Duration | Focus | Top Resource |
|-----------|----------|-------|--------------|
| m1 | 3 weeks | Python advanced patterns | Real Python Projects |
| m2 | 3 weeks | Docker containerization | Official Docker docs |
| m3 | 3 weeks | Kubernetes basics | Play with Kubernetes |
| m4 | 3 weeks | Integration & practice | Capstone project |

**Week 1 Schedule:**
- Monday-Tuesday: Python async/await (5 hrs)
- Wednesday: Code review challenge (3 hrs)
- Thursday-Friday: Start mini-project (4 hrs)
- Weekend: Rest or bonus learning (3 hrs available)

**Next 72 Hours:**
1. ✅ Assess Python level on HackerRank (30 min)
2. ✅ Bookmark Real Python projects (20 min)
3. ✅ Set up GitHub repo + virtual environment (30 min)

**Expected Timeline:** 12 weeks to Backend Engineer readiness (or faster if 20+ hrs/week)

---

## 🔧 Configuration & Customization

### Learning Styles
Edit `career_coach.py` → `_get_resources_for_skill()`:
```python
type_priority = {
    "projects": ["projects", "courses", "videos"],     # Prioritize hands-on
    "videos": ["videos", "courses", "projects"],       # Prioritize visual
    "text": ["books", "articles", "courses"],          # Prioritize reading
    "mentorship": ["courses", "projects", "videos"],   # Prioritize structure
}
```

### Add Skills/Resources
```python
RESOURCE_DATABASE = {
    "rust": {
        "projects": [
            {"title": "Build CLI in Rust", "url": "...", "cost": "free"},
        ],
        "courses": [
            {"title": "Rust Book", "url": "https://doc.rust-lang.org/book/", "cost": "free"},
        ]
    }
}
```

### Add Trends
```python
EMERGING_TRENDS = [
    {
        "trend": "Web3 & Smart Contracts",
        "impact_on_roles": ["Full Stack Developer"],
        "why": "DeFi apps growing 300% YoY",
        "verification_signals": ["job-postings", "github-stars"]
    }
]
```

---

## ⚙️ Environment Variables

```bash
# Required
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
SQLALCHEMY_DATABASE_URI=sqlite:///job_analyzer.db

# Optional (for LLM enhancement)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo  # Default
```

---

## 🧪 Testing

```bash
# Run all tests
pytest test_career_coach.py -v

# Test specific feature
pytest test_career_coach.py::test_base_plan_generation -v

# With coverage
pytest test_career_coach.py --cov=career_coach
```

---

## 📚 Documentation

- **Full Guide:** See `AI_COACH_GUIDE.md`
- **API Docs:** This file + inline code comments
- **Examples:** `test_career_coach.py`

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Database not initialized | Run `db.create_all()` in Python shell |
| Missing resources for skill | Skill not in database; coach generates fallback links |
| LLM enhancement slow | LLM calls can take 3-5s; disable by not setting OPENAI_API_KEY |
| ImportError: career_coach | Ensure `career_coach.py` is in root directory |
| "Analysis not found" | Ensure analysis_id belongs to logged-in user |

---

## 🎓 Next Steps

1. **Generate your first coaching plan:** Login → Analyze job → Generate plan
2. **Track progress:** Mark milestones as complete
3. **Iterate:** Adjust availability/budget and regenerate if needed
4. **Share feedback:** Help us improve resource recommendations!

---

## 📞 Support

- **Issues:** GitHub issues
- **Questions:** Check `AI_COACH_GUIDE.md` FAQ
- **Feedback:** Email or discussions

---

**Happy learning! 🚀**

Your personalized journey to [target_role] starts now.
