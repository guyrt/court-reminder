import pyodbc

from storage.secrets import db_connection_string, db_tablename

conn = pyodbc.connect(db_connection_string,
                      autocommit=True) 
cursor = conn.cursor()
sqlcommand = """
CREATE TABLE {db_tablename}
(
    ID int NOT NULL IDENTITY,
    AlienRegistrationNumber varchar(255) NOT NULL UNIQUE,
    Status varchar(255),
    CallID varchar(255),
    CallTimestamp datetime,
    CallTranscript varchar(max),
    CallUploadUrl varchar(2100),
    CourtHearingType varchar(124),
    CourtHearingDate varchar(512),
    CourtHearingLocation varchar(1024),
    CourtHearingJudgeName varchar(1024),
    LastUpdatedTimestamp datetime,
    PRIMARY KEY (ID)
)
             """.format(db_tablename=db_tablename)

cursor.execute(sqlcommand)
cursor.commit()
conn.commit()
