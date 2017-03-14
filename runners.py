import threading
import uuid
from raven import Client
from time import sleep

from call.place_call import TwilioCallWrapper
from storage.filestorage import BlobManager
from storage.models import Database, NoRecordsToProcessError, Statuses
from storage.secrets import local_tmp_dir, sentry_dsn
from transcribe.transcribe import BingTranscriber
from utils.exceptions import TemporaryChillError
from utils.tempfilemanager import TmpFileCleanup
from extract.date_info import extract_date_time
from extract.location_info import extract_location


class CourtCallRunner(object):

    def __init__(self):
        self._database = Database()
        self._caller = TwilioCallWrapper(self._call_placed_callback, self._call_done_callback)
        self._caller.try_server()

    def __str__(self):
        return "CourtCallRunner"

    def call(self):
        """
        Main call loop

        At this stage, the recording has been uploaded.
        next stages are to call speech to text api then
        semantic extraction
        """
        next_ain = self._database.retrieve_next_record_for_call()
        print("Processing {0}".format(next_ain))
        try:
            self._caller.place_call(next_ain)
        except:
            # reset and throw
            print("Rolling back {0}".format(next_ain))
            self._database.error_calling(next_ain)
            raise

    def _call_placed_callback(self, ain, call_id):
        """ Update database to say that a call was started and set call id """
        print("Call placed: {0} {1}".format(ain, call_id))
        self._database.update_call_id(ain, call_id)

    def _call_done_callback(self, ain, call_duration, recording_uri):
        """
        Download the call and reupload to azure.

        Update database to say that a call was started and save the recording location.
        """
        print("Call duration was: {0}".format(call_duration))
        try:
            azure_path = BlobManager().download_and_reupload(recording_uri)
            print("Azure path: ", azure_path)
            self._database.update_azure_path(ain, azure_path)
        except ValueError as e:
            print("Error!: {0}".format(e))


class TranscribeRunner(object):

    def __init__(self):
        self.blob_manager = BlobManager()
        self.bingTranscriber = BingTranscriber()
        self.azure_table = Database()

    def __str__(self):
        return "TranscribeRunner"

    def call(self):
        azure_blob, partition_key = self.azure_table.retrieve_next_record_for_transcribing()

        with TmpFileCleanup() as tmp_file_store:
            filename = "{0}.{1}".format(uuid.uuid4(), "wav")
            local_filename = local_tmp_dir + "/" + filename
            tmp_file_store.tmp_files.append(local_filename)

            self.blob_manager.download_wav_from_blob_and_save_to_local_file(azure_blob, local_filename)

            transcript = self.bingTranscriber.transcribe_audio_file_path(local_filename)
            print(transcript)
            self.azure_table.update_transcript(partition_key, transcript)


class EntityRunner(object):

    def __init__(self):
        self.azure_table = Database()

    def __str__(self):
        return "EntityRunner"

    def call(self):
        transcript, partition_key = self.azure_table.retrieve_next_record_for_extraction()
        location_dict = extract_location(transcript)
        print("Location: " + str(location_dict))
        date_dict = extract_date_time(transcript)
        print("Date, time: " + str(date_dict))
        self.azure_table.update_location_date(partition_key, location_dict, date_dict)


class RunnerThread(threading.Thread):

    def __init__(self, runnerClass):
        threading.Thread.__init__(self)
        self.runner = runnerClass()
        self.client = Client(sentry_dsn)

    def __str__(self):
        return str(self.runner)

    def run(self):
        while 1:
            try:
                self.runner.call()
                print("{0}: Sleeping after success".format(self.runner))
                sleep(5)  # 5 seconds
            except NoRecordsToProcessError:
                print("{0}: Nothing to do: sleeping for five minutes".format(self.runner))
                sleep(60 * 5)
            except TemporaryChillError as e:
                print("{0}: Temporary chill for {1} seconds".format(self.runner, e.pause_time))
                self.client.captureException()
                sleep(e.pause_time)
            except KeyboardInterrupt:
                return


if __name__ == "__main__":
    import argparse
    import sys
    import signal

    description = """CourtReminder! Process INS court cases. To add new cases, see ./insert.py.
If you call with no arguments, all runners will start."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--call', help='Run caller', action='store_const', const="call")
    parser.add_argument('--transcribe', help='Run transcriber', action='store_const', const="transcribe")
    parser.add_argument('--parse', help='Run entity parser', action='store_const', const="parse")
    parser.add_argument('--re_extract',
                        help='Include previously parsed records in entity parsing',
                        action='store_true')

    args = vars(parser.parse_args())

    if args.pop('re_extract'):
        db = Database()
        db.change_status(Statuses.extracting_done, Statuses.transcribing_done)
        db.change_status(Statuses.extracting, Statuses.transcribing_done)
    
    runnables = [k for k, v in args.items() if v]
    if not runnables:
        # if none passed, run them all.
        runnables = args.keys()

    runnable_map = {'call': CourtCallRunner,
                    'transcribe': TranscribeRunner,
                    'parse': EntityRunner}

    for runnable in runnables:
        thread = RunnerThread(runnable_map.get(runnable))
        thread.start()

    def interrupt(*args, **kwargs):
        sys.exit(0)

    signal.signal(signal.SIGINT, interrupt)
    while 1:
        sleep(60)
        print("There are {0} threads active:".format(threading.active_count()))
        if not threading.active_count():
            break
        for thread in threading.enumerate():
            print("{0}: {1}".format(thread.name, thread))
