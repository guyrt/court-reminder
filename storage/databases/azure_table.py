from datetime import datetime
from azure.storage.table import TableService, Entity
from storage.secrets import storage_account, table_connection_string, table_name
from storage.models import Statuses, NoRecordsToProcessError


class AzureTableDatabase(object):
    def __init__(self):
        self.connection = TableService(account_name=storage_account, account_key=table_connection_string)
        self.table_name = table_name

    def create_table(self):
        self.connection.create_table(self.table_name)

    def list_calls(self, limit=100, select='PartitionKey'):
        """
        Retrieve a set of records that need a phone call
        """

        calls = self.connection.query_entities(self.table_name, num_results=limit, select=select)
        return [c.PartionKey for c in calls] 

    def retrieve_next_record_for_call(self):
        """
        Retrieve a set of records that need a phone call
        """

        records = self.connection.query_entities(self.table_name, num_results=1, filter="Status eq {0}".format(Statuses.new))

        if len(records.items) == 0:
            raise NoRecordsToProcessError()

        record = records.items[0]
        record.Status = Statuses.calling
        self.connection.update_entity(self.table_name, record)

        return record.PartitionKey

    def retrieve_next_record_for_transcribing(self):
        records = self.connection.query_entities(self.table_name, num_results=1, filter="Status eq {0}".format(Statuses.recording_ready))
        if len(records.items) == 0:
            raise NoRecordsToProcessError()
        
        record = records.item[0]
        record.Status = Statuses.transcribing
        self.connection.update_entity(self.table_name, record)

        return record.CallUploadUrl, record.PartitionKey


    def update_transcript(self, partition_key, transcript):
        record = self.connection.get_entity(self.table_name, partition_key, partition_key)
        record.CallTranscript = transcript
        record.Status = Statuses.transcribing_done
        record.TranscribeTimestamp = datetime.now()
        self.connection.update_entity(self.table_name, record)

    def upload_new_requests(self, request_ids):
        """
        Upload new request ids to the database
        """

        for request_id in request_ids:
            record = {'PartitionKey': request_id, 'RowKey': request_id, 'Status': Statuses.new}
            self.connection.insert_entity(self.table_name, record)

    def update_call_id(self, alien_registration_id, call_id):
        record = self.connection.get_entity(self.table_name, alien_registration_id, alien_registration_id)
        record.CallID = call_id
        record.Status = Statuses.calling
        record.CallTimestamp = datetime.now() 
        self.connection.update_entity(self.table_name, record)
