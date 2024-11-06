import subprocess

def send_sms(phone="+1234567890", proxy="proxy1"):
    try:
        subprocess.run(['python', 'program2.py', '--phone', phone, '--proxy', proxy], check=True)
        print(f"SMS sent to {phone} via {proxy}.")
    except subprocess.CalledProcessError:
        print(f"Failed to send SMS to {phone} via {proxy}.")

# Example usage in program1.py
if __name__ == "__main__":
    send_sms()  # Calls program2.py with default values
