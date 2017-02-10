"""
Main runner
"""

from storage.models import Database, NoRecordsToProcessError
from call.place_call import TwilioCallWrapper


class CourtReminderRunner(object):

    def __init__(self):
        self._database = Database()
        self._caller = TwilioCallWrapper(self._call_placed_callback, self._call_done_callback)

    def call():
        """
        Main call loop
        """
        next_sid = self._database.retrieve_next_record_for_call()

        # at this stage, the recording has been uploaded.
        # next stages are to call speech to text api then
        # semantic extraction

    def _call_placed_callback(self, call_id):
        """ Update database to say that a call was started and set call id """
        print(call_id)

    def _call_done_callback(self, recording_id):
        """ 
        Download the call and reupload to azure.

        Update database to say that a call was started and save the recording location.
        """
        print(recording_id)


if __name__ == "__main__":
    import time

    runner = CourtReminderRunner()
    while 1:
        try:
            runner.call()
            sleep(5)  # 5 seconds
        except NoRecordsToProcessError:
            sleep(60 * 60)  # sleep for an hour
