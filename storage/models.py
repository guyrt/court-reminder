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
        # todo: make this transactional to avoid double work select and update
        select_query = """
            SELECT TOP 1 sid 
            FROM {table}
            WHERE status == "new"
            ORDER BY last_modified
        """.format(table=secrets.db_tablename)

        # Get the sid from the transaction

        if True:  # change to if don't have a sid
            raise NoRecordsToProcessError()

        update_query = """
            UPDATE {table}
            SET status = "calling"
            WHERE sid = ?
        """.format(table=db_tablename)

        # update the sid

        #return side

    def upload_new_requests(self, request_ids):
        """
        Upload new request ids to the database
        """

        insert_query = """
        BEGIN
            IF NOT EXISTS (
                SELECT * 
                FROM {table}
                WHERE AlientRegistrationNumber = ?
            )

            BEGIN
                INSERT INTO {table}
                (AlientRegistrationNumber, Status)
                VALUES (?, '{status}')
            END
        END
        """.format(table=db_tablename, status=Statuses.new)

        cursor = self.connection.cursor()
        for id in request_ids:
            cursor.execute(insert_query, id, id)
            self.connection.commit()
