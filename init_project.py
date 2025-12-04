# init_project.py
import subprocess
import sys

def init_project():
    print("🚀 Initializing Job Skill Gap Analyzer with Gap Bridge...")
    print("=" * 60)
    
    # Step 1: Setup gap bridge database
    print("\n📊 Setting up gap bridge database...")
    try:
        import setup_database
        setup_database.setup_database()
        print("✅ Gap bridge database setup complete!")
    except Exception as e:
        print(f"❌ Error setting up gap bridge database: {e}")
    
    # Step 2: Create main app database tables
    print("\n📝 Creating main application database...")
    try:
        # Import and create tables
        from app import app, db
        with app.app_context():
            db.create_all()
            print("✅ Main database tables created!")
    except Exception as e:
        print(f"❌ Error creating main database: {e}")
        print("Note: If you're seeing 'no module named...', make sure to install dependencies first.")
        print("Run: pip install -r requirements.txt")
    
    print("\n" + "=" * 60)
    print("🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Run: python app.py")
    print("2. Open browser to: http://localhost:5000")
    print("3. Register/Login and test the analyzer")
    print("\nTo test gap bridge:")
    print("- Enter a job description requiring 'React' or 'Python'")
    print("- Check the 'Personalized Learning Plans' section in results")

if __name__ == '__main__':
    init_project()