class TemporaryChillError(Exception):

    def __init__(self, numseconds):
        self.pause_time = numseconds

class TooManyErrorsException(Exception):
	pass

class TranscriptionError(Exception):
	pass

class TwilioResponseError(Exception):
	pass

class EntityExtractionError(Exception):
    pass
