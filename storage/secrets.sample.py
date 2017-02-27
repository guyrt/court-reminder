# SQL Server
db_name = "database"
db_username = "usre@machine"
db_password = "americawasgreatalready"
db_server = "tcp:somemachine,1433"
_driver = "{ODBC Driver 13 for SQL Server}"
db_tablename = "tablaname"
db_connection_string = "Driver={driver};Server={server};Database={database};Uid={db_username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(server=db_server, driver=_driver, database=db_name, db_username=db_username, password=db_password)

# Azure Table
table_name = 'tablename'
storage_account = 'account'
table_connection_string = 'connectionstring'

# Used for azure blob store, where we upload raw files.
blob_accountmae = "court"
blob_key = "mah_blob"
blob_container = "somecontainer"
local_tmp_dir = "/tmp"

# sentry
sentry_dsn = ''
