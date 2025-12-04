# app.py - MINIMAL WORKING VERSION
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, bcrypt, User, Analysis
from skill_analyzer import analyzer  # This imports the 'analyzer' variable
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_analyzer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Basic validation
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's recent analyses
    recent_analyses = Analysis.query.filter_by(user_id=current_user.id)\
        .order_by(Analysis.created_at.desc())\
        .limit(5)\
        .all()
    return render_template('dashboard.html', analyses=recent_analyses)

@app.route('/analyze', methods=['POST'])
@login_required
def analyze():
    try:
        job_description = request.form.get('job_description', '')
        resume_text = request.form.get('resume_text', '')
        job_title = request.form.get('job_title', 'Untitled Position')
        company = request.form.get('company', '')
        
        if not job_description or not resume_text:
            return jsonify({'error': 'Please provide both job description and resume text'})
        
        # Perform analysis - analyzer.analyze_gap() now returns gap bridge plans too
        results = analyzer.analyze_gap(job_description, resume_text)
        
        # Save analysis to database
        analysis = Analysis(
            user_id=current_user.id,
            job_title=job_title,
            company=company,
            job_description=job_description,
            resume_text=resume_text,
            match_score=results['match_score'],
            analysis_results=json.dumps(results)  # Now includes gap_bridge_plans
        )
        db.session.add(analysis)
        db.session.commit()
        
        results['analysis_id'] = analysis.id
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'})

@app.route('/analysis/<int:analysis_id>')
@login_required
def view_analysis(analysis_id):
    analysis = Analysis.query.filter_by(id=analysis_id, user_id=current_user.id).first_or_404()
    results = json.loads(analysis.analysis_results)
    return render_template('analysis_detail.html', analysis=analysis, results=results)

@app.route('/analyze/new')
@login_required
def analyze_page():
    return render_template('analyze.html')

# Initialize database
with app.app_context():
    db.create_all()
    print("✅ Main database tables created")

if __name__ == '__main__':
    app.run(debug=True)