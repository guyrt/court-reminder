"""
Flask Admin App
"""

import os

from flask import Flask, flash, render_template, request
from flask_admin import Admin
from flask_basicauth import BasicAuth
from azure.storage.blob import BlockBlobService, ContentSettings

from storage.models import Database
from storage.secrets import blob_key, blob_accountname, blob_container
from server.views import AinView
from server import config

db = Database()
blob_service = BlockBlobService(account_name=blob_accountname, account_key=blob_key)

app = Flask(__name__)
app.config.from_object(config.Config)

basic_auth = BasicAuth(app)

admin = Admin(app, name='ASAP', template_mode='bootstrap3')
admin.add_view(AinView(None, name='Ain', endpoint='ain'))


@app.route('/audio')
def audio():
    ain = request.args.get('id')
    azure_path = db.get_ain(ain).get('CallUploadUrl')
    if azure_path:
        filename = ain + '.wav'
        path = os.path.join('static', filename)
        blob_service.get_blob_to_path(container_name=blob_container, 
              blob_name=azure_path, file_path=path)
    else:
        filename = None
    return render_template('audio.html', filename=filename)

