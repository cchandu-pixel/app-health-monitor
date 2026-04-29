import requests
import time
import datetime
import json
import os
import subprocess

# ── Services to monitor ──────────────────────────────────────────
SERVICES = [
    {
        "name": "user-service",
        "url": "http://localhost:5001/health",
        "port": 5001,
        "script": "services/user_service.py"
    },
    {
        "name": "order-service",
        "url": "http://localhost:5002/health",
        "port": 5002,
        "script": "services/order_service.py"
    },
    {
        "name": "payment-service",
        "url": "http://localhost:5003/health",
        "port": 5003,
        "script": "services/payment_service.py"
    },
    {
        "name": "inventory-service",
        "url": "http://localhost:5004/health",
        "port": 5004,
        "script": "services/inventory_service.py"
    },
    {
        "name": "notification-service",
        "url": "http://localhost:5005/health",
        "port": 5005,
        "script": "services/notification_service.py"
    }
]

# ── Uptime tracker ───────────────────────────────────────────────
uptime_tracker = {
    service["name"]: {
        "total_checks": 0,
        "successful_checks": 0,
        "failed_checks": 0,
        "last_status": "unknown",
        "downtime_events": []
    }
    for service in SERVICES
}

# ── Log to file ──────────────────────────────────────────────────
def log_event(message):
    timestamp = str(datetime.datetime.now())
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    os.makedirs("docs", exist_ok=True)
    with open("docs/health_log.txt", "a") as f:
        f.write(log_entry + "\n")

# ── Check single service ─────────────────────────────────────────
def check_service(service):
    try:
        start = time.time()
        response = requests.get(service["url"], timeout=5)
        duration = time.time() - start

        if response.status_code == 200:
            log_event(f"✅ {service['name']} is UP - {duration:.2f}s")
            return True
        else:
            log_event(f"❌ {service['name']} returned {response.status_code}")
            return False

    except Exception as e:
        log_event(f"❌ {service['name']} is DOWN - {str(e)[:50]}")
        return False

# ── Auto restart service ─────────────────────────────────────────
def restart_service(service):
    log_event(f"🔄 Attempting to restart {service['name']}...")
    try:
        subprocess.Popen(
            ["python3", service["script"]],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(3)
        if check_service(service):
            log_event(f"✅ {service['name']} restarted successfully!")
            return True
        else:
            log_event(f"❌ {service['name']} failed to restart!")
            return False
    except Exception as e:
        log_event(f"❌ Restart failed: {str(e)}")
        return False

# ── Update uptime tracker ────────────────────────────────────────
def update_tracker(service_name, is_up):
    tracker = uptime_tracker[service_name]
    tracker["total_checks"] += 1

    if is_up:
        tracker["successful_checks"] += 1
        tracker["last_status"] = "UP"
    else:
        tracker["failed_checks"] += 1
        tracker["last_status"] = "DOWN"
        tracker["downtime_events"].append(
            str(datetime.datetime.now())
        )

# ── Save uptime data ─────────────────────────────────────────────
def save_uptime_data():
    os.makedirs("docs", exist_ok=True)
    with open("docs/uptime_data.json", "w") as f:
        json.dump(uptime_tracker, f, indent=2)

# ── Print uptime summary ─────────────────────────────────────────
def print_summary():
    print("\n" + "=" * 60)
    print("📊 UPTIME SUMMARY")
    print("=" * 60)
    for service_name, data in uptime_tracker.items():
        if data["total_checks"] > 0:
            uptime_pct = (
                data["successful_checks"] /
                data["total_checks"] * 100
            )
            print(f"\n{service_name}")
            print(f"  Uptime:  {uptime_pct:.1f}%")
            print(f"  UP:      {data['successful_checks']}")
            print(f"  DOWN:    {data['failed_checks']}")
            print(f"  Status:  {data['last_status']}")
    print("=" * 60)

# ── Main monitoring loop ─────────────────────────────────────────
def run_monitor():
    log_event("🚀 Health Monitor Started - Checking every 30 seconds")
    log_event("=" * 60)

    check_count = 0

    while True:
        check_count += 1
        log_event(f"\n🔍 Check #{check_count} - {datetime.datetime.now()}")
        log_event("-" * 60)

        for service in SERVICES:
            is_up = check_service(service)
            update_tracker(service["name"], is_up)

            if not is_up:
                log_event(
                    f"⚠️  {service['name']} is down! "
                    f"Attempting auto recovery..."
                )
                restarted = restart_service(service)
                if restarted:
                    update_tracker(service["name"], True)

        save_uptime_data()

        if check_count % 5 == 0:
            print_summary()

        log_event(f"⏳ Next check in 30 seconds...")
        time.sleep(30)

if __name__ == '__main__':
    run_monitor()