import argparse
import json
from datetime import datetime

# --- Constants ---
FEEDBACK_FILE = "jsons\chatbot_feedback.jsonl" # The file where feedback will be stored

# --- Core Logic Function ---

def save_feedback(user_id: str, feedback_type: str, description: str):
    """
    Creates a feedback record and appends it to the feedback file.

    Args:
        user_id (str): The ID of the user providing the feedback.
        feedback_type (str): The category of the feedback.
        description (str): The detailed content of the feedback.
    """
    # 1. Create the feedback record as a Python dictionary
    feedback_record = {
        "timestamp": datetime.utcnow().isoformat() + "Z", # Use UTC time in ISO 8601 format
        "user_id": user_id,
        "feedback_type": feedback_type,
        "description": description
    }

    # 2. Append the record to the JSON Lines file
    try:
        with open(FEEDBACK_FILE, "a") as f:
            f.write(json.dumps(feedback_record) + "\n")
        
        # 3. Provide confirmation to the user
        print("✅ Feedback successfully saved!")
        print(json.dumps(feedback_record, indent=2))

    except IOError as e:
        print(f"❌ Error: Could not write to file {FEEDBACK_FILE}. {e}")


# --- Main Execution Block for CLI ---

if __name__ == "__main__":
    # 1. Set up the argument parser
    parser = argparse.ArgumentParser(
        description="A CLI tool to collect and store user feedback for the chatbot."
    )

    # 2. Define the command-line arguments
    parser.add_argument(
        "--user-id",
        type=str,
        required=True,
        help="The unique identifier of the user submitting feedback."
    )
    parser.add_argument(
        "--feedback-type",
        type=str,
        required=True,
        choices=["bug_report", "suggestion", "confusing_response", "other"],
        help="The category of the feedback."
    )
    parser.add_argument(
        "--description",
        type=str,
        required=True,
        help="The detailed feedback message."
    )

    # 3. Parse the arguments from the command line
    args = parser.parse_args()

    # 4. Call the main logic function with the parsed arguments
    save_feedback(args.user_id, args.feedback_type, args.description)

