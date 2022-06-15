from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from os import getenv
import pymysql
from random import randrange

# Instantiate Flask
app = Flask(__name__)

# #Initialize database
# app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DB_URI")
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # Database for offline testing
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = getenv('secretkey')
# db = SQLAlchemy(app)

API_KEY = getenv("API_KEY")
BASE_URI = "https://api.thecatapi.com/v1"

# CHANGE VALUE TO API_KEY VIA DECOUPLE
HEADERS = {"x-api-key": "ad829b5d-b0eb-4555-af99-2d6bb0fcdcb1"}

def make_request(endpoint: str='/'):
    
    # GET request for playlist
    response = requests.get(
        f'{BASE_URI}{endpoint}',
        HEADERS,
    )
    return response


json_data = make_request('/breeds').json()
breed_list = []
for breed in json_data:
        breed_list.append(
            {
                'id': breed['id'], 
                'name': breed['name'],
                'origin': breed['origin'], 
                'temperament': breed['temperament'], 
                'adaptability': breed['adaptability'], 
                'affection_level': breed['affection_level'],
                'energy_level': breed['energy_level'] ,
                'intelligence': breed['intelligence'],
                'friendliness': round(sum([breed['child_friendly'], breed['dog_friendly'], breed['stranger_friendly']])/3),
                'description': breed['description']
            }
        )

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(breed_list, f, indent = 4)


# ==========ROUTES==========

@app.route('/')
def index():
    random_id = breed_list[randrange(len(breed_list))]['id']
    img = make_request(f"/images/search?{random_id}").json()[0]['url']

    return render_template('index.html', img=img, breed_list=breed_list)



if __name__ == "__main__":  #pragma: no cover
    app.run(host="0.0.0.0", port=5000, debug=True)