import yaml
import requests
import time
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# Load YAML config file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to check the health of an endpoint
def check_health(endpoint):
    url = endpoint.get("url")
    method = endpoint.get("method", "GET").upper()
    headers = endpoint.get("headers", {})
    body = endpoint.get("body", None)

    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=body, timeout=5)
        latency = (time.time() - start_time) * 1000  # Convert to milliseconds

        is_up = 200 <= response.status_code < 300 and latency < 500
        return is_up, latency
    except requests.RequestException:
        return False, None

# Function to push metrics to Prometheus Pushgateway
def push_metrics_to_grafana(domain, availability, avg_latency):
    registry = CollectorRegistry()

    # Define Prometheus metrics
    availability_metric = Gauge('availability_percentage', 'Availability of the domain', ['domain'], registry=registry)
    latency_metric = Gauge('response_latency_ms', 'Response latency in milliseconds', ['domain'], registry=registry)

    # Set metric values
    availability_metric.labels(domain=domain).set(availability)
    latency_metric.labels(domain=domain).set(avg_latency if avg_latency is not None else 0)

    # Push metrics to Prometheus Pushgateway
    push_to_gateway('localhost:9091', job=domain, registry=registry)

# Main function to monitor endpoints
def monitor_endpoints(config_file):
    endpoints = load_config(config_file)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0, "latencies": []})

    try:
        while True:
            with ThreadPoolExecutor(max_workers=5) as executor:
                results = {executor.submit(check_health, ep): ep for ep in endpoints}
                print("\n--- New Monitoring Cycle ---")

                for future in results:
                    endpoint = results[future]
                    url = endpoint["url"]
                    domain = url.split("/")[2]
                    is_up, latency = future.result()

                    print(f"Checked: {url} | Domain: {domain} | Status: {'UP' if is_up else 'DOWN'} | Latency: {latency:.2f}ms" if latency else "N/A")

                    domain_stats[domain]["total"] += 1
                    if is_up:
                        domain_stats[domain]["up"] += 1
                        if latency is not None:
                            domain_stats[domain]["latencies"].append(latency)

            # Compute and push availability and latency metrics
            for domain, stats in domain_stats.items():
                availability = round(100 * (stats["up"] / stats["total"]))
                avg_latency = sum(stats["latencies"]) / len(stats["latencies"]) if stats["latencies"] else 0
                print(f"{domain} has {availability}% availability with avg latency {avg_latency:.2f}ms")

                # Push to Grafana (Prometheus)
                push_metrics_to_grafana(domain, availability, avg_latency)

            time.sleep(15)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
        sys.exit(0)

# Entry point
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python monitor_grafana.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    monitor_endpoints(config_file)
