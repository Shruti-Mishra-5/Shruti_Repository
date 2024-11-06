import subprocess

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
    except subprocess.CalledProcessError as e:
        print(f"Error sending SMS: {e.stderr}")

# Example usage
if __name__ == "__main__":
    send_sms("+1234567890", "proxy1")
