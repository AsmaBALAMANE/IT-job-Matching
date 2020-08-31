# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 23:30:58 2020

@author: BALAMANE Asma
"""

import flask
import pickle
from flask import Flask, jsonify, request
import json
import prediction_sevice as ps


app = Flask(__name__)
@app.route('/predict', methods=['POST'])
def predict():
     
    request_json = request.get_json()
    # coefficient 
    skills_rate  = float(request_json['skills_rate'])   
    title_rate   = float(request_json['title_rate'])   
    description_rate = float(request_json['description_rate'])  
    
    # job and profile
    job = request_json['job']
    profile = request_json['profile']
    #['data science, python, tensorflow','Business  Analyst','Junior to Mid-Level Business Intelligence AnalystLocation: onsite Marlborough, MAUS Citizens and Green Card Holders and those authorized to work in the US are encouraged to apply. We are unable to sponsor H1B candidates at this time.Description:We are looking for an energetic go getter who is looking to climb the career ladder!Would you like to be working with one of the worlds largest travel groups, with more than 16,000 staff worldwide. They are the world leader in the enterprise travel management space with an active global network spanning over 90 countries worldwide.  Offering a unique and welcoming culture, this rapidly growing organization works with cutting edge technology, offers a very stable, career growth-oriented environment and has excellent benefits including discounts on accommodationsWe seek a motivated person to work on the Global Technology team to enhance our technical product platform. This position requires technical ingenuity, the ability to work with people and win the hearts of our great clients. The ideal candidate will have experience working with the Microsoft BI platform and knows how to extract data from complex databases using SQL.The position will require the candidate to liaise with our global teams to manage and assist with projects through to completion. An applicant should be able to demonstrate the ability to initiate process improvements with automation to create efficiencies.  If this job is for you and you do not mind getting your hands dirty, we’ll help you grow your development skills with 2 industry leading BI platforms the Microsoft Business Intelligence Stack and the GoodData reporting suite.Responsibilities:Must have experience with: SQL Server solid understanding of relational database. Able to write queries with joins (basic to mid-level)Solid understanding of TSQL syntax, stored procedures and user defined functionsStrong problem solving and troubleshooting skillsSoft skills: Smart and quick learner.Respond to internal support queries, such as data and report validation questionsAdhoc analysis of travel data for internal review & external clientsDocumenting processes and proceduresAssist with support of our Web Development team Position Requirements:Hands on experience extracting data with SQL using complex joinsExperience using a business intelligence and analytic platformMust have experience working with end users and/ or technical product ownersMust be able to facilitate meetings and keep participants engagedHighly logical with proven analytical and problem-solving abilitiesExperience of gathering user requirements and translating these into codeAbility to execute tasks in a high-pressure environmentStrong interpersonal, written and oral communication skillsExperience of working both independently and in a team environmentStrong technical knowledge of the Microsoft Office SuiteExperience with SQL Server Reporting Services is a plusWorking knowledge of Sharepoint is a plus']
    
    #models
    w2v_skills = load_models('models/w2v_skills.p')
    w2v_jobtitles = load_models('models/w2v_jobtitles.p')
    w2v_description = load_models('models/w2v_description.p')
    
    # calculate matching rate
    matching= ps.job_profile_matching(skills_rate, title_rate, description_rate, job, profile,w2v_skills, w2v_jobtitles, w2v_description)
    response = json.dumps({'taux': matching})
    return response, 200

# deserialization
def load_models(file_path):  
    with open(file_path, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

if __name__ == '__main__':
    application.run(debug=True)
    