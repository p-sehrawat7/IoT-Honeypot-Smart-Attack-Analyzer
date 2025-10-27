import os
import pandas as pd
from glob import glob
from datetime import datetime

REPORTS_DIR = "reports"
OUTPUT_FILE = os.path.join(REPORTS_DIR, f"ai_summary_{datetime.now():%Y%m%d_%H%M%S}.txt")

def load_latest_report():
    """Load the most recent CSV report."""
    files = glob(os.path.join(REPORTS_DIR, "*.csv"))
    if not files:
        print("[!] No reports found to analyze.")
        return None
    latest = max(files, key=os.path.getctime)
    print(f"[+] Loaded latest report: {latest}")
    return pd.read_csv(latest)

def summarize_attacks(df):
    """Generate a human-readable summary of attack patterns."""
    summary = []
    total_attacks = len(df)

    summary.append(f"📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append(f"⚔️ Total Attack Attempts: {total_attacks}")

    if 'source_ip' in df.columns:
        top_ips = df['source_ip'].value_counts().head(5)
        summary.append("\n🌍 Top Attacker IPs:")
        for ip, count in top_ips.items():
            summary.append(f"  - {ip} ➜ {count} attempts")

    if 'attack_type' in df.columns:
        top_attacks = df['attack_type'].value_counts()
        summary.append("\n🧠 Attack Type Breakdown:")
        for atype, count in top_attacks.items():
            pct = (count / total_attacks) * 100
            summary.append(f"  - {atype}: {count} ({pct:.1f}%)")

    if 'country' in df.columns:
        top_countries = df['country'].value_counts().head(5)
        summary.append("\n🌎 Top Source Countries:")
        for c, count in top_countries.items():
            summary.append(f"  - {c}: {count} attacks")

    if 'command' in df.columns:
        common_cmds = df['command'].value_counts().head(5)
        summary.append("\n💻 Most Common Commands:")
        for cmd, count in common_cmds.items():
            summary.append(f"  - {cmd} ➜ {count} times")

    # Simple intelligence logic
    summary.append("\n🧩 AI Threat Intelligence Summary:")
    if 'attack_type' in df.columns:
        if (df['attack_type'] == 'Brute Force Attempt').sum() > (0.3 * total_attacks):
            summary.append("  ⚠️ High number of brute-force attempts detected — consider blocking suspicious IPs.")
        if (df['attack_type'] == 'Malware Download Attempt').sum() > 0:
            summary.append("  🚨 Potential malware distribution attempt detected — inspect payloads carefully.")
        if (df['attack_type'] == 'Reconnaissance').sum() > (0.2 * total_attacks):
            summary.append("  🕵️ Numerous reconnaissance commands — possible scanning activity.")
        else:
            summary.append("  ✅ No major anomalies detected; system appears stable.")

    return "\n".join(summary)

def main():
    df = load_latest_report()
    if df is None:
        return

    summary_text = summarize_attacks(df)

    # Save to text file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(summary_text)

    print(f"\n[+] AI Threat Summary saved to: {OUTPUT_FILE}")
    print("\n===== AI SUMMARY PREVIEW =====\n")
    print(summary_text)

if __name__ == "__main__":
    main()
