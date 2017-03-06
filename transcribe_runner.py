from time import sleep
from raven import Client

from utils.tempfilemanager import TmpFileCleanup
from storage.filestorage import BlobManager
from transcribe.transcribe import BingTranscriber
from storage.secrets import local_tmp_dir, sentry_dsn
from storage.models import Database, NoRecordsToProcessError
from utils.exceptions import TemporaryChillError

import uuid


class TranscribeRunner(object):

    def __init__(self):
        self.blobManager = BlobManager()
        self.bingTranscriber = BingTranscriber()
        self.azureTable = Database()
        self.tempFileCleaner = TmpFileCleanup()

    def call(self):
        azure_blob, partition_key = self.azureTable.retrieve_next_record_for_transcribing()

        with TmpFileCleanup() as tmp_file_store:
            filename = "{0}.{1}".format(uuid.uuid4(), "wav")
            local_filename = local_tmp_dir + "/" + filename
            tmp_file_store.tmp_files.append(local_filename)

            self.blobManager.download_wav_from_blob_and_save_to_local_file(azure_blob, local_filename)

            transcript = self.bingTranscriber.transcribe_audio_file_path(local_filename)
            print(transcript)
            self.azureTable.update_transcript(partition_key, transcript)


if __name__ == "__main__":
    client = Client(sentry_dsn)
    runner = TranscribeRunner()

    while 1:
        try:
            runner.call()
            print("Sleeping after success")
            sleep(5)  # 5 seconds
        except NoRecordsToProcessError:
            print("Nothing to do: sleeping for five minutes")
            sleep(60 * 5)
        except TemporaryChillError as e:
            print("Temporary chill for {0} seconds".format(e.pause_time))
            client.captureException()
            sleep(e.pause_time)
        except KeyboardInterrupt as e:
            print("Interrupted by user.")
            break
        # except Exception as e:
        #     print("Error!: {0}".format(e))
        #     client.captureException()
        #     sleep(60)

