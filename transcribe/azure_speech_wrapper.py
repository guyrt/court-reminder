import sys
import azure.cognitiveservices.speech as speechsdk
from transcribe.secrets import (
    azure_speech_key,
)
from transcribe.transcribe import TranscriptionStatus

class AzureTranscriber(object):
    """
    Wrapper for the Azure speech to text service.

    See
    https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/quickstart-python
    """

    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(subscription=azure_speech_key, region="westus")

    def transcribe_audio_file_path(self, audio_file_path):
        # For now supports wav, not mp3
        # https://stackoverflow.com/questions/51614216/what-audio-formats-are-supported-by-azure-cognitive-services-speech-service-ss?rq=1
        audio_config = speechsdk.AudioConfig(use_default_microphone=False, filename=audio_file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        transcript = ""
        transcription_status = TranscriptionStatus.success
        try:
            result = speech_recognizer.recognize_once()
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                transcript = result.text

            elif result.reason == speechsdk.ResultReason.NoMatch:
                transcription_status = TranscriptionStatus.transcription_error

            elif result.reason == speechsdk.ResultReason.Canceled:
                transcription_status = TranscriptionStatus.unknown_error

        except:
            print("Unknown transcription error:", sys.exc_info())
            transcription_status = TranscriptionStatus.unknown_error

        return transcript, transcription_status
