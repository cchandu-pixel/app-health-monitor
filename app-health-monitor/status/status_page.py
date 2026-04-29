from flask import Flask
import json
import datetime
import requests

app = Flask(__name__)

SERVICES = [
    {"name": "user-service",         "url": "http://localhost:5001/health"},
    {"name": "order-service",        "url": "http://localhost:5002/health"},
    {"name": "payment-service",      "url": "http://localhost:5003/health"},
    {"name": "inventory-service",    "url": "http://localhost:5004/health"},
    {"name": "notification-service", "url": "http://localhost:5005/health"},
]

def check_service(service):
    try:
        response = requests.get(service["url"], timeout=3)
        if response.status_code == 200:
            return "UP"
        return "DOWN"
    except:
        return "DOWN"

def load_uptime():
    try:
        with open("docs/uptime_data.json", "r") as f:
            return json.load(f)
    except:
        return {}

@app.route('/')
def status_page():
    uptime_data = load_uptime()
    services_status = []

    for service in SERVICES:
        status = check_service(service)
        uptime_pct = 0
        if service["name"] in uptime_data:
            data = uptime_data[service["name"]]
            if data["total_checks"] > 0:
                uptime_pct = (data["successful_checks"] / data["total_checks"] * 100)
        services_status.append({
            "name": service["name"],
            "status": status,
            "uptime": f"{uptime_pct:.1f}%"
        })

    all_up = all(s["status"] == "UP" for s in services_status)
    overall = "All Systems Operational" if all_up else "Some Systems Down"
    overall_color = "#2ecc71" if all_up else "#e74c3c"
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    rows = ""
    for s in services_status:
        badge = "#2ecc71" if s["status"] == "UP" else "#e74c3c"
        rows += (
            "<div style='display:flex;justify-content:space-between;"
            "padding:15px;border-bottom:1px solid #eee;'>"
            "<div style='font-weight:bold;color:#333;'>" + s["name"] + "</div>"
            "<div style='display:flex;gap:20px;align-items:center;'>"
            "<div style='color:#666;'>Uptime: " + s["uptime"] + "</div>"
            "<div style='background:" + badge + ";color:white;padding:6px 16px;"
            "border-radius:20px;font-weight:bold;'>" + s["status"] + "</div>"
            "</div></div>"
        )

    html = (
        "<!DOCTYPE html><html><head><title>System Status</title>"
        "<meta http-equiv='refresh' content='30'>"
        "<style>body{font-family:Arial,sans-serif;background:#f5f5f5;"
        "margin:0;padding:20px;}</style></head>"
        "<body><div style='max-width:800px;margin:0 auto;background:white;"
        "border-radius:10px;padding:30px;box-shadow:0 2px 10px rgba(0,0,0,0.1);'>"
        "<div style='text-align:center;margin-bottom:30px;'>"
        "<h1 style='color:#333;'>System Status</h1>"
        "<p>Last updated: " + now + "</p>"
        "<p>Auto refreshes every 30 seconds</p></div>"
        "<div style='background:" + overall_color + ";color:white;padding:15px;"
        "border-radius:8px;text-align:center;font-size:20px;font-weight:bold;"
        "margin-bottom:30px;'>" + overall + "</div>"
        "<div>" + rows + "</div>"
        "<div style='text-align:center;margin-top:30px;color:#999;font-size:13px;'>"
        "<p>Built by Chandu - App Health Monitor</p></div>"
        "</div></body></html>"
    )
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)