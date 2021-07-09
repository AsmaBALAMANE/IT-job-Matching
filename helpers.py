# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 21:36:54 2020

@author: a.balamane
"""
import pickle

# deserialization
def load_models(file_path):  
    with open(file_path, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model 
