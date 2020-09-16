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
    
    # get job as vector
    profile=[]
    profile.append(request_json['profile']['p_skills'])
    profile.append(request_json['profile']['p_skills'])
    profile.append(request_json['profile']['experiences'])
    
 
    #models
    w2v_skills = load_models('models/w2v_skills.p')
    w2v_jobtitles = load_models('models/w2v_jobtitles.p')
    w2v_description = load_models('models/w2v_description.p')  
    # calculate matching rate
    matching= ps.job_profile_matching(skills_rate, title_rate, description_rate, job, profile,w2v_skills, w2v_jobtitles, w2v_description)
    rates= {'rate_titles': matching[0],'rate_description': matching[1],'rate_skills': matching[2],'final_rate': matching[3]}
    response = flask.jsonify(rates)
    return response, 200

# deserialization
def load_models(file_path):  
    with open(file_path, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

if __name__ == '__main__':
    application.run(debug=True)
    