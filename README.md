# 🚦 Fetch SRE Monitoring Tool

This is a synthetic monitoring solution built from scratch for the Fetch SRE Take-Home Assessment. It monitors the health of defined HTTP endpoints, calculates domain-level availability and latency, and reports results in two ways:

- ✅ Console-based logging (monitor.py)
- 📊 Grafana dashboards via Prometheus + Pushgateway (monitor_grafana.py)

---

## 📦 Project Structure

| File                 | Description                                                              |
|----------------------|--------------------------------------------------------------------------|
| `monitor.py`         | Console-based SRE monitor that logs health data to terminal              |
| `monitor_grafana.py` | Enhanced version that pushes metrics to Prometheus Pushgateway           |
| `config.yaml`        | Defines endpoints to monitor                                             |
| `requirements.txt`   | Python dependencies                                                      |
| `.gitignore`         | Excludes virtualenv, data artifacts, and system files                    |

---

## ⚙️ Prerequisites

- Python 3.7+
- pip
- Prometheus
- Prometheus Pushgateway
- Grafana
- Homebrew (for macOS users)

---

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone git@github.com:dataops-mike/fetch_sre_monitor.git
cd fetch_sre_monitor
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # For Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🧾 Create `config.yaml`

This file contains the endpoints to monitor:
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

- name: Fetch Rewards Home Page
  url: https://www.fetchrewards.com/
  method: GET
  headers:
    user-agent: fetch-synthetic-monitor
```

---

## ▶️ Run Console-Based Monitor

```bash
python monitor.py config.yaml
```

Every 15 seconds, it logs:
- UP/DOWN per endpoint
- Latency (ms)
- Domain availability %

---

## ▶️ Run Prometheus + Grafana Monitor

### 1. Install Monitoring Tools (macOS via Homebrew)
```bash
brew install prometheus grafana
brew install --no-quarantine prometheus-pushgateway
```

### 2. Configure Prometheus
Edit `/usr/local/etc/prometheus.yml`:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'pushgateway'
    static_configs:
      - targets: ['localhost:9091']
```

Restart Prometheus:
```bash
brew services restart prometheus
```

### 3. Start Services
```bash
pushgateway
brew services start prometheus
brew services start grafana
```

### 4. Reset Grafana Password (Optional)
```bash
grafana-cli admin reset-admin-password <your-secure-password> --homepath /usr/local/opt/grafana/share/grafana
```

Login: [http://localhost:3000](http://localhost:3000)

---

### 5. Run the Monitor
```bash
python monitor_grafana.py config.yaml
```

Pushes:
- `availability_percentage{exported_job="fetch.com"}`
- `response_latency_ms{exported_job="fetch.com"}`

---

## 📊 Grafana Setup

### Step 1: Add Prometheus as a Data Source
- URL: `http://localhost:9090`

### Step 2: Create Dashboard Panels

**Availability:**
```promql
availability_percentage{exported_job="fetch.com"}
```

**Latency:**
```promql
response_latency_ms{exported_job="fetch.com"}
```

Repeat for `www.fetchrewards.com`.

**Set Gauge Thresholds:**
- Red: < 85
- Green: ≥ 85

---

## ✅ Stopping Services
```bash
brew services stop grafana
brew services stop prometheus
# CTRL+C to stop Pushgateway
```

---

## 🛠 Troubleshooting

| Problem | Fix |
|--------|-----|
| Grafana login fails | Use grafana-cli with --homepath |
| No metrics in panel | Check Prometheus scrape + query labels |
| Prometheus not scraping | Ensure pushgateway target in prometheus.yml |
| “No data” in panel | Adjust time range to "Last 5 minutes" |

---

## 👤 Author

Michael Iheanacho  
Built for Fetch SRE Take-Home Assessment
