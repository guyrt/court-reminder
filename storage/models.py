"""
Handles database reads and updates
"""

import pyodbc

from storage.secrets import db_connection_string, db_tablename


class NoRecordsToProcessError(Exception):
    pass


class Statuses(object):

    new = "new"
    calling = "calling"
    recording_ready = "recording_ready"


class Database(object):

    def __init__(self):
        self.connection = pyodbc.connect(db_connection_string)

    def retrieve_next_record_for_call(self):
        """
        Retrieve a set of records that need a phone call
        """
        cursor = self.connection.cursor()

        # todo: make this transactional to avoid double work select and update
        select_query = """
            SELECT TOP 1 AlienRegistrationNumber
            FROM {table}
            WHERE Status = 'new'
            ORDER BY LastUpdatedTimestamp asc
        """.format(table=db_tablename)

        # Get the sid from the transaction
        result = cursor.execute(select_query)
        rows = result.fetchall()

        if not rows:
            raise NoRecordsToProcessError()

        ain = rows[0][0]

        update_query = """
            UPDATE {table}
            SET Status = '{status}'
            WHERE AlienRegistrationNumber = ?
        """.format(table=db_tablename, status=Statuses.calling)

        # update the number
        cursor.execute(update_query, ain)
        self.connection.commit()

        return ain

    def upload_new_requests(self, request_ids):
        """
        Upload new request ids to the database
        """

        insert_query = """
        BEGIN
            IF NOT EXISTS (
                SELECT * 
                FROM {table}
                WHERE AlienRegistrationNumber = ?
            )

            BEGIN
                INSERT INTO {table}
                (AlienRegistrationNumber, Status)
                VALUES (?, '{status}')
            END
        END
        """.format(table=db_tablename, status=Statuses.new)

        cursor = self.connection.cursor()
        for id in request_ids:
            cursor.execute(insert_query, id, id)
            self.connection.commit()

    def update_call_id(self, alien_registration_id, call_id):

        update_query = """
        UPDATE {table}
        SET 
            Status = '{status}',
            CallID = ?,
            CallTimestamp = CURRENT_TIMESTAMP
        WHERE AlienRegistrationNumber = ?
        """.format(table=db_tablename, status=Statuses.calling)

        cursor = self.connection.cursor()
        cursor.execute(update_query, call_id, alien_registration_id)
        self.connection.commit()

    def update_azure_path(self, alien_registration_id, azure_path):
        update_query = """
        UPDATE {table}
        SET 
            Status = '{status}',
            CallUploadUrl = ?
        WHERE AlienRegistrationNumber = ?
        """.format(table=db_tablename, status=Statuses.recording_ready)

        cursor = self.connection.cursor()
        cursor.execute(update_query, azure_path, alien_registration_id)
