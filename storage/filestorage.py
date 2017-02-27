"""
handle downloading and reuploading files to our own servers
"""

import requests
import uuid 
from utils.tempfilemanager import TmpFileCleanup
from azure.storage.blob import BlobServicepip
from storage.secrets import blob_key, blob_accountname, blob_container, local_tmp_dir

class BlobManager(object):

    def download_and_reupload(self, twilio_filename):
        """ Download file from Twilio, upload to Azure, and return the Azure location and local file. """
        blob_service = BlobService(account_name=blob_accountname, account_key=blob_key)
        response = requests.get(twilio_filename)
        if response.status_code != 200:
            raise ValueError("Couldn't find Twilio file {0}".format(twilio_filename))

        suffix = "wav"
        short_file_name = "{0}.{1}".format(uuid.uuid4(), suffix)
        azure_path = "/recordings/" + short_file_name

        with TmpFileCleanup() as tmp_file_store:
            local_filename = local_tmp_dir + "/" + short_file_name
            tmp_file_store.tmp_files.append(local_filename)
            f = open(local_filename, "wb")
            f.write(response.content)
            f.close()
            # Now upload the local file to azure
            blob_service.put_block_blob_from_path(
                blob_container,
                azure_path,
                local_filename,
                'audio/x-wav'
            )
        return azure_path

    def download_wave_from_blob_and_save_to_local_file(self, azure_path, temp_file_name):
        blob_service = BlobService(account_name=blob_accountname, account_key=blob_key)
        
        f = open(temp_file_name, "wb")
        x= blob_service.get_blob_to_file(container_name= blob_container, blob_name= azure_path, stream= f)
        f.close()