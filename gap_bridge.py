# gap_bridge.py - NEW SIMPLIFIED VERSION
import sqlite3
import json

def get_gap_bridge_connection():
    """Get connection to skill_analyzer.db"""
    conn = sqlite3.connect('skill_analyzer.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_skill_bridge(skill_name):
    """Get gap bridge data for a specific skill"""
    conn = get_gap_bridge_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM skill_recommendations WHERE skill_name = ?", 
        (skill_name,)
    )
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'skill_name': row['skill_name'],
            'category': row['category'],
            'free_resources': json.loads(row['free_resources']) if row['free_resources'] else [],
            'project_ideas': json.loads(row['project_ideas']) if row['project_ideas'] else [],
            'time_to_beginner': row['time_to_beginner']
        }
    return None

def generate_gap_bridge_plans(missing_skills):
    """Generate gap bridge plans for missing skills"""
    plans = []
    
    for skill in missing_skills:
        bridge_data = get_skill_bridge(skill)
        if bridge_data:
            plan = {
                'skill': skill,
                'resources': bridge_data['free_resources'][:3],
                'projects': bridge_data['project_ideas'][:2],
                'time_required': bridge_data['time_to_beginner'],
                'weekly_hours': 5,
                'weeks_needed': round(bridge_data['time_to_beginner'] / 5, 1)
            }
            plans.append(plan)
    
    return plans