"""
Simple twillio callback app
"""

import sys
from flask import Flask
from twilio import twiml

from storage.models import Database

app = Flask(__name__)
db = Database()


@app.route("/", methods=['GET', 'POST'])
def index():
    return str(db.list_calls())


@app.route("/ain/<ain>", methods=['GET'])
def get_ain(ain):
    return str(db.get_ain(ain))
    

@app.route("/ain/<ain>", methods=['POST'])
def post_ain(ain):
    return db.upload_new_requests([ain]) 
    

@app.route("/record.xml", methods=['GET', 'POST'])
def record():
    response = twiml.Response()
    response.pause(length=120)
    return str(response)
