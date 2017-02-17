"""
Place a Twilio phone call and record the outcome.
"""

from call.secrets import *
from twilio.rest import TwilioRestClient
import time
import requests

class TwilioCallWrapper(object):

    callback_url = 'http://13.68.220.163/record.xml'

    def __init__(self, call_placed_callback=None, call_done_callback=None):
        self.call_placed_callback = call_placed_callback
        self.call_done_callback = call_done_callback

        self._client = TwilioRestClient(twilio_account_sid, twilio_auth_token)

    def try_server(self):
        try:
            response = requests.get(self.callback_url)
            if response.status_code != 200:
                raise RuntimeError("Server {0} not found. Can't make calls.".format(self.callback_url))
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Server {0} not found. Can't make calls.".format(self.callback_url))

    def build_dtmf_sequence(self, case_number):
        """ Sequence represents the following:

        Send 1  [to enter in English?]
        Wait 1 Second
        Send case number
        Wait 1 Second
        Send 1  [why?]
        Wait 1 Second
        Send 1  [why?]
        Wait 1 Second
        Send 1  [why?]
        Wait for 10 seconds
        Send 1  [trick into a repeat so we catch the full message.]
        """
        return "1ww{case_number}ww1ww1ww1".format(case_number=case_number) + ("w" * 5 * 2) + "1"

    def place_call(self, case_number):
        send_digits = self.build_dtmf_sequence(case_number)
        call = self._client.calls.create(to=to_phone, from_=from_phone, url=self.callback_url, record=True, send_digits=send_digits)
        if self.call_placed_callback:
            self.call_placed_callback(case_number, call.sid)
        self._handle_call(case_number, call.sid)

    def _handle_call(self, case_number, call_sid):
        time.sleep(90)  # sleep for a bit to let the call happen
        call = self._client.calls.get(call_sid)

        if call.status != 'completed':
            call.hangup()
        call_duration = call.duration

        # get a fresh call.
        recording = call.recordings.list()[0]
        recording_uri = recording.uri

        if self.call_done_callback:
            self.call_done_callback(case_number, call_duration=call_duration, recording_uri=recording_uri)
