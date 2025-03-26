# Fetch SRE Monitoring Tool

## 🧭 Overview

This project provides two scripts for monitoring HTTP endpoint health:

1. **Console-based Monitor (`monitor.py`)**  
   - Logs availability % and latency per domain to the terminal.
2. **Prometheus + Grafana Monitor (`monitor_grafana.py`)**  
   - Pushes metrics to Prometheus via Pushgateway and visualizes them in Grafana.

Both scripts use a YAML configuration file and run health checks every 15 seconds.

---

## 🚀 Features

### ✅ Console-Based Monitor (`monitor.py`)
- Multi-threaded HTTP checks
- Tracks domain-level availability %
- Logs average latency per cycle
- Clean and portable, no external services required

### ✅ Prometheus + Grafana Monitor (`monitor_grafana.py`)
- Pushes real-time metrics to Pushgateway
- Monitored by Prometheus
- Visualized in Grafana dashboards
- Ideal for observability and alerting integrations

---

## ⚙️ Prerequisites

Make sure you have these installed:

- **Python 3.x**
- **pip** (comes with Python)
- **Prometheus**
- **Grafana**
- **Prometheus Pushgateway**

You can install Prometheus/Grafana/Pushgateway via [Homebrew](https://brew.sh/) on macOS:
```bash
brew install prometheus grafana
brew install --no-quarantine prometheus-pushgateway
