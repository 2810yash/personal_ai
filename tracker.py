import os
import time
from memory import store_memory
from datetime import datetime

# 👇 ONLY track your project folder
WATCH_FOLDER = "D:\\ML\\personal_ai"

# Ignore useless folders/files
IGNORE_FOLDERS = ["venv", "__pycache__", ".git", "memory_db"]
IGNORE_EXTENSIONS = [".pyc", ".txt", ".md", ".bin", ".sqlite3"]

seen_files = {}

def should_ignore(path):
    for folder in IGNORE_FOLDERS:
        if folder in path:
            return True
    
    for ext in IGNORE_EXTENSIONS:
        if path.endswith(ext):
            return True
    
    return False


def track_changes():
    while True:
        for root, dirs, files in os.walk(WATCH_FOLDER):
            for file in files:
                path = os.path.join(root, file)

                if should_ignore(path):
                    continue

                try:
                    modified_time = os.path.getmtime(path)

                    if path not in seen_files or seen_files[path] != modified_time:
                        seen_files[path] = modified_time

                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                        project = os.path.basename(WATCH_FOLDER)
                        activity = f"{timestamp} - Working on {project} → {file}"

                        store_memory(activity)
                        print("Tracked:", activity)

                except:
                    pass

        time.sleep(5)


if __name__ == "__main__":
    track_changes()