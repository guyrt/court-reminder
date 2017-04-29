import threading
import uuid
import sys

from datetime import datetime, timedelta
from raven import Client
from time import sleep

from call.place_call import TwilioCallWrapper
from storage.filestorage import BlobManager
from storage.models import Database, NoRecordsToProcessError, Statuses
from storage.secrets import local_tmp_dir, sentry_dsn
from transcribe.transcribe import GoogleTranscriber, TranscriptionStatus
from utils.exceptions import (
    TemporaryChillError,
    TooManyErrorsException,
    TranscriptionError,
    TwilioResponseError,
    EntityExtractionError,
)
from utils.tempfilemanager import TmpFileCleanup
from extract.date_info_Google import extract_date_time
from extract.location_info_Google import extract_location



class RunnerBase(object):

    # Max number of consecutive errors allowed in a runner before shutting down
    # program
    MAX_ALLOWABLE_ERRORS = 30
    default_sleep_time = 5  # seconds

class CourtCallRunner(RunnerBase):
    def __init__(self):
        self._database = Database()
        self._caller = TwilioCallWrapper(self._call_placed_callback,
            self._call_done_callback)
        self._caller.try_server()
        self.consec_error_count = 0

    def __str__(self):
        return "CourtCallRunner"

    def call(self):
        """
        Main call loop

        At this stage, the recording has been uploaded.
        next stages are to call speech to text api then
        semantic extraction
        """
        if self.consec_error_count > self.MAX_ALLOWABLE_ERRORS:
            raise TooManyErrorsException
        next_ain = self._database.retrieve_next_record_for_call()
        print("Processing {0}".format(next_ain))
        try:
            self._caller.place_call(next_ain)
            self.consec_error_count = 0
        except:
            # reset and throw
            print("Rolling back {0}".format(next_ain))
            self._database.set_error(next_ain, Statuses.new)
            self.consec_error_count += 1
            raise

    def _call_placed_callback(self, ain, call_id):
        """ Update database to say that a call was started and set call id """
        print("Call placed: {0} {1}".format(ain, call_id))
        self._database.update_call_id(ain, call_id)

    def _call_done_callback(self, ain, call_duration, recording_uri):
        """
        Download the call and reupload to azure.

        Update database to say that a call was started
        and save the recording location.
        """
        print("Call duration was: {0}".format(call_duration))
        try:
            azure_path = BlobManager().download_and_reupload(recording_uri)
            print("Azure path: ", azure_path)
            self._database.update_azure_path(ain, azure_path)
        except TwilioResponseError as e:
            raise


class TranscribeRunner(RunnerBase):

    def __init__(self):
        self.blob_manager = BlobManager()
        self.googleTranscriber = GoogleTranscriber()
        self.azure_table = Database()
        self.consec_error_count = 0

    def __str__(self):
        return "TranscribeRunner"

    def call(self):
        if self.consec_error_count > self.MAX_ALLOWABLE_ERRORS:
            raise TooManyErrorsException

        azure_blob, partition_key = \
            self.azure_table.retrieve_next_record_for_transcribing()

        with TmpFileCleanup() as tmp_file_store:
            filename = "{0}.{1}".format(uuid.uuid4(), "wav")
            local_filename = local_tmp_dir + "/" + filename
            tmp_file_store.tmp_files.append(local_filename)
            self.blob_manager.download_wav_from_blob_and_save_to_local_file(
                azure_blob,
                local_filename,
            )
            transcript, transcription_status = \
                self.googleTranscriber.transcribe_audio_file_path(
                    local_filename,
            )
        self.azure_table.update_transcript(
            partition_key,
            transcript,
            transcription_status,
        )
        if transcription_status != TranscriptionStatus.success:
            self.consec_error_count += 1
            raise TranscriptionError("Transcription failed, status: " +
                transcription_status)
        else:
            self.consec_error_count = 0
            print("Transcript for {partition_key}: {transcript}"
                .format(**locals()))


class EntityRunner(RunnerBase):

    def __init__(self):
        self.azure_table = Database()
        self.consec_error_count = 0

    def __str__(self):
        return "EntityRunner"

    def call(self):
        if self.consec_error_count > self.MAX_ALLOWABLE_ERRORS:
            raise TooManyErrorsException

        transcript, partition_key = self.azure_table.retrieve_next_record_for_extraction()
        location_dict = extract_location(transcript)
        print("Location for {0}: {1}".format(partition_key, str(location_dict)))
        date_dict = extract_date_time(transcript)
        print("Date, time for {0}: {1}".format(partition_key, str(date_dict)))
        self.azure_table.update_location_date(partition_key,
            location_dict, date_dict)
        if location_dict == None or date_dict == None:
            self.consec_error_count += 1
            raise EntityExtractionError(
                "failed to extract location or date for {0}"
                .format(partition_key))
        else:
            self.consec_error_count = 0


class ErrorRecovery(RunnerBase):
    """
    Handles two kinds of errors:
        - Stale progressions.
        - Error states.
    """

    default_sleep_time = 60 * 10

    def __init__(self):
        self.azure_table = Database()

    def __str__(self):
        return "ErrorRecovery"

    def call(self):
        cutoff_time = datetime.now() - timedelta(days=14)
        try:
            num_resets = self.azure_table.reset_stale_calls(cutoff_time)
        except NoRecordsToProcessError:
            num_resets = 0
        print("Reset {0} records".format(num_resets))


class RunnerThread(threading.Thread):

    def __init__(self, runnerClass, stop_event):
        threading.Thread.__init__(self)
        self.runner = runnerClass()
        self.client = Client(sentry_dsn)
        self.stop_event = stop_event

    def __str__(self):
        return str(self.runner)

    def run(self):
        while not self.stop_event.isSet():
            try:
                self.runner.call()
                print("{0}: Sleeping after success".format(self.runner))
                sleep(self.runner.default_sleep_time)
            except NoRecordsToProcessError:
                mins = 5
                print("{0}: Nothing to do: sleeping for {1} minutes".format(self.runner, mins))
                sleep(60 * mins)
            except TemporaryChillError as e:
                print("{0}: No recording after call completion; temporary chill for {1} seconds".format(self.runner, e.pause_time))
                self.client.captureException()
                sleep(e.pause_time)
            except KeyboardInterrupt:
                sys.exit("Exited due to Keyboard Interrupt")
                return
            except TooManyErrorsException:
                print("\n Too many consecutive errors with the " +
                      str(self.runner) + " thread; Setting stop event \n")
                self.stop_event.set()
                return
            except (
                TranscriptionError,
                TwilioResponseError,
                EntityExtractionError,
                ) as e:
                print("{0}: {1}".format(self.runner, e))

        print("The " + str(self.runner) + " thread has received a stop event")


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
    parser.add_argument('--recover', help='Run error recovery function', action='store_const', const="recover")
    parser.add_argument('--re_extract',
                        help='Include previously parsed records in entity parsing, used for testing',
                        action='store_true')
    parser.add_argument('--re_transcribe',
                        help='Include previously transcribed records in entity transcription, used for testing',
                        action='store_true')
    parser.add_argument('--tryAgain',
                        help='Try calling again numbers for which we failed to get location date info',
                        action='store_true')
    parser.add_argument('--setCallingToNew',
                        help='Resets statuses stuck on calling to new',
                        action='store_true')
    parser.add_argument('--set_to_new',
                        help='Resets all status to new, used for testing',
                        action='store_true')


    args = vars(parser.parse_args())

    if args.pop('tryAgain'):
        db = Database()
        db.change_status(Statuses.failed_to_return_info, Statuses.new)

    if args.pop('setCallingToNew'):
        db = Database()
        db.change_status(Statuses.calling, Statuses.new)


    if args.pop('re_extract'):
        db = Database()
        db.change_status(Statuses.extracting_done, Statuses.transcribing_done)
        db.change_status(Statuses.extracting, Statuses.transcribing_done)

    if args.pop('re_transcribe'):
        db = Database()
        db.change_status(Statuses.transcribing_done, Statuses.recording_ready)
        db.change_status(Statuses.transcribing, Statuses.recording_ready)
        db.change_status(Statuses.extracting, Statuses.recording_ready)
        db.change_status(Statuses.extracting_done, Statuses.recording_ready)

    if args.pop('set_to_new'):
        db = Database()
        db.change_status(Statuses.transcribing_done, Statuses.new)
        db.change_status(Statuses.transcribing, Statuses.new)
        db.change_status(Statuses.extracting, Statuses.new)
        db.change_status(Statuses.extracting_done, Statuses.new)
        db.change_status(Statuses.calling, Statuses.new)
        db.change_status(Statuses.failed_to_return_info, Statuses.new)
        db.change_status(Statuses.error, Statuses.new)

    runnables = [k for k, v in args.items() if v]
    if not runnables:
        # if none passed, run them all.
        runnables = args.keys()

    runnable_map = {'call': CourtCallRunner,
                    'transcribe': TranscribeRunner,
                    'recover': ErrorRecovery,
                    'parse': EntityRunner}

    stop_event = threading.Event() #all threads will share this stop event

    for runnable in runnables:
        thread = RunnerThread(runnable_map.get(runnable), stop_event)
        thread.start()

    def interrupt(*args, **kwargs):
        sys.exit(0)

    signal.signal(signal.SIGINT, interrupt)

    while not stop_event.isSet():
        sleep(60)
        print("There are {0} threads active:".format(threading.active_count()))

        for thread in threading.enumerate():
            print("{0}: {1}".format(thread.name, thread))
