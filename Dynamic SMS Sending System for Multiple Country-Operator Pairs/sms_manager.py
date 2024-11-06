import yaml
import asyncio
import subprocess
from rate_limiter import rate_limit  # type: ignore
from monitoring import sms_sent, sms_failed, start_metrics_server

# Load configuration
with open('config.yaml') as f:
    config = yaml.safe_load(f)

def send_sms(phone, proxy):
    print("Preparing to send SMS...")
    try:
        result = subprocess.run(
            ['python', 'program2.py', '--phone', phone, '--proxy', proxy],
            check=True,  # This will raise an error if the command fails
            capture_output=True,
            text=True
        )
        print(result.stdout)  # Print the output from program2.py
        return True  # Return success
    except subprocess.CalledProcessError as e:
        print(f"Error sending SMS: {e.stderr}")
        return False  # Return failure

async def main():
    start_metrics_server()  # Start Prometheus metrics server
    
    tasks = []
    for country, data in config.items():
        for operator in data["operators"]:
            for i in range(10):  # 10 SMS per minute
                # Call send_sms synchronously
                task = asyncio.to_thread(send_sms, data["phone"], data["proxy"])
                sms_sent.labels(country=country, operator=operator).inc()  # Increment metric
                tasks.append(task)
                await asyncio.sleep(6)  # 10 SMS per minute (60 sec / 10)
    
    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
