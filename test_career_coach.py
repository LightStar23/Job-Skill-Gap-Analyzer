"""
Integration tests for AI Career Coach feature.
Run with: pytest test_career_coach.py -v
"""

import json
import pytest
from app import app, db
from models import User, CoachingPlan, MilestoneProgress
from career_coach import AICareerCoach


@pytest.fixture
def client():
    """Create Flask test client."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def test_user(client):
    """Create a test user."""
    with app.app_context():
        user = User(
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('testpass123')
        db.session.add(user)
        db.session.commit()
        return user


def test_coach_initialization():
    """Test AI Coach initializes without errors."""
    coach = AICareerCoach()
    assert coach is not None
    assert coach.RESOURCE_DATABASE is not None
    assert len(coach.EMERGING_TRENDS) > 0


def test_base_plan_generation():
    """Test rule-based coaching plan generation."""
    coach = AICareerCoach()
    
    user_profile = {
        "id": "1",
        "name": "Alice",
        "current_role": "Junior Dev",
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
    
    # Assertions
    assert "error" not in plan
    assert plan["human_message"]
    assert plan["summary"]
    assert len(plan["prioritized_path"]) > 0
    assert plan["confidence"] > 0
    assert len(plan["next_actions_72h"]) == 3
    assert plan["study_schedule"]["duration_weeks"] == 12


def test_prioritized_path_structure():
    """Test milestone structure in prioritized path."""
    coach = AICareerCoach()
    
    user_profile = {
        "id": "1",
        "name": "Bob",
        "target_role": "ML Engineer",
        "experience_years": 1,
        "availability_per_week_hours": 15,
        "preferred_learning_style": "videos",
        "budget_level": "medium",
    }
    
    skill_gap = {
        "score": 30,
        "gaps": [
            {"skill": "machine learning", "importance": 0.95, "current_level": 1, "gap": 9},
        ],
        "strengths": []
    }
    
    plan = coach.generate_coaching_plan(user_profile, skill_gap)
    milestone = plan["prioritized_path"][0]
    
    # Check milestone structure
    assert milestone["milestone_id"]
    assert milestone["title"]
    assert milestone["skills_targeted"]
    assert milestone["why"]
    assert milestone["time_estimate_weeks"] > 0
    assert len(milestone["practice_tasks"]) > 0
    assert len(milestone["resources"]) > 0
    assert "metric" in milestone["validation"]


def test_obsolete_skills_detection():
    """Test detection of obsolete skills."""
    coach = AICareerCoach()
    
    user_profile = {
        "target_role": "Frontend Developer",
        "experience_years": 5,
        "availability_per_week_hours": 10,
        "preferred_learning_style": "projects",
        "budget_level": "free",
    }
    
    skill_gap = {
        "score": 40,
        "gaps": [
            {"skill": "jquery", "importance": 0.3, "current_level": 8, "gap": 1},
            {"skill": "react", "importance": 0.95, "current_level": 2, "gap": 8},
        ],
        "strengths": ["javascript"]
    }
    
    plan = coach.generate_coaching_plan(user_profile, skill_gap)
    
    # jQuery should be flagged as obsolete
    obsolete = plan["obsolete_skills"]
    assert len(obsolete) > 0
    assert any(obs["skill"].lower() == "jquery" for obs in obsolete)


def test_emerging_trends_for_role():
    """Test emerging trends are returned for relevant roles."""
    coach = AICareerCoach()
    
    user_profile = {
        "target_role": "Backend Developer",
        "experience_years": 3,
        "availability_per_week_hours": 10,
        "preferred_learning_style": "projects",
        "budget_level": "free",
    }
    
    skill_gap = {
        "score": 60,
        "gaps": [],
        "strengths": ["python", "django"]
    }
    
    plan = coach.generate_coaching_plan(user_profile, skill_gap)
    trends = plan["emerging_trends"]
    
    assert len(trends) > 0
    for trend in trends:
        assert "trend" in trend
        assert "impact_on_role" in trend
        assert "why" in trend
        assert "verification_signals" in trend


def test_progress_tracking():
    """Test milestone progress calculation."""
    coach = AICareerCoach()
    
    coaching_data = {
        "prioritized_path": [
            {"milestone_id": "m1"},
            {"milestone_id": "m2"},
            {"milestone_id": "m3"},
        ]
    }
    
    # No completed milestones
    progress = coach.calculate_overall_progress(coaching_data, [])
    assert progress["progress_percentage"] == 0
    assert progress["total_milestones"] == 3
    
    # 2 completed milestones
    progress = coach.calculate_overall_progress(coaching_data, ["m1", "m2"])
    assert progress["progress_percentage"] == 66  # 2/3 * 100
    assert progress["completed_milestones"] == ["m1", "m2"]
    
    # All completed
    progress = coach.calculate_overall_progress(coaching_data, ["m1", "m2", "m3"])
    assert progress["progress_percentage"] == 100


def test_api_generate_coaching_plan(client, test_user):
    """Test /api/coach/generate endpoint."""
    # Login first
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    response = client.post('/api/coach/generate', 
        json={
            "target_role": "Data Scientist",
            "current_role": "Analyst",
            "experience_years": 4,
            "availability_per_week_hours": 12,
            "preferred_learning_style": "projects",
            "budget_level": "medium",
        }
    )
    
    assert response.status_code == 201
    data = response.get_json()
    assert "coaching_plan_id" in data
    assert "human_message" in data
    assert "prioritized_path" in data


def test_api_missing_target_role(client, test_user):
    """Test error handling when target_role is missing."""
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    response = client.post('/api/coach/generate', 
        json={
            "current_role": "Developer",
            # Missing target_role
        }
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_study_schedule_structure():
    """Test study schedule structure and completeness."""
    coach = AICareerCoach()
    
    user_profile = {
        "target_role": "DevOps Engineer",
        "experience_years": 3,
        "availability_per_week_hours": 20,
        "preferred_learning_style": "projects",
        "budget_level": "free",
    }
    
    skill_gap = {
        "score": 50,
        "gaps": [
            {"skill": "kubernetes", "importance": 0.9, "current_level": 2, "gap": 8},
        ],
        "strengths": ["docker"]
    }
    
    plan = coach.generate_coaching_plan(user_profile, skill_gap)
    schedule = plan["study_schedule"]
    
    assert schedule["duration_weeks"] == 12
    assert len(schedule["weekly_plan"]) == 12
    
    for week_plan in schedule["weekly_plan"]:
        assert "week" in week_plan
        assert "hours" in week_plan
        assert "focus" in week_plan
        assert "tasks" in week_plan
        assert week_plan["hours"] == 20  # Should match availability


def test_resource_filtering_by_budget():
    """Test resources are filtered by budget level."""
    coach = AICareerCoach()
    
    # Free budget
    resources_free = coach._get_resources_for_skill("python", "projects", "free")
    for res in resources_free:
        assert res["cost"] == "free", f"Expected free but got {res['cost']}"
    
    # Medium budget (can have paid)
    resources_medium = coach._get_resources_for_skill("python", "projects", "medium")
    assert len(resources_medium) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
