# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 23:43:26 2020

@author: a.balamane
"""
from pydantic import BaseModel
from typing import List

class Profile(BaseModel):
    p_title: str
    experiences: str
    p_skills: str
       
class ProfileList(Profile):
    profiles: List[Profile] 
    
class Job(BaseModel):
    j_title: str
    description: str
    j_skills: str
    
    
class JobList(Job):
    Jobs: List[Job]  
       
    
class InputRates(BaseModel):
    skills_rate: float
    title_rate: float
    description_rate: float    
    
class Matching(BaseModel):
    matching_titles: float
    matching_description: float
    matching_skills: float     
    final_matching: float  
  