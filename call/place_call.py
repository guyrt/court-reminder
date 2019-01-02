"""
Place a Twilio phone call and record the outcome.
"""

from call.secrets import *
from twilio.rest import Client as TwilioRestClient
import time
import requests

from utils.exceptions import TemporaryChillError


class TwilioCallWrapper(object):

    # use echo below to return whatever twiml is sent to it:
    # https://www.twilio.com/labs/twimlets/echo
    # we will specify the digits and length below
    callback_url = "http://twimlets.com/echo?Twiml=%3CResponse%3E%0A%3CPlay%20digits%3D%22{digits}%22%2F%3E%0A%3CPause%20length%3D%22{length}%22%2F%3E%0A%3CHangup%2F%3E%0A%3C%2FResponse%3E&"

    # base is mentioned here: https://www.twilio.com/docs/voice/api/recording
    twilio_uri_base = "https://api.twilio.com"

    call_length_seconds = 45

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

        Note: sequence must be at most 32 digits long:
        https://www.twilio.com/docs/voice/api/call#create-a-call-resource
        (Can use <Play> in twiml instead)
        """

        # with repeat:
        #return "1ww{case_number}ww1ww1ww1".format(case_number=case_number) + ("w" * 5 * 2) + "1"

        # if warning of maintenance:
        # "1w1ww{case_number}ww1w1w1".format(case_number=case_number) + ("w" * 5 * 2) + "1"

        return "1ww{case_number}ww1ww1ww1".format(case_number=case_number)


    def place_call(self, case_number):
        send_digits = self.build_dtmf_sequence(case_number)
        callback_url = self.callback_url.format(digits=send_digits, length=self.call_length_seconds)
        call = self._client.calls.create(to=to_phone, from_=from_phone, url=callback_url, record=True)
        if self.call_placed_callback:
            self.call_placed_callback(case_number, call.sid)
        self._handle_call(case_number, call.sid)

    def _get_twilio_uri(self, uri_from_recording):
        # recording.uri is:
        # -- relative to twilio_uri_base above, and
        # -- ends in ".json" which needs to be removed
        return self.twilio_uri_base + uri_from_recording.split(".json")[0]

    def _handle_call(self, case_number, call_sid):
        time.sleep(90)  # sleep for a bit to let the call happen
        call = self._client.calls.get(call_sid).fetch()

        if call.status != 'completed':
            # call.hangup() no longer works
            # see: https://www.twilio.com/docs/voice/tutorials/how-to-modify-calls-in-progress-python
            call.update(status='completed')

        call_duration = call.duration

        # get a fresh call.
        recordings = call.recordings.list()
        if not recordings:
            raise TemporaryChillError(60 * 5)
        recording = recordings[0]
        recording_uri = self._get_twilio_uri(recording.uri)

        if self.call_done_callback:
            self.call_done_callback(case_number, call_duration=call_duration, recording_uri=recording_uri)

        # delete the recording and the call from twilio
        self._cleanup_after_call(call_sid)

    def _cleanup_after_call(self, call_sid):
        call = self._client.calls.get(call_sid).fetch()

        # delete recordings
        for recording in call.recordings.list():
            recording.delete()

        # delete the call itself
        call.delete()
