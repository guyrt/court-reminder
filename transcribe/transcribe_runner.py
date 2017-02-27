
from utils.tempfilemanager import TmpFileCleanup
from storage.filestorage import BlobManager
from transcribe.transcribe import BingTranscriber
from transcribe.secrets import local_tmp_dir

import uuid 

def TranscribeRunner(azure_blob):

    blobManager= BlobManager()
    bingTranscriber = BingTranscriber()

    tempFileCleaner = TmpFileCleanup()

    with TmpFileCleanup() as tmp_file_store:
        filename = "{0}.{1}".format(uuid.uuid4(), "wav")
        local_filename = "C:/"+local_tmp_dir + "/" + filename
        tmp_file_store.tmp_files.append(local_filename)

        blobManager.download_wave_from_blob_and_save_to_local_file(azure_blob, local_filename)
        
        result=bingTranscriber.transcribe_audio_file_path(local_filename)
        print(result)