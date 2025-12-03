# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to analysis history
    analyses = db.relationship('Analysis', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200))
    job_description = db.Column(db.Text, nullable=False)
    resume_text = db.Column(db.Text, nullable=False)
    match_score = db.Column(db.Float, nullable=False)
    analysis_results = db.Column(db.Text)  # JSON string of full results
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to coaching plan
    coaching_plan = db.relationship('CoachingPlan', backref='analysis', uselist=False, lazy=True)

class CoachingPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target_role = db.Column(db.String(200), nullable=False)
    current_role = db.Column(db.String(200))
    experience_years = db.Column(db.Integer, default=0)
    availability_per_week_hours = db.Column(db.Integer, default=10)
    preferred_learning_style = db.Column(db.String(50), default='projects')  # projects, videos, text, mentorship
    budget_level = db.Column(db.String(20), default='free')  # free, low, medium, high
    
    # Coaching plan data (JSON)
    coaching_data = db.Column(db.Text)  # Full JSON coaching plan from AI Coach
    confidence_score = db.Column(db.Float, default=0.0)  # 0-1 confidence in recommendations
    
    # Progress tracking
    current_milestone_id = db.Column(db.String(50))  # e.g., "m1", "m2"
    completion_percentage = db.Column(db.Integer, default=0)  # 0-100
    milestones_completed = db.Column(db.Text)  # JSON array of completed milestone IDs
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to user
    user = db.relationship('User', backref='coaching_plans')

class MilestoneProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coaching_plan_id = db.Column(db.Integer, db.ForeignKey('coaching_plan.id'), nullable=False)
    milestone_id = db.Column(db.String(50), nullable=False)  # e.g., "m1", "m2"
    task_index = db.Column(db.Integer)  # Index of practice task within milestone
    
    status = db.Column(db.String(20), default='not_started')  # not_started, in_progress, completed
    completion_percentage = db.Column(db.Integer, default=0)  # 0-100
    notes = db.Column(db.Text)  # User notes on progress
    validation_evidence = db.Column(db.Text)  # JSON: e.g., {"project_link": "...", "test_score": 85}
    
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)