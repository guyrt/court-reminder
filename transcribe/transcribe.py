#!/usr/bin/env python3
import sys
import speech_recognition as sr
from transcribe.secrets import (
    bing_speech_api_key,
    google_credentials_json,
    google_preferred_phrases,
)

class TranscriptionStatus(object):
    success = "success"
    request_error = "request error"
    transcription_error = "unintelligible audio"
    unknown_error = "unknown error"


class BingTranscriber(object):

    def __init__(self):
        self.bing_key = bing_speech_api_key
        self.language = "en-US"

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
                return self.transcribe_audio_object(audio), TranscriptionStatus.success
        except sr.UnknownValueError as e:
            print("{0}".format(e))


class GoogleTranscriber(object):

    def __init__(self):
        self.google_creds = google_credentials_json
        self.language = "en-US"
        self.preferred_phrases = google_preferred_phrases

    def transcribe_audio_file_path(self, audio_file_path):
        r = sr.Recognizer()
        transcript = ""
        transcription_status = TranscriptionStatus.success
        with sr.AudioFile(audio_file_path) as source:
            audio_object = r.record(source)
            try:
                transcript = r.recognize_google_cloud(
                    audio_data=audio_object,
                    credentials_json=self.google_creds,
                    language=self.language,
                    preferred_phrases=self.preferred_phrases,
                    show_all=False,
                )
            except sr.UnknownValueError as e:
                transcription_status = TranscriptionStatus.transcription_error
                print("Google Cloud Speech could not understand audio: {0}".format(e))
            except sr.RequestError as e:
                transcription_status = TranscriptionStatus.request_error
                print("Could not request results from Google Cloud Speech "
                      "service; {0}".format(e))
            except:
                print("Unknown transcription error:", sys.exc_info())
                transcription_status = TranscriptionStatus.unknown_error
        return transcript, transcription_status
