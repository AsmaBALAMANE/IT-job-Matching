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

# if mode==0 : use 3 models; if mode==1 : use global model
__mode=1
# deserialization
def load_models(file_path):  
    with open(file_path, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

#Loading models
if __mode==1 :
    w2v_all = load_models('models/w2v_all.p')
if __mode==0 :    
    w2v_skills = load_models('models/w2v_skills.p')
    w2v_jobtitles = load_models('models/w2v_jobtitles.p')
    w2v_description = load_models('models/w2v_description.p') 

@app.route('/', methods=['GET'])
def connect():
    response = json.dumps({'response': 'connected'})
    return response, 200

@app.route('/predict', methods=['POST'])
def predict():
     
    request_json = request.get_json()
    # coefficient 
    skills_rate  = float(request_json['skills_rate'])   
    title_rate   = float(request_json['title_rate'])   
    description_rate = float(request_json['description_rate'])  
    
    # get job as vector
    job=[]
    job.append(request_json['job']['j_skills'])
    job.append(request_json['job']['j_title'])
    job.append(request_json['job']['description'])
    
   # get profile as vector
    profile=[]
    profile.append(request_json['profile']['p_skills'])
    profile.append(request_json['profile']['p_title'])
    profile.append(request_json['profile']['experiences'])
  
    # calculate matching rate
    if __mode==0 :
      matching= ps.job_profile_matching(skills_rate, title_rate, description_rate, job, profile,w2v_skills, w2v_jobtitles, w2v_description)
    if __mode==1 :
      matching= ps.job_profile_matching(skills_rate, title_rate, description_rate, job, profile, w2v_all, w2v_all, w2v_all)
    rates= {'rate_titles': matching[0],'rate_description': matching[1],'rate_skills': matching[2],'final_rate': matching[3]}
    response = flask.jsonify(rates)
    return response, 200


@app.route('/predictListOffers', methods=['POST'])
def predictListOffers():
     
    request_json = request.get_json()
    # coefficient 
    skills_rate  = float(request_json['skills_rate'])   
    title_rate   = float(request_json['title_rate'])   
    description_rate = float(request_json['description_rate'])  
        
     # get Profile as vector
    profile=[]
    profile.append(request_json['profile']['p_skills'])
    profile.append(request_json['profile']['p_title'])
    profile.append(request_json['profile']['experiences'])
        
    jobs=[]
    rates_raw=[]  
   
    jobs= request_json['job']
    for job in jobs:   
        # get job as vector
        job_raw=[] 
        job_raw.append(job['j_skills'])
        job_raw.append(job['j_title'])
        job_raw.append(job['description'])
        
        # calculate matching rate 
        if __mode==0 :
          matching= ps.job_profile_matching(skills_rate, title_rate, description_rate, job_raw, profile,w2v_skills, w2v_jobtitles, w2v_description)
        if __mode==1 :
          matching= ps.job_profile_matching(skills_rate, title_rate, description_rate, job_raw, profile,w2v_all, w2v_all, w2v_all)
        rates= {'rate_titles': matching[0],'rate_description': matching[1],'rate_skills': matching[2],'final_rate': matching[3]}
        rates_raw.append(rates)
        
    response = flask.jsonify(rates_raw)
    return response, 200

@app.route('/predictListProfiles', methods=['POST'])
def predictListProfiles():
     
    request_json = request.get_json()
    # coefficient 
    skills_rate  = float(request_json['skills_rate'])   
    title_rate   = float(request_json['title_rate'])   
    description_rate = float(request_json['description_rate'])  

    # get job as vector
    job=[]
    job.append(request_json['job']['j_skills'])
    job.append(request_json['job']['j_title'])
    job.append(request_json['job']['description'])

    #models
    w2v_skills = load_models('models/w2v_skills.p')
    w2v_jobtitles = load_models('models/w2v_jobtitles.p')
    w2v_description = load_models('models/w2v_description.p')  
   
    profiles=[]
    rates_raw=[]  
   
    profiles= request_json['profile']
    for profile in profiles:   
        # get job as vector
        profile_raw=[] 
        profile_raw.append(profile['p_skills'])
        profile_raw.append(profile['p_title'])
        profile_raw.append(profile['experiences'])
        
        # calculate matching rate 
        if __mode==0 :
           matching= ps.job_profile_matching(skills_rate, title_rate, description_rate, job, profile_raw,w2v_skills, w2v_jobtitles, w2v_description)
        if __mode==1 : 
           matching= ps.job_profile_matching(skills_rate, title_rate, description_rate, job, profile_raw,w2v_all, w2v_all, w2v_all)
        rates= {'rate_titles': matching[0],'rate_description': matching[1],'rate_skills': matching[2],'final_rate': matching[3]}
        rates_raw.append(rates)
        
    response = flask.jsonify(rates_raw)
    return response, 200


if __name__ == '__main__':
    application.run(debug=True)
    