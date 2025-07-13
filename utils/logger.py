from config import CONFIG
from datetime import datetime
import os

def log_action(action_desc, log_file="logs/activity_log.txt"):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {action_desc}"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")
