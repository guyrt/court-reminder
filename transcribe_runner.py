
from utils.tempfilemanager import TmpFileCleanup
from storage.filestorage import BlobManager
from transcribe.transcribe import BingTranscriber
from transcribe.secrets import local_tmp_dir
from storage.models import Database

import uuid 

def TranscribeRunner():

    blobManager= BlobManager()
    bingTranscriber = BingTranscriber()
    azureTable = Database()
    tempFileCleaner = TmpFileCleanup()
    
    azure_blob, partition_key = azureTable.retrieve_next_record_for_transcribing()

    with TmpFileCleanup() as tmp_file_store:
        filename = "{0}.{1}".format(uuid.uuid4(), "wav")
        local_filename = "C:/"+local_tmp_dir + "/" + filename
        tmp_file_store.tmp_files.append(local_filename)

        blobManager.download_wave_from_blob_and_save_to_local_file(azure_blob, local_filename)
        
        transcript=bingTranscriber.transcribe_audio_file_path(local_filename)
        print(partition_key)
        print(transcript)
        #azureTable.update_transcript(partition_key,result)

TranscribeRunner()
