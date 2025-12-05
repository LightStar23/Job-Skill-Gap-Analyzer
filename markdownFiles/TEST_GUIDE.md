# 🚀 Quick Test Guide - AI Career Coach Features

## ✅ App is Running!

Visit: **http://localhost:5000**

---

## 📋 Test Workflow (5 minutes)

### Step 1: Create Account
1. Click **"Register"**
2. Enter:
   - Email: `test@example.com`
   - First Name: `John`
   - Last Name: `Doe`
   - Password: `testpass123`
   - Confirm: `testpass123`
3. Click **"Register"**

### Step 2: Login
1. Enter email: `test@example.com`
2. Enter password: `testpass123`
3. Click **"Login"**

### Step 3: Analyze a Job (Original Feature)
1. Click **"Analyze New Job"** on dashboard
2. Copy-paste this Job Description:
```
We're hiring a Backend Engineer with 3+ years experience.
Required: Python, Django, REST APIs, PostgreSQL, Docker, Git
Nice-to-have: Kubernetes, AWS, Redis, GraphQL
```
3. Copy-paste this Resume:
```
Senior Software Developer with 5 years experience.
Expert in Python and JavaScript. 
Proficient in Flask, REST API development, SQL, Git.
Some experience with Docker. Familiar with Linux and Bash.
Knowledge of AWS basics and CI/CD pipelines.
```
4. Enter:
   - Job Title: `Backend Engineer`
   - Company: `TechCorp`
5. Click **"Analyze"**

### Step 4: View Skill Gap Results
You'll see:
- ✅ **Match Score:** ~65%
- ✅ **Matching Skills:** Python, REST API, Git, etc.
- ✅ **Missing Skills:** Django, PostgreSQL, Docker, Kubernetes, AWS
- ✅ **Categorized Gaps:** By skill category

### Step 5: 🎯 Generate Coaching Plan (NEW!)
1. Look for **"Get Coaching Plan"** button
2. Fill in profile:
   - **Target Role:** Backend Engineer
   - **Current Role:** Senior Developer
   - **Experience:** 5 years
   - **Hours/Week:** 15
   - **Learning Style:** Projects
   - **Budget:** Free
3. Click **"Generate Plan"**

### Step 6: View Your Personalized Coaching Plan (NEW!)
You'll see a beautiful dashboard with:

#### 📊 Progress
- Overall completion percentage
- Milestones completed

#### 💬 Coach's Message
- Personalized greeting from AI Coach
- Summary of your situation

#### 📚 Prioritized Learning Path
Accordion with milestones (e.g., "m1", "m2", "m3"):
- **Milestone title** (e.g., "Python Mastery")
- **Why it matters** for your target role
- **Time estimate** (e.g., 3 weeks)
- **Practice tasks** with acceptance criteria
- **Curated resources**
  - Type: Project, Course, Video, etc.
  - Title: Resource name
  - Cost: Free or Paid
  - Link: Clickable URL

#### ⚠️ Obsolete Skills
If your analysis mentions outdated skills:
- Shows which skills to avoid
- Suggests modern alternatives

#### 🚀 Emerging Trends
Shows opportunities:
- AI/ML Integration in Backend
- TypeScript adoption
- Serverless computing
- etc.

#### 📅 Study Schedule
12-week plan:
- Week 1-3: Focus on Python, 15 hrs/week
- Week 4-6: Focus on Django & Databases
- etc.

#### 🎯 Next Actions (72 hours)
3 immediate micro-tasks:
1. Assess your Python level (30 min)
2. Bookmark resources (20 min)
3. Setup GitHub repo (30 min)

#### 📈 Progress Tracking
- **Confidence Score:** 0.85 (85%)
- **Explanation:** Why this plan was created

---

## 🧪 Run Tests

```bash
cd C:\Users\HP\Job-Skill-Gap-Analyzer
pytest test_career_coach.py -v
```

Expected: **12 tests pass**

---

## 📡 Test API Endpoints (Advanced)

### Test Generate Coaching Plan
```bash
curl -X POST http://localhost:5000/api/coach/generate \
  -H "Content-Type: application/json" \
  -d '{
    "target_role": "ML Engineer",
    "current_role": "Data Analyst",
    "experience_years": 3,
    "availability_per_week_hours": 20,
    "preferred_learning_style": "projects",
    "budget_level": "free"
  }'
```

### List All Plans
```bash
curl http://localhost:5000/api/coach/list
```

### View Single Plan
```bash
curl http://localhost:5000/api/coach/1
```

---

## 🎯 What to Check

### ✅ Core Features to Verify

1. **Skill Gap Analysis** (Original)
   - [ ] Extracts skills from JD & resume
   - [ ] Calculates match score
   - [ ] Shows missing skills

2. **Coaching Plan Generation** (NEW!)
   - [ ] Creates personalized 12-week plan
   - [ ] Prioritizes by importance & gap size
   - [ ] Includes practice tasks

3. **Resource Curation** (NEW!)
   - [ ] Shows 3-5 resources per milestone
   - [ ] Filtered by budget (free)
   - [ ] Filtered by style (projects)
   - [ ] Has correct type (project/course/video)

4. **Trend Detection** (NEW!)
   - [ ] Shows emerging trends
   - [ ] Shows why trends matter
   - [ ] Provides verification signals

5. **Obsolete Skills** (NEW!)
   - [ ] Warns about outdated skills
   - [ ] Suggests replacements

6. **Progress Tracking** (NEW!)
   - [ ] Can mark milestones complete
   - [ ] Shows progress percentage
   - [ ] Calculates next milestone

---

## 💡 Key Features to Test

### Feature 1: Smart Prioritization
- Milestones ordered by: (Importance × Gap Size)
- Top gap (Django) = highest priority
- Should take ~3 weeks per milestone

### Feature 2: Resource Filtering
Try different learning styles:
- **projects:** See GitHub projects first
- **videos:** See YouTube courses first
- **text:** See articles & books first

### Feature 3: LLM Enhancement (Optional)
If you set `OPENAI_API_KEY` in `.env`:
- Plan gets more personalized insights
- Confidence score increases ~15%
- Takes 3-5 seconds longer

### Feature 4: 72-Hour Actions
Quick micro-tasks to start immediately:
- Assessment (30 min)
- Bookmark resources (20 min)
- Setup environment (30 min)

### Feature 5: Study Schedule
12 weeks with:
- Realistic hour allocation per week
- Focus areas per week
- Milestone progression

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| **404 Not Found** | App not running. Run `python app.py` |
| **Database locked** | Delete `instance/job_analyzer.db` and restart |
| **No resources shown** | Check budget filter; all "free" resources selected |
| **Plan takes too long** | LLM call in progress (3-5s). Set OPENAI_API_KEY="" to disable |
| **ModuleNotFoundError** | Run `pip install -r requirements.txt` |

---

## 📝 Sample Data

### Job Description
```
Backend Software Engineer

Company: TechCorp Solutions
Location: Remote

We're looking for a talented Backend Engineer to join our growing team.

Requirements:
- 3+ years professional experience with Python
- Strong understanding of databases (PostgreSQL/MySQL)
- Experience with Django or Flask
- RESTful API design and development
- Git version control
- Docker containerization basics

Nice-to-have:
- Kubernetes experience
- AWS/GCP cloud experience
- GraphQL knowledge
- Redis caching
- Microservices architecture
- CI/CD pipelines

You should be:
- A problem solver
- Communicative
- Ready to mentor juniors
```

### Resume
```
JOHN DOE
john@example.com | 555-1234 | linkedin.com/in/johndoe

EXPERIENCE:
Senior Developer | 5 years
- Built APIs in Python (Flask)
- SQL database optimization
- Implemented CI/CD pipelines
- Git workflow management
- Some Docker experience
- Basic AWS knowledge

Skills: Python, Flask, JavaScript, SQL, Git, Linux, Bash

EDUCATION:
BS Computer Science
```

---

## 🎓 What You'll Learn

This test demonstrates:
1. ✅ Skill gap analysis (existing)
2. ✅ AI-powered coaching (new)
3. ✅ Smart prioritization (new)
4. ✅ Resource curation (new)
5. ✅ Progress tracking (new)
6. ✅ Emerging trends (new)
7. ✅ Personalization (new)

---

## 📚 Documentation Reference

- **QUICKSTART.md** - Fast setup
- **AI_COACH_GUIDE.md** - Complete reference
- **AI_COACH_README.md** - Feature overview
- **test_career_coach.py** - Code examples

---

## ✨ Next Steps

After testing:
1. **Review** the generated plans
2. **Provide feedback** on resources
3. **Customize** skill database (add your own)
4. **Deploy** to production

---

**Happy testing! 🚀**
