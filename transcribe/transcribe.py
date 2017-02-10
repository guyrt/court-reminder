#!/usr/bin/env python3

import speech_recognition as sr
from secrets import *

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


# def text2int(textnum, numwords={}):
#     if not numwords:
#       units = [
#         "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", 
#         "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
#         "sixteen", "seventeen", "eighteen", "nineteen",
#       ]

#       tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

#       scales = ["hundred", "thousand", "million", "billion", "trillion"]

#       numwords["and"] = (1, 0)
#       for idx, word in enumerate(units):    numwords[word] = (1, idx)
#       for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
#       for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

#     current = result = 0
#     for word in textnum.split()

#         scale, increment = numwords[word]
#         current = current * scale + increment
#         if scale > 100:
#             result += current
#             current = 0

#     return result + current    

# print(text2int(result))

# Microsoft Bing Voice Recognition thinks you said ford junk vernon miles at eight zero zero bella rosa street suite three zero zero san antonio texas seven eight two zero seven your next individual hearing date is april thirteen two thousand seventeen at one PM before it jumps vernon miles at eight zero zero delarossa street suite three zero zero san antonio texas seven eight two zero seven william next hearing date press one for case processing information