class TemporaryChillError(Exception):

    def __init__(self, numseconds):
        self.pause_time = numseconds