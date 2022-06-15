from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from os import getenv
import pymysql

# Instantiate Flask
app = Flask(__name__)

# #Initialize database
# app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DB_URI")
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # Database for offline testing
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = getenv('secretkey')
# db = SQLAlchemy(app)


headers = {"x-api-key": "ad829b5d-b0eb-4555-af99-2d6bb0fcdcb1"}


# ==========ROUTES==========

@app.route('/')
def index():
    
    response = requests.get("https://api.thecatapi.com/v1/images/search?breed_ids=beng", headers=headers)
    json = response.json()[0]
    img = json['url']
    description = json['breeds'][0]['description']

    return render_template('index.html', img=img, desc=description)



if __name__ == "__main__":  #pragma: no cover
    app.run(host="0.0.0.0", port=5000, debug=True)