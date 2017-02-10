import pyodbc

from storage.secrets import db_connection_string
conn = pyodbc.connect(db_connection_string,
                      autocommit=True) 
cursor = conn.cursor()
sqlcommand = """
                   CREATE TABLE CourtHearings
(
ID int NOT NULL AUTO_INCREMENT,
AlientRegistrationNu
mber varchar(255) NOT NULL UNIQUE,
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
             """
cursor.execute(sqlcommand)
cursor.commit()
conn.commit()


