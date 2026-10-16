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

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def get_base_dir() -> pathlib.Path:
    if getattr(sys, 'frozen', False):
        exe_dir = pathlib.Path(sys.executable).parent.resolve()
        if (exe_dir / "data/database/ziziphus_jujuba.db").exists():
            return exe_dir
        if (exe_dir / "_internal/data/database/ziziphus_jujuba.db").exists():
            return exe_dir / "_internal"
        if hasattr(sys, '_MEIPASS'):
            meipass = pathlib.Path(sys._MEIPASS).resolve()
            if (meipass / "data/database/ziziphus_jujuba.db").exists():
                return meipass
        return exe_dir
    return pathlib.Path(__file__).parent.resolve()

BASE_DIR = get_base_dir()
DB_FILE = BASE_DIR / "data/database/ziziphus_jujuba.db"

def is_server_already_running(port: int = 8765) -> bool:
    import urllib.request
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{port}/api/overview", headers={"User-Agent": "ZiziphusLauncher"})
        with urllib.request.urlopen(req, timeout=1.0) as resp:
            return resp.status == 200
    except Exception:
        return False

def open_browser(port: int = 8765):
    time.sleep(1.5)
    print("\n[ZIZIPHUS JUJUBA] Opening lab in default web browser...")
    webbrowser.open(f"http://127.0.0.1:{port}")

def main():
    print("=" * 70)
    print("       ZIZIPHUS JUJUBA : SIGNAL INTELLIGENCE & PATTERN LAB")
    print("=" * 70)
    print(f"Working directory: {BASE_DIR}")
    print(f"Python interpreter: {sys.executable}")

    # 0. Check if already running
    if is_server_already_running(8765):
        print("\n" + "=" * 70)
        print(" [INFO] ZIZIPHUS JUJUBA уже запущен и работает в фоновом режиме!")
        print(" [INFO] Адрес: http://127.0.0.1:8765")
        print(" [INFO] Открываем лабораторию в браузере...")
        print("=" * 70 + "\n")
        webbrowser.open("http://127.0.0.1:8765")
        time.sleep(2)
        return

    # 1. Check if database exists
    if not DB_FILE.exists():
        print("\n[INIT] Database not found. Building dataset from primary logs...")
        from src.ingestion.build_dataset import run_pipeline
        run_pipeline()
    else:
        print("[INIT] Normalized SQLite database verified.")

    # 2. Start browser opener thread
    threading.Thread(target=open_browser, args=(8765,), daemon=True).start()

    # 3. Start server
    print("[SERVER] Starting local server at http://127.0.0.1:8765 ...")
    print("[SERVER] Press Ctrl+C in this window to stop the server.\n")
    
    import uvicorn
    from app.main import app
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="info")

if __name__ == "__main__":
    main()
