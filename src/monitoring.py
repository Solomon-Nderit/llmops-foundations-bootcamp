import re
import time
import json
import logging
import random
from typing import Dict, Any, Optional

# --- Constants and Configuration ---

# Define PII patterns using compiled regex for efficiency
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
PHONE_PATTERN = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
LOG_FILE_PATH = "..\sample_chatbot_logs.jsonl" # Path to the data file

# --- Individual Checker Functions ---

def detect_pii(text: str) -> bool:
    """
    Checks for the presence of email or phone number PII in the given text.

    Args:
        text (str): The text to scan for PII.

    Returns:
        bool: True if PII is found, False otherwise.
    """
    if not isinstance(text, str):
        return False
    if EMAIL_PATTERN.search(text) or PHONE_PATTERN.search(text):
        return True
    return False

def check_for_data_errors(interaction: Dict[str, Any]) -> Optional[str]:
    """
    Validates the structure and content of the chatbot interaction log.

    Args:
        interaction (dict): The interaction log to validate.

    Returns:
        Optional[str]: An error message string if an issue is found, otherwise None.
    """
    if not interaction.get("user_query"):
        return "Missing user_query"
    # A null response is a critical functional error for a chatbot
    if interaction.get("bot_response") is None:
        return "Bot response is null"
    return None

# --- Main Orchestrator Function ---

def monitor_single_interaction(interaction: Dict[str, Any]) -> Dict[str, Any]:
    """
    Orchestrates all monitoring checks for a single chatbot interaction.
    This includes latency simulation, PII detection, and error checking.

    Args:
        interaction (dict): A single interaction record to process.

    Returns:
        dict: A structured log entry containing monitoring metadata and the original data.
    """
    start_time = time.time()

    # 1. Check for data integrity and functional errors first
    error = check_for_data_errors(interaction)

    # 2. Check for PII in the bot's response
    pii_detected = detect_pii(interaction.get("bot_response", ""))

    # 3. Simulate the delay of the LLM call for realistic latency
    # In a real system, this would wrap the actual API call.
    simulated_delay = random.uniform(0.3, 1.8) # Simulate 300ms to 1.8s
    time.sleep(simulated_delay)

    # 4. Finalize latency calculation
    latency_ms = round((time.time() - start_time) * 1000)

    # 5. Assemble the final, structured log entry
    monitoring_result = {
        "interaction_id": interaction.get("id"),
        "timestamp_utc": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "latency_ms": latency_ms,
        "pii_detected": pii_detected,
        "error": error,
        "original_interaction": interaction
    }

    return monitoring_result

# --- Main Execution Block ---

if __name__ == "__main__":
    # Setup logging to print structured JSON to the console (standard output)
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    try:
        with open(LOG_FILE_PATH, 'r') as f:
            for line in f:
                try:
                    # Load each line as a separate JSON object
                    interaction_data = json.loads(line)
                    # Process each interaction through the monitoring function
                    final_log = monitor_single_interaction(interaction_data)
                    # Log the result as a single JSON string
                    logging.info(json.dumps(final_log))
                except json.JSONDecodeError:
                    logging.error(f"Error: Could not decode JSON from line: {line.strip()}")

    except FileNotFoundError:
        logging.error(f"Error: Log file not found at '{LOG_FILE_PATH}'. Please ensure the file exists in the root directory.")