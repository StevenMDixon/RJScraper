import os
import json
import re

import sys
sys.stdout.reconfigure(encoding='utf-8')

config = {}

with open('config.json', 'r') as f:
    config = json.load(f)

# ===== SETTINGS =====
MEDIA_FOLDER = config["downloadLoc"]
MAP_FILE = outputTitleMapLoc = os.path.join(config["fileLocation"], config["OutputTitleFile"])
# ====================

def sanitize_filename(name):
    """Make filename Windows-safe."""
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()

with open(MAP_FILE, "r", encoding="utf-8") as f:
    id_name_map = json.load(f)

renamed = 0
skipped = 0

for filename in os.listdir(MEDIA_FOLDER):
    if not filename.lower().endswith(".mp4"):
        continue
    fileparts = filename.split(" ")
    file_id = fileparts[0]

    if file_id not in id_name_map:
        print(f"Skipping (id not in map): {filename}")
        skipped += 1
        continue

    new_name = sanitize_filename(id_name_map[file_id]) + ".mp4"
    
    old_path = os.path.join(MEDIA_FOLDER, filename)
    new_path = os.path.join(MEDIA_FOLDER, new_name)

    base, ext = os.path.splitext(new_name)
    counter = 1

    while os.path.exists(new_path):
        new_filename = f"{base} ({counter}){ext}"
        new_path = os.path.join(MEDIA_FOLDER, new_filename)
        counter += 1

    os.rename(old_path, new_path)
    renamed += 1

print(f"\nDone! Renamed {renamed} files. Skipped {skipped}.")