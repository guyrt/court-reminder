# court-reminder
Calling things and transcribing.

# Setup
pip install -r requirement.txt

Secrets files (these contain API keys, lists of numbers for which you want info):
  1. Storage
  2. Server
  3. Transcription
  4. Call
 You want to copy secrets sample and then fill in the blanks.

# Run
Two parts: 
1. Running the runners (transcribing, calling, extracting)
  - python ./court-reminder/runners.py
2. Running the servers (twiml server, admin server)
  - python run_server.py --twilio_prod
  - python run_server.py --admin_prod
