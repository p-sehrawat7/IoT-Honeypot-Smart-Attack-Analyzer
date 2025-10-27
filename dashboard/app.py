# dashboard/app.py
from flask import Flask, render_template, send_file, jsonify
import pandas as pd
import os
from datetime import datetime
from glob import glob

app = Flask(__name__, template_folder='templates')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)

MAP_FILE = os.path.join(REPORTS_DIR, "attack_map.html")

def get_latest_report():
    files = [f for f in os.listdir(REPORTS_DIR) if f.endswith('.csv')]
    if not files:
        return None
    return os.path.join(REPORTS_DIR, sorted(files)[-1])

def get_latest_ai_summary():
    # find latest ai_summary_*.txt
    files = glob(os.path.join(REPORTS_DIR, "ai_summary_*.txt"))
    if not files:
        return None, None
    latest = max(files, key=os.path.getctime)
    with open(latest, "r", encoding="utf-8") as f:
        text = f.read()
    return latest, text

@app.route('/')
def home():
    latest_csv = get_latest_report()
    df_html = "<p>No report available.</p>"
    if latest_csv:
        try:
            df = pd.read_csv(latest_csv)
            df_html = df.tail(10).to_html(classes='table table-dark table-striped', index=False)
        except Exception as e:
            df_html = f"<p>Error loading CSV: {e}</p>"

    ai_path, ai_text = get_latest_ai_summary()
    if ai_text is None:
        ai_text = "No AI summary found. Run analyzer/ai_summary_engine.py to generate a summary."

    return render_template('index.html', table=df_html, ai_summary=ai_text, ai_path=ai_path)

@app.route('/map')
def map_view():
    if os.path.exists(MAP_FILE):
        return send_file(MAP_FILE)
    return "No map found. Please run geo_analyzer first."

@app.route('/download_report')
def download_report():
    latest = get_latest_report()
    if not latest:
        return "No CSV reports found.", 404
    return send_file(latest, as_attachment=True)

@app.route('/download_summary')
def download_summary():
    ai_path, _ = get_latest_ai_summary()
    if not ai_path:
        return "No AI summary found.", 404
    return send_file(ai_path, as_attachment=True)

@app.route('/data')
def data():
    """Old AJAX endpoint for live table refresh (kept for compatibility)."""
    latest = get_latest_report()
    if not latest:
        return jsonify({"error": "No report found"})
    try:
        df = pd.read_csv(latest)
        df_html = df.tail(10).to_html(classes='table table-dark table-striped', index=False)
        return jsonify({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "table": df_html})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
