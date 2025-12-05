# AI Career Coach Integration Guide

## Overview

The **AI Career Coach** is a personalized learning path generator that analyzes skill gaps and creates actionable coaching plans tailored to each learner's profile. It combines:

- **LLM Intelligence** (OpenAI GPT-3.5+) for conversational, context-aware recommendations
- **Rule-Based Fallback** when LLM is unavailable (cost-free, always works)
- **Curated Resource Database** for projects, courses, videos, and books
- **Trend Detection** for emerging tech skills and career trajectories
- **Progress Tracking** with milestone validation and evidence collection

---

## Architecture

### Components

#### 1. **career_coach.py** - Core AI Coach Engine
- `AICareerCoach` class: Main orchestrator
- `generate_coaching_plan()`: Creates personalized plans from user profile + skill gaps
- `update_milestone_progress()`: Tracks learning progress
- `calculate_overall_progress()`: Computes completion %, next milestone, ETA

**Key Methods:**
- `_build_base_plan()`: Rule-based planning (skill prioritization, task generation, resource curation)
- `_enhance_with_llm()`: Optional LLM enhancement for deeper personalization
- `_generate_human_message()`: Coach's conversational opening
- `_build_prioritized_path()`: Creates learning milestones with practice tasks
- `_build_study_schedule()`: 12-week weekly schedule with hours allocated

#### 2. **Database Models** (models.py)
- `CoachingPlan`: Stores generated coaching plans with metadata
- `MilestoneProgress`: Tracks per-task/per-milestone progress
- Links to `Analysis` (skill gap results) and `User`

#### 3. **Flask Endpoints** (app.py)
- `POST /api/coach/generate`: Create new coaching plan
- `GET /api/coach/<plan_id>`: Retrieve saved plan
- `POST /api/coach/<plan_id>/milestone/<milestone_id>/progress`: Update milestone status
- `GET /api/coach/list`: List all user's coaching plans
- `GET /coach/<plan_id>`: View plan in browser (renders coach_plan.html)

#### 4. **UI Template** (templates/coach_plan.html)
- Interactive coaching plan display
- Milestone accordion with resources
- Weekly schedule table
- Progress tracker
- Trend alerts and obsolete skill warnings

---

## Usage

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables** (.env):
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key (optional)
   OPENAI_API_KEY=sk-your-key-here
   ```

3. **Initialize database:**
   ```bash
   python
   >>> from app import app, db
   >>> with app.app_context():
   ...     db.create_all()
   ```

4. **Run the app:**
   ```bash
   python app.py
   ```

### API Usage Examples

#### Generate a Coaching Plan

**Request:**
```bash
curl -X POST http://localhost:5000/api/coach/generate \
  -H "Content-Type: application/json" \
  -d '{
    "target_role": "Machine Learning Engineer",
    "current_role": "Software Developer",
    "experience_years": 3,
    "availability_per_week_hours": 15,
    "preferred_learning_style": "projects",
    "budget_level": "medium",
    "analysis_id": 1
  }'
```

**Response (JSON):**
```json
{
  "coaching_plan_id": 5,
  "human_message": "Great news! You're well-positioned for ML Engineer...",
  "summary": "You're 65% aligned. Focus: master machine learning algorithms. Timeline: 12 weeks.",
  "prioritized_path": [
    {
      "milestone_id": "m1",
      "title": "ML Fundamentals: Data → Predictions",
      "skills_targeted": ["machine learning"],
      "why": "High priority for ML Engineer: 80% importance, current level 3/10",
      "time_estimate_weeks": 3,
      "practice_tasks": [
        {
          "task": "Build Iris classifier",
          "acceptance_criteria": ">90% accuracy on test set",
          "est_hours": 6
        }
      ],
      "resources": [
        {
          "type": "course",
          "title": "Andrew Ng's ML Course",
          "url": "https://www.coursera.org/learn/machine-learning",
          "cost": "free"
        }
      ],
      "validation": {
        "metric": "Kaggle competition or project",
        "threshold": "Model >85% accuracy, blog post written"
      }
    }
  ],
  "obsolete_skills": [],
  "emerging_trends": [
    {
      "trend": "AI/ML Integration in Backend",
      "impact_on_role": "increase",
      "why": "LLMs and ML are becoming standard in modern applications",
      "verification_signals": ["job-posting-trend", "github-stars"]
    }
  ],
  "study_schedule": {
    "duration_weeks": 12,
    "weekly_plan": [
      {
        "week": 1,
        "hours": 15,
        "focus": ["machine learning"],
        "tasks": ["Complete beginner tutorial on machine learning", "Build small project using machine learning"]
      }
    ]
  },
  "next_actions_72h": [
    "Assess your current machine learning level: complete free online quiz or do a quick code challenge (30 min)",
    "Find and bookmark 3 recommended resources for your top priority skill (20 min)",
    "Set up learning environment: GitHub repo, IDE, learning tracker (30 min)"
  ],
  "confidence": 0.85,
  "explainability": "...",
  "tracking_hooks": {
    "progress_metric_ids": ["metric_0", "metric_1"],
    "suggested_check_in_frequency_days": 7
  }
}
```

#### Retrieve a Coaching Plan

```bash
curl http://localhost:5000/api/coach/5 \
  -H "Authorization: Bearer <token>"
```

#### Update Milestone Progress

```bash
curl -X POST http://localhost:5000/api/coach/5/milestone/m1/progress \
  -H "Content-Type: application/json" \
  -d '{
    "task_index": 0,
    "status": "completed",
    "validation_evidence": {
      "project_link": "https://github.com/user/iris-classifier",
      "test_score": 92
    }
  }'
```

---

## Configuration

### Learning Styles
- **"projects"**: Emphasizes hands-on GitHub projects and Kaggle competitions
- **"videos"**: Prioritizes YouTube tutorials and video courses
- **"text"**: Focuses on blogs, articles, and books
- **"mentorship"**: Recommends structured courses and communities

### Budget Levels
- **"free"**: Only free resources (YouTube, GitHub, official docs, Coursera free tier)
- **"low"**: ~$10-50 resources (Udemy sales, single courses)
- **"medium"**: ~$50-200 (subscription services, multiple courses)
- **"high"**: Premium resources (bootcamps, personalized coaching)

### Emerging Trends Tracked
- **AI/ML Integration** (increase impact)
- **TypeScript over JavaScript** (increase impact)
- **Rust for Systems** (increase impact)
- **Serverless & Edge Computing** (increase impact)
- **LLM Prompt Engineering** (increase impact)

### Obsolete Skills Detected
- jQuery → Modern frameworks
- Flash → HTML5/Canvas
- COBOL → Python/Java
- Silverlight → React/ASP.NET
- Perl → Python/Bash

---

## LLM Integration (Optional)

### With OpenAI API

If `OPENAI_API_KEY` is set, the coach will enhance generated plans with:
- Personalized narrative insights
- Role-specific nuances
- Timeline adjustments based on context
- Red flag warnings (e.g., "Your experience in X aligns well, but Y is missing for this role")

**Cost:** ~$0.01-0.05 per plan generation (gpt-3.5-turbo)

### Without OpenAI API

Coach operates in **rule-based mode**:
- Still generates structured, prioritized plans
- Applies heuristics for time estimation
- Curates resources from embedded database
- Confidence score slightly lower (~0.65 vs ~0.85)

---

## Database Schema

### CoachingPlan Table
```
id (int, PK)
analysis_id (int, FK to Analysis) - optional link
user_id (int, FK to User)
target_role (str)
current_role (str)
experience_years (int)
availability_per_week_hours (int)
preferred_learning_style (str)
budget_level (str)
coaching_data (JSON) - Full coaching plan JSON
confidence_score (float, 0-1)
current_milestone_id (str, e.g., "m1")
milestones_completed (JSON array) - ["m1", "m2"]
created_at (datetime)
updated_at (datetime)
```

### MilestoneProgress Table
```
id (int, PK)
coaching_plan_id (int, FK)
milestone_id (str)
task_index (int)
status (str) - "not_started", "in_progress", "completed"
completion_percentage (int, 0-100)
notes (text)
validation_evidence (JSON) - {"project_link": "...", "test_score": 85}
started_at (datetime)
completed_at (datetime)
created_at (datetime)
updated_at (datetime)
```

---

## Extending the Coach

### Add Custom Resources

Edit `RESOURCE_DATABASE` in `career_coach.py`:

```python
"kubernetes": {
    "projects": [
        {"title": "Deploy Microservices on K8s", "url": "...", "cost": "free"},
    ],
    "courses": [
        {"title": "Linux Academy Kubernetes", "url": "...", "cost": "paid"},
    ]
}
```

### Add Trends

Edit `EMERGING_TRENDS`:

```python
{
    "trend": "Web3 & Blockchain",
    "impact_on_roles": ["Full Stack Developer", "Smart Contract Engineer"],
    "why": "Decentralized apps are new frontier",
    "verification_signals": ["github-stars", "job-postings", "conference-talks"]
}
```

### Add Obsolete Skills

Edit `OBSOLETE_SKILLS`:

```python
"adobe_flash": {
    "reason": "Deprecated in 2021; browsers no longer support",
    "suggested_alternatives": ["HTML5", "WebGL", "Canvas"]
}
```

### Customize Practice Tasks

Modify `_generate_practice_tasks()` to add role-specific tasks.

---

## Testing

### Test Coaching Plan Generation

```python
from career_coach import AICareerCoach

coach = AICareerCoach()

user_profile = {
    "id": "test-1",
    "name": "Alice",
    "current_role": "Junior Developer",
    "target_role": "Backend Engineer",
    "experience_years": 2,
    "availability_per_week_hours": 10,
    "preferred_learning_style": "projects",
    "budget_level": "free",
}

skill_gap = {
    "score": 55,
    "gaps": [
        {"skill": "python", "importance": 0.9, "current_level": 4, "gap": 6},
        {"skill": "docker", "importance": 0.8, "current_level": 1, "gap": 9},
    ],
    "strengths": ["javascript", "git"]
}

plan = coach.generate_coaching_plan(user_profile, skill_gap)
print(json.dumps(plan, indent=2))
```

---

## FAQ

**Q: Can the coach work without OpenAI?**
A: Yes! Rule-based mode works perfectly. LLM is optional for richer personalization.

**Q: How are milestones prioritized?**
A: By skill importance weight × gap size, then by frequency in job postings for the target role.

**Q: Can users track progress?**
A: Yes, via `MilestoneProgress` table and the dashboard UI. Completion % updates as milestones are marked done.

**Q: What if a skill isn't in the resource database?**
A: Coach generates fallback resources (generic Udemy/GitHub links).

**Q: How long is the typical plan?**
A: Fixed at 12 weeks, but users can complete faster/slower. Adjust availability_per_week_hours to compress timeline.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "OpenAI API error" | Check `OPENAI_API_KEY` in .env; ensure it's valid and has quota |
| "No resources found for skill" | Add skill to `RESOURCE_DATABASE` or coach generates fallbacks |
| "Database integrity error" | Run `db.create_all()` to initialize missing tables |
| "Coach takes >5s to generate" | Likely LLM call; use rule-based mode or check network |

---

## Future Enhancements

- [ ] Real-time progress notifications (Slack/Email)
- [ ] Peer accountability groups
- [ ] Weekly check-in emails with micro-quizzes
- [ ] Dynamic resource recommendations based on user feedback
- [ ] Integration with job boards (e.g., fetch trending skills from LinkedIn)
- [ ] Multi-language support for global learners
- [ ] Interactive mentor matching
- [ ] Certification tracking

---

## Support

For issues, questions, or feature requests, open a GitHub issue or contact the development team.

Happy learning! 🚀
