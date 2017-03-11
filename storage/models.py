"""
Handles database reads and updates
"""

class NoRecordsToProcessError(Exception):
    pass


class Statuses(object):
    new = "new"
    calling = "calling"
    recording_ready = "recording_ready"
    transcribing = "transcribing_recording"
    transcribing_done = "transcribing_completed"
    extracting = "extracting_info"
    extracting_done = "extracting_done"
    error = "error"

from storage.databases.azure_table import AzureTableDatabase as Database
