"""
Main runner
"""

from storage.models import Database, NoRecordsToProcessError
from storage.filestorage import download_and_reupload
from call.place_call import TwilioCallWrapper
from time import sleep


class CourtReminderRunner(object):

    def __init__(self):
        self._database = Database()
        self._caller = TwilioCallWrapper(self._call_placed_callback, self._call_done_callback)
        self._caller.try_server()

    def call(self):
        """
        Main call loop
        """
        next_ain = self._database.retrieve_next_record_for_call()
        print("Processing {0}".format(next_ain))
        self._caller.place_call(next_ain)

        # at this stage, the recording has been uploaded.
        # next stages are to call speech to text api then
        # semantic extraction

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
            azure_path = download_and_reupload(recording_uri)
            print("Azure path: ", azure_path)
            self._database.update_azure_path(ain, azure_path)
        except ValueError as e:
            print("Error!: {0}".format(e))


if __name__ == "__main__":
    import time

    runner = CourtReminderRunner()
    while 1:
        try:
            runner.call()
            print("Sleeping after success")
            sleep(5)  # 5 seconds
        except NoRecordsToProcessError:
            print("Nothing to do: sleeping for five minutes")
            sleep(60 * 5)
