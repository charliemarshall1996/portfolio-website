import os
import shutil
from datetime import datetime


# Settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = "db.sqlite3"
BACKUP_DIR = os.path.join(BASE_DIR, "db_backups")


def run():
    # Ensure backup directory exists
    os.makedirs(BACKUP_DIR, exist_ok=True)

    # Timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"{DB_NAME}_{timestamp}.backup"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    # Copy DB
    shutil.copy2(os.path.join(BASE_DIR, DB_NAME), backup_path)
    print(f"Backup created: {backup_path}")
