# IT job-candidate matching : Project overview

The automatic matching system we offer simulates the human resources process to match candidates and job offers. Usually, when searching for suitable candidates, human recruiters use their understanding of the meaning of words. Then, depending on their semantic interpretation, they find the perfect match.


The machine learning model behind the matching system uses natural language processing to compare the inputs ( job offers and candidate profiles) and measures the similarity rate.  
The system ensures more than matching input words to one another; it matches their meaning, as well as of the underlying concepts and contexts.    


The system takes as input a job offer ‘j’ and a candidate's profile ‘p’. It gives as output a matching rate ‘r’ (0 < r < 1 /  with 0 for no matching and 1 for perfectly matched).

### The system process overview 

![alt text](https://github.com/AsmaBALAMANE/job-profile-matcher/blob/master/generalProcess.png?raw=true)

### Technical documentation 
-   [technical report](https://drive.google.com/file/d/1T-QxfpwCQy1Y2YQ68flzyGQi6d5uG0dD/view?usp=sharing):  a guide for understanding the proposed system and its technical details  
-   [technical architecture](https://app.milanote.com/1KhxA61Pv0Ff7b?p=8hNPmkRUZuJ): gives an overview of the system’s technical architecture and its external dependencies

## API : IT job-candidate matching

In order to use the system easily and efficiently, it was deployed with an API. Therefore, it could be used early in the development of other websites. 

### Test the API online 
The API is deployed on [heroku](https://www.heroku.com/), to test it, please use an API-tester ( e.g. [postman](https://www.postman.com/downloads/) ) 

### Endpoints
- test host    :    https://profile-job-matcher.herokuapp.com/
- endpoint:         /predict
- method:            POST 
- body: json structure 
```
{
	"skills_rate" : "w3",
	"title_rate"   : "w2" ,
	"description_rate" : "w1" ,
	"job" : {
		 "j_title": "text", 
		 "description": "text", 
		 "j_skills": "text"
	         },
	"profile" : {
		 "p_title": "text", 
		 "experiences": "text", 
		 "p_skills": "text"
	           }
}
```
- Expected reponse : json structure 
```
{
    "final_rate": r,
    "rate_description": m2,
    "rate_skills": m3,
    "rate_titles": m1
}
```

## Development Usage

### Create and train prediction models  

[ModelsTraining.ipynb](https://colab.research.google.com/drive/1MZeVYIkjrGQZSSbcCSTg0xg5TUoKHdIo#scrollTo=YZW3YrezfBHP) :  conatains code to create and train the prediction models

#### Prerequisites
- Python >= 2.8 
- Packages manager conda or pip to install requirements.

### Preparing the envirement

- Clone the repository  
- Run `pip install -r requirements.txt` in the root project folder
- Run `python wsgi.py` in the root project folder to run the app on the development server



