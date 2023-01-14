import re

""" Extract Experiences 

"""
def extract_experiences(text):
    experience_section = re.search("(?i)experience.*?(?=education|skills|$)", text, re.DOTALL)
    if experience_section:
        return experience_section.group()
    else:
        return None
    

""" Extract Skills 

"""
def extract_skills(text):
    skills_section = re.search("(?i)skills.*?(?=experience|education|$)", text, re.DOTALL)
    if skills_section:
        return skills_section.group()
    else:
        return None
 