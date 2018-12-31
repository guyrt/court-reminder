import sys
from storage.models import Database

if len(sys.argv) != 2:
    print("Usage: python insert.py <file>  # file should contain one A Number per line.")
    sys.exit(1)

alien_numbers = [line.strip().replace('-', '') for line in open(sys.argv[1])]
db = Database()
db.create_table() # checks if already exists
db.upload_new_requests(alien_numbers)
