import yaml
import requests
import time
import sys
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, jsonify

# Flask app for real-time monitoring dashboard
app = Flask(__name__)
domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def check_health(endpoint):
    name = endpoint.get("name")
    url = endpoint.get("url")
    method = endpoint.get("method", "GET").upper()
    headers = endpoint.get("headers", {})
    body = endpoint.get("body", None)
    
    print(f"Checking: {name} ({url})")
    
    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=body, timeout=5)
        latency = (time.time() - start_time) * 1000
        
        # Logging additional details for debugging
        print(f"Response Status: {response.status_code}, Latency: {latency:.2f}ms")
        
        return 200 <= response.status_code < 300 and latency < 500
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False

def monitor_endpoints(config_file):
    endpoints = load_config(config_file)
    
    try:
        while True:
            with ThreadPoolExecutor(max_workers=5) as executor:
                results = {executor.submit(check_health, ep): ep for ep in endpoints}
                
                for future in results:
                    endpoint = results[future]
                    url = endpoint["url"]
                    domain = url.split("/")[2]
                    is_up = future.result()
                    
                    domain_stats[domain]["total"] += 1
                    if is_up:
                        domain_stats[domain]["up"] += 1
            
            for domain, stats in domain_stats.items():
                availability = round(100 * (stats["up"] / stats["total"]))
                print(f"{domain} has {availability}% availability percentage")
            
            time.sleep(15)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
        sys.exit(0)

@app.route('/status', methods=['GET'])
def get_status():
    status_data = {domain: round(100 * (stats["up"] / stats["total"])) for domain, stats in domain_stats.items()}
    return jsonify(status_data)

def start_monitoring(config_file):
    monitor_thread = threading.Thread(target=monitor_endpoints, args=(config_file,), daemon=True)
    monitor_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    start_monitoring(config_file)
