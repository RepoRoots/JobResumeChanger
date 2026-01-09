#!/usr/bin/env python3
"""
One-Click Setup Script for Resume Optimizer
Just run: python setup_and_run.py
"""

import subprocess
import sys
import os
import webbrowser
import time

def main():
    print("=" * 50)
    print("  RESUME OPTIMIZER - One Click Setup")
    print("=" * 50)
    print()

    # Step 1: Install dependencies
    print("[1/3] Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "flask", "pymupdf", "python-docx", "werkzeug",
            "--quiet"
        ])
        print("      Done!")
    except Exception as e:
        print(f"      Error: {e}")
        print("      Try running: pip install flask pymupdf python-docx werkzeug")
        return

    # Step 2: Create necessary directories
    print("[2/3] Setting up directories...")
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)
    print("      Done!")

    # Step 3: Start the app
    print("[3/3] Starting the application...")
    print()
    print("=" * 50)
    print("  APP IS RUNNING!")
    print("  Open this URL in your browser:")
    print()
    print("  >>> http://localhost:5000 <<<")
    print()
    print("  Press Ctrl+C to stop")
    print("=" * 50)
    print()

    # Open browser automatically after 2 seconds
    time.sleep(2)
    webbrowser.open("http://localhost:5000")

    # Import and run Flask app
    from app import app
    app.run(debug=False, host='127.0.0.1', port=5000)

if __name__ == "__main__":
    main()
