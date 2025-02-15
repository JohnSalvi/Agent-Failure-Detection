import os
import json
import pandas as pd

# Define input folder and output files
LOGS_FOLDER = "."
OUTPUT_SUCCESS = "processed_success.csv"
OUTPUT_FAILURE = "processed_failure.csv"

# Define keys to extract AI progression
KEYS_TO_EXTRACT = ["Thought", "Research Plan", "Reflection"]

# Lists to store extracted data
success_logs = []
failure_logs = []

# Process each JSON file in the folder
for root, _, files in os.walk(LOGS_FOLDER):  # Recursively search all subdirectories
    for filename in files:
        if filename.endswith(".json"):
            filepath = os.path.join(root, filename)
            print(f"Processing file: {filepath}")  # Debugging line
            
            try:
                # Read the JSON file only once
                with open(filepath, "r", encoding="utf-8") as file:
                    data = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"⚠️ Error reading JSON file {filepath}: {e}")
                continue  # Skip corrupted or missing files

            # Extract challenge details safely
            challenge_name = data.get("challenge", {}).get("name", "Unknown Challenge")
            agent_name = data.get("challenge_run_input", {}).get("agent_config", {}).get("deployment_name", "Unknown Agent")

            # Determine if the run was a success or failure
            is_success = "HTB{" in str(data)  # Check if the flag was retrieved

            # Extract AI progression safely
            iterations = data.get("subtask_completions", {}).get("subtask_1", {}).get("iterations", [])
            for iteration in iterations:
                model_response = (iteration.get("model_response") or {}).get("value", "")
                execution_output = iteration.get("execution_output") or {}

                ai_response = {
                    "Filename": filename,
                    "Challenge": challenge_name,
                    "Agent": agent_name,
                    "Success": is_success,
                    "Reflection": model_response.split("\n")[0] if model_response else "",
                    "Research Plan": model_response.split("\n")[1:] if model_response else [],
                }

                if is_success:
                    success_logs.append(ai_response)
                else:
                    failure_logs.append(ai_response)

# Save extracted logs to CSV
df_success = pd.DataFrame(success_logs)
df_failure = pd.DataFrame(failure_logs)

df_success.to_csv(OUTPUT_SUCCESS, index=False, mode='w')
df_failure.to_csv(OUTPUT_FAILURE, index=False, mode='w')

print(f"✅ Processing complete!\n📂 Success logs saved to: {OUTPUT_SUCCESS}\n📂 Failure logs saved to: {OUTPUT_FAILURE}")  
