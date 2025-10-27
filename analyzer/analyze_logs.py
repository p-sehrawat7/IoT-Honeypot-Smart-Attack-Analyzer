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
                    except json.JSONDecodeError as e:
                        print(f"[!] Skipping bad JSON: {e}")
        return data
    except FileNotFoundError:
        print(f"[!] Log file not found: {LOG_FILE}")
        return []

def analyze_logs():
    logs = load_logs()
    if not logs:
        print("[!] No logs found.")
        return

    df = pd.DataFrame(logs)

    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    print("\n===== ATTACK SUMMARY =====")
    print(f"Total attack attempts: {len(df)}")

    if 'ip' in df.columns:
        print("\nTop Attacker IPs:")
        print(df['ip'].value_counts().head(10))

    if 'command' in df.columns:
        print("\nMost Common Commands:")
        print(df['command'].value_counts().head(10))

    csv_path = os.path.join(REPORTS_DIR, f"attack_report_{datetime.now():%Y%m%d_%H%M%S}.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[+] Report saved to: {csv_path}")

if __name__ == "__main__":
    analyze_logs()