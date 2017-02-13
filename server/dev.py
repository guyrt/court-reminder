"""
Expose flask app in debug mode for dev purpose
"""

from app import app
app.run(port=8080, debug=True, processes=1)
