import json
import os
from datetime import datetime

def update_log():
    proposals_file = 'data/proposals.json'
    log_file = 'data/outreach_log.json'

    # Check if proposals even exists
    if not os.path.exists(proposals_file):
        print(f"❌ Error: {proposals_file} not found!")
        return

    # Load new drafts
    with open(proposals_file, 'r') as f:
        new_proposals = json.load(f)
    
    if not new_proposals:
        print("⚠️ proposals.json is empty. Nothing to log.")
        return

    # Load or Create Log
    outreach_log = []
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                outreach_log = json.load(f)
        except:
            outreach_log = []

    # Get names already in log
    existing_names = [entry['name'] for entry in outreach_log]
    
    added_count = 0
    for proposal in new_proposals:
        # If we haven't logged this one yet, add it
        if proposal['name'] not in existing_names:
            proposal['logged_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            outreach_log.append(proposal)
            added_count += 1

    # Save everything back to the log
    with open(log_file, 'w') as f:
        json.dump(outreach_log, f, indent=4)

    print(f"✅ Success! Added {added_count} new entries.")
    print(f"📊 Total log entries: {len(outreach_log)}")

if __name__ == "__main__":
    update_log()