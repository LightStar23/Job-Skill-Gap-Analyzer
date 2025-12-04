# test_fix.py
print("🧪 Testing Import and Gap Bridge...")
print("=" * 50)

# Test 1: Check if analyzer can be imported
print("\n1. Testing import from skill_analyzer...")
try:
    from skill_analyzer import analyzer
    print("✅ SUCCESS: Imported 'analyzer' from skill_analyzer")
    print(f"   Type: {type(analyzer)}")
    print(f"   Class: {analyzer.__class__.__name__}")
except ImportError as e:
    print(f"❌ FAILED: {e}")
    print("   Make sure 'skill_analyzer.py' has 'analyzer = SkillGapAnalyzer()' at the bottom")

# Test 2: Test gap bridge database
print("\n2. Testing gap bridge database...")
try:
    import sqlite3
    conn = sqlite3.connect('skill_analyzer.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM skill_recommendations")
    count = cursor.fetchone()[0]
    conn.close()
    print(f"✅ Database has {count} skills")
except Exception as e:
    print(f"❌ Database error: {e}")
    print("   Run: python setup_database.py")

# Test 3: Test analyzer functionality
print("\n3. Testing analyzer functionality...")
try:
    test_result = analyzer.get_gap_bridge("React")
    if test_result:
        print(f"✅ Gap bridge for 'React' working:")
        print(f"   - Time: {test_result['time_required']} hours")
        print(f"   - Resources: {len(test_result['resources'])}")
        print(f"   - Projects: {len(test_result['projects'])}")
    else:
        print("❌ Gap bridge returned None")
except Exception as e:
    print(f"❌ Analyzer error: {e}")

# Test 4: Full analysis test
print("\n4. Testing full analysis...")
try:
    test_jd = "Looking for React developer with Python"
    test_resume = "I know HTML and CSS"
    results = analyzer.analyze_gap(test_jd, test_resume)
    print(f"✅ Analysis working:")
    print(f"   - Match score: {results['match_score']}%")
    print(f"   - Missing skills: {results['missing_skills']}")
    if results.get('gap_bridge_plans'):
        print(f"   - Gap bridge plans: {len(results['gap_bridge_plans'])}")
except Exception as e:
    print(f"❌ Analysis error: {e}")

print("\n" + "=" * 50)
print("🎯 Summary:")
print("- If all tests pass ✅, run: python app.py")
print("- If imports fail ❌, check skill_analyzer.py has 'analyzer = SkillGapAnalyzer()'")
print("- If database fails ❌, run: python setup_database.py")