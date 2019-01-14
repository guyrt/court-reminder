import argparse
import os
import requests

import call.secrets as call_secrets
from call.place_call import TwilioCallWrapper

class CallURIHandler(object):

    def __init__(self, recording_file):
        self.recording_file = recording_file

    def call_done_callback(self, case_number, call_duration, recording_uri):
        print("Call duration: {call_duration}".format(**locals()))

        response = requests.get(recording_uri)
        if response.status_code != 200:
            print("Could not retrieve recording from {recording_uri}".format(**locals()))
            return

        if os.path.exists(self.recording_file):
            print("File {0} exists".format(self.recording_file))
            input("Press enter to continue...")

        print("Saving recording to {0}".format(self.recording_file))
        with open(self.recording_file, "wb") as f:
            f.write(response.content)

def main(case_number, recording_file):
    print("Making call for case number: {case_number}".format(**locals()))
    print("Come back in 90 secs...")
    call_uri_handler = CallURIHandler(recording_file)

    call_wrapper = TwilioCallWrapper(None, call_uri_handler.call_done_callback)

    call_wrapper.place_call(case_number)

if __name__ == "__main__":

    description = "Makes call for a single case number and saves recording to given file"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--file', help='File to save recording', type=str, required=True)
    parser.add_argument('--number', help='Case number', type=int, required=True)

    args = parser.parse_args()

    main(args.number, args.file)
