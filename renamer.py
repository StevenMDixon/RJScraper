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

# Load id -> name map
with open(MAP_FILE, "r", encoding="utf-8") as f:
    id_name_map = json.load(f)

renamed = 0
skipped = 0

for filename in os.listdir(MEDIA_FOLDER):
    if not filename.lower().endswith(".mp4"):
        continue
    fileparts = filename.split(" ")
    file_id = fileparts[0]
    # print(file_id)

    if file_id not in id_name_map:
        print(f"Skipping (id not in map): {filename}")
        skipped += 1
        continue

    new_name = sanitize_filename(id_name_map[file_id]) + ".mp4"

    old_path = os.path.join(MEDIA_FOLDER, filename)
    new_path = os.path.join(MEDIA_FOLDER, new_name)

    # Avoid overwriting existing files
    if os.path.exists(new_path):
        # print(f"Skipping (already exists): {new_name}")
        skipped += 1
        continue

    os.rename(old_path, new_path)
    # print(f"Renamed: {filename} -> {new_name}")
    renamed += 1

print(f"\nDone! Renamed {renamed} files. Skipped {skipped}.")