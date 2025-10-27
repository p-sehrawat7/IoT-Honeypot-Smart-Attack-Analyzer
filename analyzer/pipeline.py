import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import webbrowser
import threading

# ✅ Correct paths based on your folder structure
LOG_FILE = "../logs/attacks.log"

DASHBOARD_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dashboard", "app.py")

DASHBOARD_URL = "http://127.0.0.1:5000"  # Flask default URL
dashboard_running = False  # Prevents multiple launches


class LogChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("attacks.log"):
            print("\n🚨 New attack detected! Running analysis pipeline...\n")
            run_pipeline()


def run_pipeline():
    global dashboard_running
    try:
        print("[1/4] 🌍 Running Geo Analyzer...")
        subprocess.run(["python", "analyzer/geo_analyzer.py"], check=True)

        print("[2/4] 🧠 Running Smart Analyzer...")
        subprocess.run(["python", "analyzer/smart_analyzer.py"], check=True)

        print("[3/4] 🛰️ Running Threat Intelligence Correlator...")
        subprocess.run(["python", "analyzer/threat_intel_correlater.py"], check=True)

        print("[4/4] 🧾 Running AI Summary...")
        subprocess.run(["python", "analyzer/ai_summary.py"], check=True)

        # Launch dashboard once (if not already running)
        if not dashboard_running:
            dashboard_running = True
            print("\n🚀 Launching Flask Dashboard...")
            threading.Thread(target=run_dashboard, daemon=True).start()
            time.sleep(3)
            webbrowser.open(DASHBOARD_URL)

        print("\n✅ Pipeline completed successfully.\n")

    except Exception as e:
        print(f"[!] Pipeline error: {e}")


def run_dashboard():
    try:
        subprocess.run(["python", DASHBOARD_PATH])
    except Exception as e:
        print(f"[!] Dashboard launch error: {e}")


if __name__ == "__main__":
    print("⚙️ IoT Honeypot Smart Pipeline Started")
    print(f"📡 Watching for new attacks in: {LOG_FILE}")
    print("------------------------------------------------\n")

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # 🧠 TEMPORARY MODE (Run pipeline immediately for testing/demo)
    run_pipeline()

    # 🕵️‍♂️ REAL-TIME MODE (commented out for now)
    """
    event_handler = LogChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(LOG_FILE), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Pipeline stopped manually.")
    observer.join()
    """
