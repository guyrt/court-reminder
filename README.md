# court-reminder
Calling things and transcribing.

# Setup
pip install -r requirement.txt

# Run
Two parts: 
1. Running the runners (transcribing, calling, extracting)
  - python runners.py
2. Running the servers (twiml server, admin server)
  - python run_server.py --twilio_prod
  - python run_server.py --admin_prod
