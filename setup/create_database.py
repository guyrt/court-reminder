import pyodbc

from storage.secrets import db_connection_string, db_name

conn = pyodbc.connect(db_connection_string,
                      autocommit=True) 
cursor = conn.cursor()
sqlcommand = """
BEGIN

CREATE TABLE {db_name}
(
    ID int NOT NULL IDENTITY,
    AlienRegistrationNumber varchar(255) NOT NULL UNIQUE,
    Status varchar(255),
    CallID varchar(255),
    CallTimestamp datetime,
    CallDurationInSeconds int CHECK (CallDurationInSeconds >= 0),
    CallTranscript varchar(max),
    CallUploadUrl varchar(2100),
    CourtHearingType varchar(124),
    CourtHearingDate varchar(512),
    CourtHearingLocation varchar(1024),
    CourtHearingJudgeName varchar(1024),
    LastUpdatedTimestamp datetime DEFAULT(getdate()),
    PRIMARY KEY (ID)
)

CREATE TRIGGER dbo.autoUpdateTimestamp 
ON dbo.{db_tablename}
FOR UPDATE 
AS 
BEGIN 
    IF NOT UPDATE(LastUpdatedTimestamp) 
        UPDATE dbo.{db_tablename} SET LastUpdatedTimestamp=GETDATE() 
        WHERE col1 IN (SELECT col1 FROM inserted) 
END 
GO

END
             """.format(db_tablename=db_tablename)

cursor.execute(sqlcommand)
cursor.commit()
conn.commit()
