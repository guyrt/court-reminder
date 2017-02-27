#!/usr/bin/env python3

import speech_recognition as sr
from transcribe.secrets import *

# obtain path to "english.wav" in the same folder as this script
from os import path
class BingTranscriber(object):

    def __init__(self):
        self.bing_key = bing_speech_api_key
        self.language="en-US"
        self.audio_file = path.join(path.dirname(path.realpath(__file__)), sample_wav)

    def transcribe_audio_object(self, audio_object):    
            try:
                r = sr.Recognizer()
                return r.recognize_bing(audio_object, key=self.bing_key, language = self.language, show_all = False)
            except sr.UnknownValueError:
                print("Microsoft Bing Voice Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

    def transcribe_audio_file_path(self, audio_file_path):
        r = sr.Recognizer()
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = r.record(source)       
                return self.transcribe_audio_object(audio)
        except sr.UnknownValueError as e:
            print("{0}".format(e))