#!/usr/bin/env python3

import speech_recognition as sr
from ../secrets import *

# obtain path to "english.wav" in the same folder as this script
from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "C:\\Users\\King_Ash\\Documents\\GitHub\\court-reminder\\storage\\RE95beae266dea9295637c66104c1d1e17.wav")

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source) # read the entire audio file

# recognize speech using Microsoft Bing Voice Recognition
BING_KEY = bing_speech_api_key # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
try:
    result = r.recognize_bing(audio, key=BING_KEY, language = "en-US", show_all = False)
    print("Microsoft Bing Voice Recognition thinks you said " + result)
except sr.UnknownValueError:
    print("Microsoft Bing Voice Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))