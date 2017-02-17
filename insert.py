import sys
from storage.models import Database

if len(sys.argv) != 2:
    print("Usage: python insert.py <file>  # file should contain one A Number per line.")
    sys.exit(1)

alien_numbers = [line.strip() for line in open(sys.argv[1])]
db = Database()
db.upload_new_requests(alien_numbers)
