# IoT Honeypot + Smart Attack Analyzer

**Short:** A Telnet-like IoT honeypot that captures attacker activity, enriches it (geo + threat intelligence), runs smart analysis (classification + anomaly detection), and shows results on a Flask dashboard. Includes an automated pipeline to run analyzers when new logs arrive.

## Features
- Fake Telnet honeypot that logs attacker commands and metadata
- Log parser and CSV report generation
- Geo-IP enrichment and interactive map
- Smart classification of commands (recon, brute force, malware fetch, etc.)
- Threat intelligence correlator (reputation scoring, weighted threat score)
- AI summary engine that writes human-readable SOC-like summaries
- Flask dashboard showing live logs, AI summary, and map
- Pipeline watcher to auto-run analyzers on new logs and open dashboard

## Quick start (Windows)
1. Clone:
```bash
git clone <your-repo-url>
cd IOT_HON_SMAR_ATT_ANALYZER
