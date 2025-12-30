import pandas as pd
import random
from faker import Faker

fake = Faker()
num_students = 200 # Smaller dataset for better visuals

def get_skills_and_role():
    roll = random.random()
    if roll < 0.25:
        return 'System Architect', [8, 3, 9, 2, 7] # High Backend
    elif roll < 0.5:
        return 'Product Designer', [3, 9, 2, 9, 2] # High Design/Front
    elif roll < 0.75:
        return 'Data Strategist', [9, 2, 4, 1, 9] # High Data
    else:
        return 'Full Stack Engineer', [6, 7, 7, 5, 5] # Balanced

data = []
for i in range(1, num_students + 1):
    role_name, skills = get_skills_and_role()
    
    # Team Logic
    is_recruiting = random.choice([True, False, False]) # 33% chance to be a team lead
    team_name = fake.bs().title() + " Labs" if is_recruiting else "None"
    members_needed = random.randint(1, 3) if is_recruiting else 0
    looking_for = random.choice(['Frontend', 'Backend', 'Data', 'Any']) if is_recruiting else "None"

    data.append({
        'Student_ID': i,
        'Name': fake.name(),
        'Discord': f"{fake.user_name()}#{random.randint(1000,9999)}",
        'Avatar': f"https://api.dicebear.com/7.x/notionists/svg?seed={i}",
        'Role': role_name,
        'Team_Name': team_name,
        'Is_Recruiting': is_recruiting,
        'Members_Needed': members_needed,
        'Looking_For_Role': looking_for,
        'Python': skills[0], 'Frontend': skills[1], 'Backend': skills[2], 'Design': skills[3], 'SQL': skills[4],
        'Hours_Available': random.randint(5, 40)
    })

df = pd.DataFrame(data)
df.to_csv('students.csv', index=False)
print("Database updated with Team Columns.")