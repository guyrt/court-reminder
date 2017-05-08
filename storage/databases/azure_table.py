from datetime import datetime

from azure.common import AzureConflictHttpError
from azure.storage.table import TableService
from storage.secrets import storage_account, table_connection_string, table_name
from storage.models import Statuses, NoRecordsToProcessError
from transcribe.transcribe import TranscriptionStatus


class AzureTableDatabase(object):
    def __init__(self):
        self.connection = TableService(account_name=storage_account, account_key=table_connection_string)
        self.table_name = table_name

    def _update_entity(self, record):
        record.LastModified = datetime.now()
        self.connection.update_entity(self.table_name, record)

    def create_table(self):
        self.connection.create_table(self.table_name)

    def raw_table(self, limit=100):
        """
        Retrieve a list of rows in the table.
        """
        calls = self.connection.query_entities(self.table_name, num_results=limit)
        return calls

    def list_calls(self, limit=100, select='PartitionKey'):
        """
        Retrieve a set of records that need a phone call
        """

        calls = self.connection.query_entities(self.table_name, num_results=limit, select=select)
        return [c.PartitionKey for c in calls]

    def reset_stale_calls(self, time_limit):
        """
        Retrieve calls that are not done and whose last modified time was older than the limit.
        """
        records = self.connection.query_entities(self.table_name, filter="LastModified lt datetime'{0}' and Status ne '{1}'".format(time_limit.date(), Statuses.extracting_done))
        if not records.items:
            raise NoRecordsToProcessError()
        num_records = len(records.items)

        for record in records:
            if 'LastErrorStep' in record:
                record.Status = record.LastErrorStep
                del record.LastErrorStep
            record.Status = Statuses.reset_map.get(record.Status, record.Status)
            self._update_entity(record)

        return num_records

    def retrieve_next_record_for_call(self):
        """
        Retrieve a set of records that need a phone call
        """

        records = self.connection.query_entities(self.table_name, num_results=1, filter="Status eq '{0}'".format(Statuses.new))

        if len(records.items) == 0:
            raise NoRecordsToProcessError()

        record = records.items[0]
        record.Status = Statuses.calling
        self._update_entity(record)

        return record.PartitionKey

    def set_error(self, partition_key, step):
        """ Reset a row from error state
        """
        record = self.connection.get_entity(self.table_name, partition_key, partition_key)
        record.Status = Statuses.error
        record['LastErrorStep'] = step
        self._update_entity(record)

    def retrieve_next_record_for_transcribing(self):
        records = self.connection.query_entities(
            self.table_name,
            num_results=1,
            filter="Status eq '{0}'".format(Statuses.recording_ready),
        )
        if not records.items:
            raise NoRecordsToProcessError()

        record = records.items[0]
        record.Status = Statuses.transcribing
        self._update_entity(record)

        return record.CallUploadUrl, record.PartitionKey

    def update_transcript(self, partition_key, transcript, status):
        record = self.connection.get_entity(
            self.table_name,
            partition_key,
            partition_key,
        )
        if status == TranscriptionStatus.success:
            record.CallTranscript = transcript
            record.Status = Statuses.transcribing_done
            record.TranscribeTimestamp = datetime.now()
            self._update_entity(record)
        elif status == TranscriptionStatus.request_error:
            self.set_error(partition_key, Statuses.transcribing)
        else:
            record.Status = Statuses.transcribing_failed
            self._update_entity(record)

    def change_status(self, original_status, new_status):
        records = self.connection.query_entities(
            self.table_name,
            filter="Status eq '{0}'".format(original_status),
        )
        if not records.items:
            return

        for record in records.items:
            record.Status = new_status
            self.connection.update_entity(self.table_name, record)

    def query(self, column, value, limit=1):
        records = self.connection.query_entities(self.table_name, 
              num_results=limit, filter="{0} eq '{1}'".format(column, value))
        return records

    def retrieve_next_record_for_extraction(self):
        records = self.connection.query_entities(self.table_name, num_results=1, filter="Status eq '{0}'".format(Statuses.transcribing_done))
        if not records.items:
            raise NoRecordsToProcessError()

        record = records.items[0]
        record.Status = Statuses.extracting
        self._update_entity(record)

        return record.CallTranscript, record.PartitionKey

    def update_location_date(self, partition_key, location_dict, date_dict):
        record = self.connection.get_entity(self.table_name, partition_key, partition_key)
        if location_dict and date_dict:
            record.update(**location_dict)
            record.update(**date_dict)
            record.Status = Statuses.extracting_done
        else:
            record.Status = Statuses.failed_to_return_info
        self._update_entity(record)

    def upload_new_requests(self, request_ids):
        """
        Upload new request ids to the database
        """

        for request_id in request_ids:
            record = {'PartitionKey': request_id, 'RowKey': request_id, 'Status': Statuses.new, 'LastModified': datetime.now()}
            try:
                self.connection.insert_entity(self.table_name, record)
            except AzureConflictHttpError:
                pass  # already exists. silently ignore.

    def update_call_id(self, alien_registration_id, call_id):
        record = self.connection.get_entity(self.table_name, alien_registration_id, alien_registration_id)
        record.CallID = call_id
        record.Status = Statuses.calling
        record.CallTimestamp = datetime.now()
        self._update_entity(record)

    def update_azure_path(self, alien_registration_id, azure_path):
        record = self.connection.get_entity(self.table_name, alien_registration_id, alien_registration_id)
        record.Status = Statuses.recording_ready
        record.CallUploadUrl = azure_path
        self._update_entity(record)

    def delete_ain(self, ain):
        return self.connection.delete_entity(self.table_name, ain, ain)

    def get_ain(self, ain):
        return self.connection.get_entity(self.table_name, ain, ain)
