import json
import pandas as pd
import requests
import os
from datetime import datetime
import plotly.express as px

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "attacks.log")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Make sure reports folder exists
os.makedirs(REPORTS_DIR, exist_ok=True)

def load_logs():
    data = []
    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                try:
                    data.append(json.loads(line.strip()))
                except:
                    continue
    except FileNotFoundError:
        print(f"[!] Log file not found at {LOG_FILE}")
        return pd.DataFrame()
    return pd.DataFrame(data)

def get_location(ip):
    """Fetch location data for a given IP address."""
    try:
        # Skip private or localhost IPs
        if ip.startswith("192.") or ip.startswith("10.") or ip.startswith("172.") or ip == "127.0.0.1":
            return None
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=country,regionName,city,lat,lon,status")
        info = response.json()
        if info.get("status") == "success":
            return info
        else:
            return None
    except Exception as e:
        print(f"[!] Geo lookup failed for {ip}: {e}")
        return None

def analyze_geo():
    df = load_logs()
    if df.empty or "source_ip" not in df.columns:
        print("[!] No IPs found in logs.")
        return

    # Fetch and attach location info
    df["location"] = df["source_ip"].apply(get_location)
    df = df.dropna(subset=["location"])

    # Extract fields
    df["country"] = df["location"].apply(lambda x: x["country"])
    df["region"] = df["location"].apply(lambda x: x["regionName"])
    df["city"] = df["location"].apply(lambda x: x["city"])
    df["lat"] = df["location"].apply(lambda x: x["lat"])
    df["lon"] = df["location"].apply(lambda x: x["lon"])

    # Save updated report
    csv_path = os.path.join(REPORTS_DIR, f"geo_report_{datetime.now():%Y%m%d_%H%M%S}.csv")
    df.to_csv(csv_path, index=False)
    print(f"[+] Geo Report saved to: {csv_path}")

    # 🌍 Create map visualization
    fig = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        hover_name="source_ip",
        hover_data=["country", "city", "command"],
        title="🌍 Attacker Locations Map",
        projection="natural earth"
    )

    # 💾 Save interactive map HTML for dashboard
    map_path = os.path.join(REPORTS_DIR, "attack_map.html")
    fig.write_html(map_path)
    print(f"[+] Attack map saved to: {map_path}")

    # Also show map live for local viewing
    fig.show()

if __name__ == "__main__":
    analyze_geo()
