# Fetch SRE Monitoring Tool

## Overview
This script is designed to monitor the health of multiple HTTP endpoints based on a YAML configuration file. It performs periodic health checks, calculates availability percentages, and provides a real-time monitoring dashboard via a Flask web server.

## Features
- **Multi-threaded requests** for faster monitoring.
- **Health check every 15 seconds** with response latency tracking.
- **Availability tracking** for each domain.
- **Real-time web dashboard** available at `http://localhost:5000/status`.
- **Graceful shutdown** with `CTRL+C`.

---

## Prerequisites
Ensure you have the following installed:
- **Python 3.x** (Check with `python3 --version`)
- **pip** (Comes with Python, verify with `pip --version`)

### Install Dependencies
Navigate to the project folder and run:
```bash
pip install -r requirements.txt
```
Alternatively, manually install required packages:
```bash
pip install requests pyyaml flask
```

---

## Setup Instructions

### 1. Clone the Repository (If applicable)
```bash
git clone <repository_url>
cd fetch_sre_monitor
```

### 2. Create a Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate    # Windows
```

### 3. Create a Configuration File
Create a file named `config.yaml` and define the endpoints to monitor. Example:
```yaml
- name: Fetch Home Page
  url: https://fetch.com/
  method: GET
  headers:
    user-agent: fetch-synthetic-monitor

- name: Fetch Careers Page
  url: https://fetch.com/careers
  method: GET
  headers:
    user-agent: fetch-synthetic-monitor

- name: Submit Data
  url: https://fetch.com/api/submit
  method: POST
  headers:
    content-type: application/json
    user-agent: fetch-synthetic-monitor
  body: '{"username": "john_doe", "score": 100}'
```

### 4. Run the Monitoring Script
Execute the script with the configuration file:
```bash
python monitor.py config.yaml
```

---

## How It Works
1. The script reads `config.yaml` to load endpoint details.
2. Every **15 seconds**, it:
   - Sends HTTP requests to each endpoint.
   - Logs the response status and latency.
   - Determines if the endpoint is **UP** (2xx status & latency < 500ms).
   - Tracks the **availability percentage** for each domain.
3. It logs results to the **terminal** and exposes an **API**.

---

## Access the Real-Time Monitoring Dashboard
Once the script is running, open your browser and visit:
```bash
http://localhost:5000/status
```
You’ll see a JSON response with the availability percentages:
```json
{
    "fetch.com": 75,
    "www.fetchrewards.com": 100
}
```

---

## Stopping the Script
To gracefully stop monitoring, press:
```bash
CTRL + C
```

---

## Debugging and Logs
- If availability is low, check the **terminal output** for failed requests.
- Enable more logging by modifying `print()` statements inside `monitor.py`.
- Check **network status** to ensure endpoints are reachable.

---

## Future Enhancements
- Add **email or Slack alerts** when an endpoint is down.
- Store historical data for long-term analysis.
- Improve UI for real-time visualization.


---

## Author
Michael Iheanahco

