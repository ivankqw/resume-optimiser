import requests
from os import environ
from dotenv import load_dotenv 
import re

load_dotenv()
api_key = environ.get('OPENAI_KEY')

# GPT-3 endpoint
url = "https://api.openai.com/v1/completions"

"""get_gpt3_response
Makes a POST request to the Open AI GPT3 Completions Endpoint 
"""

def get_gpt3_response(prompt="", api_key="", model="text-davinci-003", top_p=1, max_tokens=1000):
    payload = {
        "model": model,
        "prompt": prompt,
        "top_p": top_p,
        "max_tokens": max_tokens
    }

    # Make the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.post(url, json=payload, headers=headers)

    # Print the response
    if response.status_code == 200:
        response_json = response.json()
        generated_text = response_json["choices"][0]["text"]
        return generated_text
    else:
        print(f"Error: {response.text}")
    return ""


""" get_keywords
Extract keywords from a job description 
"""

def get_keywords(jd_input):
    jd_prompt = (
        "Extract the keywords from the following text:" + 
        jd_input + 
        "Keywords:"
    )
    return get_gpt3_response(jd_prompt, api_key)

""" keywords_to_list
Parse keywords into list with whitespaces removed
"""
def keywords_to_list(keywords):
    return [word.strip() for word in get_keywords(keywords).split(",")]

""" get_resume_prompt
Get Resume Prompt by different sections
"""

def get_resume_prompt(jd_keywords, section_type, section, boost_score):
    return f'Please try to add the following keywords: {jd_keywords} to this extract of the \
        {section_type} section of the following resume: {section}. Do not change the format and any of the original text \
            while making the resulting text seem believable:'

""" rewrite_resume
Rewrite a resume using extracted keywords
Takes in parsed_resume dict object 
Returns string 
"""

def rewrite_resume(parsed_resume, jd_keywords, boost_score): 
    experience = parsed_resume.get("experience")
    skills = parsed_resume.get("skills")
    projects = parsed_resume.get("projects")
    new_experience = get_gpt3_response(get_resume_prompt(jd_keywords, "experience", experience, boost_score), api_key)
    new_skills = get_gpt3_response(get_resume_prompt(jd_keywords, "skills", skills, boost_score), api_key)
    new_projects = get_gpt3_response(get_resume_prompt(jd_keywords, "projects", projects, boost_score), api_key)
    
    x= new_experience.count('.')
    #Replace opening \n
    new_experience= new_experience.replace('\n\n','',1)
    new_experience = re.sub(r'(?<!\n)\n(?=\n|$)', '\n\n', new_experience)
    
    y= new_projects.count('.')
    #Replace opening \n
    # new_projects= new_projects.replace('\n\n','\n\u2022',1)
    new_projects = re.sub(r'(?<!\n)\n(?=\n|$)', '\n\n', new_projects)

    d = {}
    d['experience'] = new_experience
    d['skills'] = new_skills
    d['projects'] = new_projects
    
    return d