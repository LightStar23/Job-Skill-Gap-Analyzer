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

# New Modifications
# models.py - ADD THESE NEW MODELS AT THE BOTTOM
class SkillRecommendation(db.Model):
    """Skill recommendations for gap bridge"""
    __tablename__ = 'skill_recommendations'
    __bind_key__ = 'skill_analyzer'  # Use different database
    
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    free_resources = db.Column(db.Text)  # JSON stored as Text
    project_ideas = db.Column(db.Text)   # JSON stored as Text
    time_to_beginner = db.Column(db.Integer, default=20)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserLearningPlan(db.Model):
    """User's saved learning plans"""
    __tablename__ = 'user_learning_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    selected_resources = db.Column(db.Text)  # JSON stored as Text
    selected_projects = db.Column(db.Text)   # JSON stored as Text
    current_progress = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='not_started')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('learning_plans', lazy=True))

# Add this relationship to User class
# In the User class, add:
# learning_plans = db.relationship('UserLearningPlan', backref='user_rel', lazy=True)