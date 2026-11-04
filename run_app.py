"""
KARIGAR AI - Fast Launcher Script
Problem Statement 7.1: GAVS / Tech4Bharat Hackathon 2026
Usage:
    python run_app.py
This initializes the database in MySQL (Karigar_Ai), verifies seed data,
and starts the Flask REST backend server on port 5000.
"""

import sys
import os

backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

from app import create_app
from seed import seed_database

app = create_app()

if __name__ == '__main__':
    print("=" * 75)
    print("  KARIGAR AI (कारीगर AI) - GAVS / Tech4Bharat Hackathon 2026")
    print("  AI-Powered Business Assistant for Artisans and Weavers (Problem 7.1)")
    print("  'AI Recommends. Artisans Decide.'")
    print("=" * 75)
    print("\n[1/2] Connecting to MySQL database 'Karigar_Ai'...")
    try:
        seed_database()
    except Exception as e:
        print("Notice:", e)
        
    port = int(os.environ.get('PORT', 5000))
    print(f"\n[2/2] Starting Flask Backend Server on http://localhost:{port} ...")
    print(f"      Artisan & Buyer UI can be opened directly from: frontend/public/index.html")
    print("=" * 75)
    app.run(host='0.0.0.0', port=port, debug=True)
