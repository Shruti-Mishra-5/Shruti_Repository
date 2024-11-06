# Dynamic SMS Sending System for Multiple Country-Operator Pairs
---

This project implements a scalable, automated, and monitored SMS sending system across multiple country-operator pairs. The system dynamically manages Python scripts to send SMS messages based on specific rate-limiting rules and includes error handling and monitoring functionality.

## Project Structure

- **`program1.py`**: Main orchestration script that initiates SMS sending by calling `program2.py` with the required arguments.
- **`program2.py`**: Simulates sending an SMS to a specified phone number using a proxy. It accepts command-line arguments (`--phone` and `--proxy`) for flexible SMS dispatch.
- **`rate_limiter.py`**: Contains logic for rate-limiting to comply with the "10 SMS per minute per country" rule.
- **`monitoring.py`**: Script to monitor the system and track metrics like SMS success/failure rates.
- **`sms_manager.py`**: Main orchestrator script that schedules and manages SMS sending tasks with rate limiting and concurrency.
- **`sms_sender.py`**: Handles the actual sending of SMS messages by invoking program2.py and includes retry logic for failed sends.

## Features

- **Dynamic Execution**: The system automates SMS sending across country-operator pairs, ensuring only 10 SMS are sent per minute per country.
- **Rate Limiting and Concurrency**: SMS sending is rate-limited to comply with predefined quotas and supports concurrent execution.
- **Dynamic Configuration**: Enable or disable specific country-operator pairs based on success rates, using configurable logic.
- **Monitoring and Control**: Integration with monitoring tools (e.g., Prometheus, Grafana) for tracking system metrics like SMS success rates and program health.
- **Resilience and Error Handling**: Implements retry logic and error handling for robust operation.

## Requirements

- Python 3.7+
- Required Python packages: `argparse` (part of Python standard library), `subprocess` (part of Python standard library).
- Optional monitoring tools: Prometheus, Grafana.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/dynamic-sms-sending-system.git
   cd dynamic-sms-sending-system
   ```

2. **Install Dependencies**:
   Install any additional dependencies if required for monitoring and rate limiting:

3. **Configure Monitoring (optional)**:
   Set up Prometheus and Grafana if you need to track metrics (optional). Configure `monitoring.py` for metric tracking.

## Usage

1. **Run `program1.py`**:
   `program1.py` is the main orchestrator script that starts SMS sending tasks.
   ```bash
   python program1.py
   ```

2. **Run `program2.py` Independently** (Optional for Testing):
   If you want to test `program2.py` independently, pass in the required arguments:
   ```bash
   python program2.py --phone "+1234567890" --proxy "proxy1"
   ```

3. **Customizing `send_sms` in `program1.py`**:
   You can modify `phone` and `proxy` arguments in `send_sms()` function within `program1.py` as needed for different country-operator pairs.

## Configuration

- **High-Priority Country-Operator Pairs**: Define high-priority pairs that should always be active in `program1.py`.
- **Dynamic Pair Management**: Configure logic for enabling/disabling pairs based on SMS success rates in `rate_limiter.py`.

## Monitoring

To set up monitoring, integrate Prometheus and Grafana and adjust `monitoring.py` to track:
- SMS success and failure rates
- Number of SMS sent per program
- Error logs

## Error Handling

- If `program2.py` encounters an error, `program1.py` will log the failure. 
- The `CalledProcessError` exception is captured, enabling retries or logging for later analysis.


## Contact

For questions or issues, please reach out to [shrutimishra.5@gmail.com](mailto:your-email@example.com).

---
