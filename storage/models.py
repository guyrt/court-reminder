"""
Handles database reads and updates
"""

class NoRecordsToProcessError(Exception):
    pass


class Statuses(object):
    new = "new"
    calling = "calling"
    recording_ready = "recording_ready"


from storage.databases.azure_table import AzureTableDatabase as Database
