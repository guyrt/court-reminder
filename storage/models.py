"""
Handles database reads and updates
"""

class NoRecordsToProcessError(Exception):
    pass


class Statuses(object):
    """
    These are the status in order for a single run.
    """
    new = "new"
    calling = "calling"
    recording_ready = "recording_ready"
    transcribing = "transcribing_recording"
    transcribing_failed = "transcribing_failed"
    transcribing_done = "transcribing_completed"
    extracting = "extracting_info"
    extracting_done = "extracting_done"
    error = "error"
    failed_to_return_info = "failed_to_return_info"

Statuses.reset_map = {
    Statuses.calling: Statuses.new,
    Statuses.transcribing: Statuses.recording_ready,
    Statuses.extracting: Statuses.transcribing_done,
}

from storage.databases.azure_table import AzureTableDatabase as Database
