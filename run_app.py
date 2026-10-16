"""
Native Python Launcher for ZIZIPHUS JUJUBA Laboratory.
Crash-proof runner: handles database verification, delayed browser opening,
and launches the Uvicorn web server.
"""

import sys
import pathlib
import threading
import time
import webbrowser

BASE_DIR = pathlib.Path(__file__).parent.resolve()
DB_FILE = BASE_DIR / "data/database/ziziphus_jujuba.db"

def open_browser():
    time.sleep(1.5)
    print("\n[ZIZIPHUS JUJUBA] Opening lab in default web browser...")
    webbrowser.open("http://127.0.0.1:8765")

def main():
    print("=" * 70)
    print("       ZIZIPHUS JUJUBA : SIGNAL INTELLIGENCE & PATTERN LAB")
    print("=" * 70)
    print(f"Working directory: {BASE_DIR}")
    print(f"Python interpreter: {sys.executable}")
    
    # 1. Check if database exists
    if not DB_FILE.exists():
        print("\n[INIT] Database not found. Building dataset from primary logs...")
        from src.ingestion.build_dataset import run_pipeline
        run_pipeline()
    else:
        print("[INIT] Normalized SQLite database verified.")

    # 2. Start browser opener thread
    threading.Thread(target=open_browser, daemon=True).start()

    # 3. Start server
    print("[SERVER] Starting local server at http://127.0.0.1:8765 ...")
    print("[SERVER] Press Ctrl+C in this window to stop the server.\n")
    
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8765, log_level="info")

if __name__ == "__main__":
    main()
