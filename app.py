from flask import Flask, render_template
import requests
import json
from os import getenv
from random import randrange

# Instantiate Flask
app = Flask(__name__)


API_KEY = getenv("API_KEY")
BASE_URI = "https://api.thecatapi.com/v1"

# CHANGE VALUE TO API_KEY VIA DECOUPLE
HEADERS = {"x-api-key": "ad829b5d-b0eb-4555-af99-2d6bb0fcdcb1"}


# Function for making get requests
def make_request(endpoint: str='/'):
    
    # GET request for playlist
    response = requests.get(
        f'{BASE_URI}{endpoint}',
        HEADERS,
    )
    return response

# Requests the breeds endpoints to recieve all possible breeds
json_data = make_request('/breeds').json()
breed_list = []

# Filtering incoming json for only required elements
for breed in json_data:
    try:
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
                'description': breed['description'],
                'img': breed['image']['url']
            }
        )
        
    # 'image' call sometimes results in KeyError as some JSON objects have no image
    except KeyError:
        continue

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(breed_list, f, indent = 4)


# ==========ROUTES==========

@app.route('/')
def index():

    return render_template('index.html', breed_list=breed_list)

@app.route('/kasino')
def kasino():
    random_cat = breed_list[randrange(len(breed_list))]
    name = random_cat['name']
    img = random_cat['img']
    desc = random_cat['description']
    
    return render_template('kasino.html', name=name, img=img, desc=desc)


if __name__ == "__main__":  #pragma: no cover
    app.run(host="0.0.0.0", port=5000, debug=True)