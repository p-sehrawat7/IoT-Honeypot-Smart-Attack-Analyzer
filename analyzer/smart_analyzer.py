import json
import pandas as pd
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "attacks.log")

REPORTS_DIR = "reports"

os.makedirs(REPORTS_DIR, exist_ok=True)

def load_logs():
    data = []
    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return data
    except FileNotFoundError:
        print("[!] Log file not found!")
        return []

def classify_attack(command):
    if not command:
        return "Unknown"
    cmd = command.lower()
    if "login" in cmd or "admin" in cmd or "password" in cmd:
        return "Brute Force Attempt"
    elif "ls" in cmd or "cat" in cmd or "dir" in cmd:
        return "Reconnaissance"
    elif "rm" in cmd or "delete" in cmd:
        return "Destruction Attempt"
    elif "wget" in cmd or "curl" in cmd:
        return "Malware Download Attempt"
    elif "reboot" in cmd or "shutdown" in cmd:
        return "System Disruption Attempt"
    else:
        return "General Probe"

def analyze_logs():
    logs = load_logs()
    if not logs:
        print("[!] No logs found.")
        return

    df = pd.DataFrame(logs)

    if 'command' not in df.columns:
        print("[!] Command column missing — check honeypot logs format.")
        return

    # Add attack classification
    df["attack_type"] = df["command"].apply(classify_attack)

    # Convert timestamp to datetime
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    print("\n===== SMART ATTACK ANALYZER =====")
    print(f"Total Attacks Detected: {len(df)}")
    print("\nAttack Categories:")
    print(df["attack_type"].value_counts())

    print("\nMost Common Commands:")
    print(df["command"].value_counts().head(10))

    csv_path = os.path.join(REPORTS_DIR, f"smart_report_{datetime.now():%Y%m%d_%H%M%S}.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[+] Smart report saved to: {csv_path}")

if __name__ == "__main__":
    analyze_logs()
