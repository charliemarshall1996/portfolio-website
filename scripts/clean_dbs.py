import os
import time

# Settings
BACKUP_DIR = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "db_backups")
DAYS_TO_KEEP = 7

# Time threshold
now = time.time()
cutoff = now - (DAYS_TO_KEEP * 86400)  # 86400 seconds in a day


def run():
    # Delete old backups
    for filename in os.listdir(BACKUP_DIR):
        filepath = os.path.join(BACKUP_DIR, filename)
        if os.path.isfile(filepath) and filename.endswith(".backup"):
            if os.path.getmtime(filepath) < cutoff:
                os.remove(filepath)
                print(f"Deleted: {filename}")
