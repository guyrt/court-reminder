"""
handle downloading and reuploading files to our own servers
"""
import os
import requests
import uuid
from azure.storage.blob import BlobService
from storage.secrets import blob_key, blob_accountname, blob_container, local_tmp_dir


def download_and_reupload(twilio_filename):
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


class TmpFileCleanup(object):
    """ Used to clean up tmp files.
    """

    def __enter__(self):
        # Keep local copy of the tmp files.
        self.tmp_files = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Delete all tmp files.
        for file_path in self.tmp_files:
            try:
                os.remove(file_path)
            except OSError:
                pass

