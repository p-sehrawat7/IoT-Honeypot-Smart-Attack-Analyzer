import os
import json
import pandas as pd
import requests
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "attacks.log")

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# Optional: set your free AbuseIPDB key (if available)
ABUSE_IPDB_API_KEY = ""  # Add key here if you have one

def load_logs():
    """Load honeypot logs as DataFrame."""
    if not os.path.exists(LOG_FILE):
        print("[!] No logs found.")
        return pd.DataFrame()
    
    data = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                data.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    return pd.DataFrame(data)

def check_ip_reputation(ip):
    """Query AbuseIPDB API if key is available, else use mock scoring."""
    if not ip:
        return {"score": 0, "confidence": 0, "country": "Unknown", "isp": "Unknown"}

    if ABUSE_IPDB_API_KEY:
        try:
            url = f"https://api.abuseipdb.com/api/v2/check"
            headers = {"Key": ABUSE_IPDB_API_KEY, "Accept": "application/json"}
            params = {"ipAddress": ip, "maxAgeInDays": "90"}
            res = requests.get(url, headers=headers, params=params)
            if res.status_code == 200:
                data = res.json()["data"]
                return {
                    "score": data.get("abuseConfidenceScore", 0),
                    "confidence": data.get("totalReports", 0),
                    "country": data.get("countryCode", "Unknown"),
                    "isp": data.get("isp", "Unknown")
                }
        except Exception as e:
            print(f"[x] Reputation API failed for {ip}: {e}")
            pass

    # Fallback mock scoring based on heuristics
    octets = ip.split(".")
    risk = int(octets[-1]) % 100 if len(octets) == 4 else 0
    return {
        "score": risk,
        "confidence": risk // 10,
        "country": "MockLand",
        "isp": "UnknownISP"
    }

def compute_threat_score(row):
    """Weighted score based on multiple factors."""
    score = 0

    # Command-based risk
    cmd = str(row.get("command", "")).lower()
    if any(k in cmd for k in ["wget", "curl", "rm", "shutdown", "reboot"]):
        score += 40
    elif any(k in cmd for k in ["ls", "cat", "dir", "whoami"]):
        score += 10
    elif any(k in cmd for k in ["login", "password", "admin"]):
        score += 25

    # Port-based risk
    port = int(row.get("port", 0))
    if port in [22, 23, 445, 3389]:
        score += 20

    # Add IP reputation
    rep = row.get("reputation_score", 0)
    score += rep * 0.8  # weight factor

    # Confidence scaling
    score = min(100, score)
    return round(score, 2)

def correlate_threats():
    df = load_logs()
    if df.empty:
        print("[!] No logs found to correlate.")
        return

    unique_ips = df["source_ip"].unique()
    print(f"[*] Correlating {len(unique_ips)} unique IPs...")

    rep_data = []
    for ip in unique_ips:
        rep = check_ip_reputation(ip)
        rep_data.append({
            "source_ip": ip,
            **rep
        })

    rep_df = pd.DataFrame(rep_data)
    df = df.merge(rep_df, on="source_ip", how="left")

    # Compute threat scores
    df["threat_score"] = df.apply(compute_threat_score, axis=1)

    # Risk Category
    df["risk_level"] = pd.cut(
        df["threat_score"],
        bins=[0, 30, 60, 100],
        labels=["Low", "Medium", "High"]
    )

    print("\n=== THREAT INTELLIGENCE CORRELATOR ===")
    print(df[["timestamp", "source_ip", "country", "command", "threat_score", "risk_level"]].head(10))

    # Save Report
    csv_path = os.path.join(REPORTS_DIR, f"threat_correlation_{datetime.now():%Y%m%d_%H%M%S}.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[+] Threat intelligence report saved: {csv_path}")

    # Summary
    print("\nRisk Distribution:")
    print(df["risk_level"].value_counts())

if __name__ == "__main__":
    correlate_threats()