import os
import sys

# Ensure backend directory is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from seed import seed_database

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting KARIGAR AI Backend Server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
