"""
Handles database reads and updates
"""

import secrets
import pyodbc


class NoRecordsToProcessError(Exception):
    pass


class Database(object):

    def __init__(self):
        self.connection = pyodbc.connect(secrets.db_connection_string)

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
        """.format(table=db_name)

        # Get the sid from the transaction

        if True:  # change to if don't have a sid
            raise NoRecordsToProcessError()

        update_query = """
            UPDATE {table}
            SET status = "calling"
            WHERE sid = ?
        """.format(table=db_name)

        # update the sid

        #return side
