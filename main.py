# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 20:41:38 2020

@author: BALAMANE Asma
"""
from fastapi import FastAPI, HTTPException
import model_class as modelClass
import prediction_sevice as ps
import helpers as hlpr
from typing import List
from gensim.models.phrases import Phrases, Phraser 
import spacy 

app = FastAPI()

# if mode==0 : use 3 models(jobTitleModel, skillsModel, DescriptionModel); 
# if mode==1 : use global model
# recommended mode is 1
__mode=1

#Loading models 
if __mode==1 :
    w2v_all = hlpr.load_models('models/w2v_all.p')
if __mode==0 :    
    w2v_skills = hlpr.load_models('models/w2v_skills.p')
    w2v_jobtitles = hlpr.load_models('models/w2v_jobtitles.p')
    w2v_description = hlpr.load_models('models/w2v_description.p') 
    
nlp = spacy.load("en_core_web_sm")    
bigram = Phrases.load("models/pharser.pkl")
    
@app.get("/healthcheck")
async  def healthcheck():
    msg = (
        "Connected"
    )
    return {"message": msg}

@app.post("/predict", response_model=modelClass.Matching, status_code=200)
def predict(job:modelClass.Job, profile: modelClass.Profile, input_rates: modelClass.InputRates):
    
     if __mode==0 :
        matching= ps.job_profile_matching(input_rates, job, profile,w2v_skills, w2v_jobtitles, w2v_description,nlp,bigram)
     if __mode==1 :
        matching= ps.job_profile_matching(input_rates, job, profile, w2v_all, w2v_all, w2v_all,nlp,bigram)
        
     if not matching:
        raise HTTPException(status_code=500, detail="Prediction Error.")

     print(matching)
     return matching
    
@app.post("/predictListProfiles", response_model=List[modelClass.Matching], status_code=200)
async def predictListProfiles(job:modelClass.Job, profiles: List[modelClass.Profile], input_rates: modelClass.InputRates):
   for profile in profiles:
     if __mode==0 :
        matching= ps.job_profileList_matching(input_rates, job, profiles,w2v_skills, w2v_jobtitles, w2v_description,nlp,bigram)
     if __mode==1 :
        matching= ps.job_profileList_matching(input_rates, job, profiles, w2v_all, w2v_all, w2v_all,nlp,bigram)
        
     if not matching:
        raise HTTPException(status_code=500, detail="Prediction Error.")

     print(matching)
     return matching

@app.post("/predictListOffers", response_model=List[modelClass.Matching], status_code=200)
async def predictListOffers(jobs:List[modelClass.Job], profile: modelClass.Profile, input_rates: modelClass.InputRates):
     if __mode==0 :
        matching= ps.profile_jobList_matching(input_rates, jobs, profile,w2v_skills, w2v_jobtitles, w2v_description,nlp,bigram)
     if __mode==1 :
        matching= ps.profile_jobList_matching(input_rates, jobs, profile, w2v_all, w2v_all, w2v_all,nlp,bigram)
        
     if not matching:
        raise HTTPException(status_code=500, detail="Prediction Error.")

     print(matching)
     return matching