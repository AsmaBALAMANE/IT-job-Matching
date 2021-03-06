# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 00:00:27 2020

@author: BALAMANE Asma
"""


import numpy as np
import logging  
from collections import Counter
import itertools

# For preprocessing
import re
from gensim.models.phrases import Phrases, Phraser 
import spacy 

#import string
from gensim.parsing.preprocessing import remove_stopwords

# For word frequency 
from sklearn.metrics.pairwise import cosine_similarity  

# Setting up the loggings to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)

def job_profile_matching(input_rates, job, profile,skills_model, titles_model, desciptions_model,nlp,bigram):
  
  #Skills similarity 
    job_skills= input_preparation(job.j_skills,nlp,bigram)
    profile_skills= input_preparation(profile.p_skills,nlp,bigram)
    result_skills= get_sif_feature_vectors(job_skills,profile_skills,skills_model)
    #if any word from job input or profile input could be detected in the vocabulary
    if(result_skills==0):
       matching_skills=0
    else:
       matching_skills= get_cosine_similarity(result_skills[0],result_skills[1])  
    print('matching_skills:', matching_skills)
  #Title similarity  
    job_title= input_preparation(job.j_title,nlp,bigram)
    profile_title= input_preparation(profile.p_title,nlp,bigram)
    result_title= get_sif_feature_vectors(job_title,profile_title,titles_model)
    #if any word from job input or profile input could be detected in the vocabulary
    if(result_title==0):
       matching_title=0
    else:
       matching_title= get_cosine_similarity(result_title[0],result_title[1])
    print('matching_title:',matching_title)
  #Description similarity
    job_description= input_preparation(job.description,nlp,bigram)
    profile_description= input_preparation(profile.experiences,nlp,bigram)
    result_description= get_sif_feature_vectors(job_description,profile_description,desciptions_model)
     #if any word from job input or profile input could be detected in the vocabulary
    if(result_description==0):
       matching_description=0
    else:
      matching_description= get_cosine_similarity(result_description[0],result_description[1]) 
    print('matching_description:', matching_description)
    
    final_matching= matching_skills * input_rates.skills_rate + matching_title * input_rates.title_rate + matching_description * input_rates.description_rate
    print('final_matching:', final_matching)
   
    matching= dict({"matching_titles": matching_title,
            "matching_description": matching_description,
            "matching_skills":matching_skills,
            "final_matching": final_matching
            })
    
    return matching
 
# Prediction for List of profiles 
def job_profileList_matching(input_rates, job, profiles,skills_model, titles_model, desciptions_model,nlp,bigram): 
    rates_raw= []
  # calculate matching rates   
    for profile in profiles:   
       matching= job_profile_matching(input_rates, job, profile,skills_model, titles_model, desciptions_model,nlp,bigram)
       rates_raw.append(matching)  
    return rates_raw

# Prediction for List of jobs 
def profile_jobList_matching(input_rates, jobs, profile,skills_model, titles_model, desciptions_model,nlp,bigram): 
    rates_raw= []
  # calculate matching rates   
    for job in jobs:   
       matching= job_profile_matching(input_rates, job, profile,skills_model, titles_model, desciptions_model,nlp,bigram)
       rates_raw.append(matching)  
    return rates_raw

# Features Extraction 
def map_word_frequency(document):
    return Counter(itertools.chain(*document))
    
def get_sif_feature_vectors(sentence1, sentence2, word_emb_model):
    sentence1 = [token for token in sentence1 if token in word_emb_model.wv.vocab]
    sentence2 = [token for token in sentence2 if token in word_emb_model.wv.vocab]
    print(sentence1)
    print(sentence2) 
    if (not sentence1 or not sentence2): 
     return 0
    word_counts = map_word_frequency((sentence1 + sentence2))
    embedding_size = 300 # size of vectore in word embeddings
    a = 0.001
    sentence_set=[]
    for sentence in [sentence1, sentence2]:
        vs = np.zeros(embedding_size)
        sentence_length = len(sentence)
        for word in sentence:
            a_value = a / (a + word_counts[word]) # smooth inverse frequency, SIF
            vs = np.add(vs, np.multiply(a_value, word_emb_model.wv[word])) # vs += sif * word_vector
        vs = np.divide(vs, sentence_length) # weighted average
        sentence_set.append(vs)
    return sentence_set

#Input preparation 
def input_preparation(sentence,nlp,bigram): 
    doc1=nlp(sentence)
    txt= [token.lower() for token in cleaning(doc1).split()]
    txt = list(txt) 
    r = re.compile("[A-Za-z#++']+")
    txt = list(filter(r.match, txt)) 
    sentences = bigram[txt]
    return sentences

def cleaning(doc):
    # doc is a spacy Doc object
    # Lemmatization and  stopwords removing (using the SpaCy stopWords list)
    text = [token.lemma_ for token in doc if not token.is_stop]
    txt = ' '.join(text)
    #remove stopword using gensim stopword list
    txt = remove_stopwords(txt)
    #correct some indetected words by the NER model 
    txt= txt.replace("c #", "c#").replace("phantom js", "phantomjs")
    return txt

# calculate similarity 
def get_cosine_similarity(feature_vec_1, feature_vec_2):    
    return cosine_similarity(feature_vec_1.reshape(1, -1), feature_vec_2.reshape(1, -1))[0][0]