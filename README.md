# 🏥 App Health Monitor & Auto Recovery Tool

A real-world application health monitoring system that 
automatically detects service failures and restarts them 
without human intervention — simulating self-healing 
infrastructure used at companies like Amazon, Google 
and Microsoft.

---

## 🎯 What This Project Does

- Monitors **5 live microservices** every 30 seconds
- **Auto restarts** any service that goes down
- Tracks **uptime %** for every service
- Generates **weekly SLA reports as PDF**
- Shows a **live status page** for all services
- Runs everything with **one Docker command**

---

## 🏗️ Architecture

5 Microservices (ports 5001-5005)
↓
Health Monitor (checks every 30s)
↓ detects failure
Auto Recovery (restarts service)
↓ tracks uptime
SLA Report Generator (PDF report)
↓
Live Status Page (port 8080)

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python + Flask | 5 microservices + status page |
| Requests | HTTP health checks |
| ReportLab | PDF report generation |
| Docker + Compose | Container orchestration |
| SQLite | Uptime data storage |
| GitHub Actions | CI/CD pipeline |

---

## 🚀 How To Run

### Run with Docker (recommended)
```bash
# Clone the repo
git clone https://github.com/cchandu-pixel/app-health-monitor.git

# Go into folder
cd app-health-monitor

# Start everything
docker-compose up --build
```

### Access the services
| Service | URL |
|---|---|
| User Service | http://localhost:5001 |
| Order Service | http://localhost:5002 |
| Payment Service | http://localhost:5003 |
| Inventory Service | http://localhost:5004 |
| Notification Service | http://localhost:5005 |
| Status Page | http://localhost:8080 |

---

## 🔄 How Auto Recovery Works

Health monitor pings each service every 30 seconds
If service returns error or times out → marked as DOWN
Auto recovery immediately attempts restart
Service comes back online within 3-5 seconds
Incident logged to docs/health_log.txt
Uptime data updated in docs/uptime_data.json

---

## 📊 SLA Report

Generate a PDF report anytime:
```bash
python3 reports/report_generator.py
```

Report includes:
- Total services monitored
- Uptime % per service
- SLA compliance (99.9% target)
- Downtime events per service

---

## 📁 Project Structure

app-health-monitor/
📂 services/
📄 user_service.py
📄 order_service.py
📄 payment_service.py
📄 inventory_service.py
📄 notification_service.py
📂 monitor/
📄 health_check.py       ← monitors + auto recovers
📂 reports/
📄 report_generator.py   ← generates PDF SLA report
📂 status/
📄 status_page.py        ← live status page
📂 docs/
📄 health_log.txt        ← all health check logs
📄 uptime_data.json      ← uptime statistics
📄 docker-compose.yml      ← runs everything
📄 Dockerfile.service      ← container config
📄 requirements.txt        ← dependencies

---

## 💡 Key Skills Demonstrated

- ✅ Microservices architecture
- ✅ Automated health monitoring
- ✅ Self healing infrastructure
- ✅ SLA tracking and reporting
- ✅ PDF report generation
- ✅ Live status page
- ✅ Docker containerization
- ✅ Python automation

---

## 👨‍💻 Author

Built by **Chandu** as part of an Application Support 
Engineer portfolio project.

Connect on LinkedIn: www.linkedin.com/in/YOUR-LINKEDIN-HERE
