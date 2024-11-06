from prometheus_client import start_http_server, Counter

sms_sent = Counter('sms_sent', 'Number of SMS sent', ['country', 'operator'])
sms_failed = Counter('sms_failed', 'Number of SMS failed', ['country', 'operator'])

def start_metrics_server():
    start_http_server(8000)  # Expose Prometheus metrics at port 8000
