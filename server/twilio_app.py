"""
Simple twillio callback app
"""

import sys
from flask import Flask
from twilio import twiml


app = Flask(__name__)
   

@app.route("/record.xml", methods=['GET', 'POST'])
def record():
    response = twiml.Response()
    response.pause(length=120)
    return str(response)
