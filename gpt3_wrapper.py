import requests
from os import environ
from dotenv import load_dotenv 

load_dotenv()
api_key = environ.get('OPENAI_KEY')

# GPT-3 endpoint
url = "https://api.openai.com/v1/completions"

"""
jd_input = 
Responsibilities

Build Machine Learning models to respond to and mitigate risks in Global Payments products;
Improve modelling infrastructures, labels, features and algorithms towards improving robustness, automation and generalisation, as well as, reduce modelling and operational load on risk adversaries and new product/risk ramping-ups;
Level up the risk Machine Learning expertise excellence in domain areas such as privacy/compliance, interoperability, risk perception, analysis, etc;

Qualifications

Bachelor degree or above in Computer Science, Statistics, Mathematics or other related majors;
Proficient in Python, Java or Scala and big data tools such as SQL / Hive / Spark, etc;
3 years and above of Machine Learning experience, preferably with domain experiences in Trust & Safety, Risk management, Anti Fraud;
Domain experiences in one of these fields is preferred: trust and safety, risk management, fraud, anti-fraud, etc.
Experienced in Machine Learning and Deep Learning models;
"""

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

""" form_resume_prompt
"""

def get_resume_prompt(jd_keywords, section):
    return f'Please try to add the following keywords: {jd_keywords} to this extract of the \
        experience section of the following resume: {section}. Do not change the format and any of the original text \
            while making the resulting text seem believable:'

""" rewrite_resume
Rewrite a resume using extracted keywords
Takes in parsed_resume dict object 
Returns string 
"""

def rewrite_resume(parsed_resume, jd_keywords): 
    experience = parsed_resume.get("experience")
    skills = parsed_resume.get("skills")
    projects = parsed_resume.get("projects")
    new_experience = get_gpt3_response(get_resume_prompt(jd_keywords, experience), api_key)
    new_skills = get_gpt3_response(get_resume_prompt(jd_keywords, skills), api_key)
    new_projects = get_gpt3_response(get_resume_prompt(jd_keywords, projects), api_key)
    
    x= new_experience.count('.')
    #Replace opening \n
    new_experience= new_experience.replace('\n\n','',1)
    #Replace \n between job and job description
    new_experience= new_experience.replace('\n\n','\n\u2022',1)
    #Remove the rest
    #If have fullstop
    if x:
        new_experience = new_experience.replace('\n',' ')
        #replace fullstops
        new_experience = new_experience.replace('.','\n\u2022',x-1)
    else:
        #replace all \n
        new_experience = new_experience.replace('\n','\n\u2022')
    
    y= new_projects.count('.')
    #Replace opening \n
    new_projects= new_projects.replace('\n\n','\n\u2022',1)
    #Remove the rest
    #If have fullstop
    if y:
        new_projects = new_projects.replace('\n',' ')
        #replace fullstops
        new_projects = new_projects.replace('.','\n\u2022',y-1)
    else:
        #replace all \n
        new_projects = new_projects.replace('\n','\n\u2022')

    #print(new_projects)
    d = {}
    d['experience'] = new_experience
    d['skills'] = new_skills
    d['projects'] = new_projects
    
    return d

#print(get_keywords(jd_input))


