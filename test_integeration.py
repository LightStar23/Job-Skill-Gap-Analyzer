# test_integration.py
from setup_database import get_skill_bridge

# Simulate your analyzer finding missing skills
missing_skills = ['React', 'Python', 'MongoDB']  # Example

print("🔍 Skill Gap Bridge Analysis")
print("=" * 40)

for skill in missing_skills:
    plan = get_skill_bridge(skill)
    if plan:
        print(f"\n📚 {skill}:")
        print(f"   ⏱️  {plan['time_to_beginner']} hours to beginner level")
        print(f"   📖 {len(plan['free_resources'])} free resources available")
        
        if plan['project_ideas']:
            print(f"   💻 Project: {plan['project_ideas'][0]['title']}")
    else:
        print(f"\n⚠️  {skill}: No gap bridge data yet (add it to database!)")

print("\n" + "=" * 40)
print("✅ Gap bridge generator is ready!")