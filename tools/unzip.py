import os
import sys
import zipfile
from collections import defaultdict

# Extraction target directory
extract_target = 'replays'

# Assumed that zip files are in the same directory as this script
replay_archives = []
for (dirpath, dirnames, filenames) in os.walk('.'):
    for filename in filenames:
        if (filename.strip().split('.')[-1] == 'zip'):
            replay_archives.append(filename)

print(replay_archives)

illegal_chars = ":><|\"?*"

print("Beginning to Unzip all --> extract to 'replays' folder")
conut = 0

keylist = defaultdict(int)
zip_list = defaultdict(set)

for zip_archive in replay_archives:
    with zipfile.ZipFile(zip_archive, 'r') as zip_ref:
        # zip_ref.extractall(extract_target)
        conut += len(zip_ref.infolist())
        for info in zip_ref.infolist():
            name = info.filename
            sanitized_name = name
            for c in illegal_chars:
                sanitized_name = sanitized_name.replace(c, '')
            keylist[sanitized_name] += 1
            zip_list[sanitized_name].add(zip_archive)
            if (keylist[sanitized_name] > 1):
                unique_name = sanitized_name[:-10]+f"_{keylist[sanitized_name]}.SC2Replay"
                print(f"Duplicate name found, replaced with: {unique_name}")
                info.filename = unique_name
            zip_ref.extract(info, extract_target)

print(f"Number of replays: {conut}")
dup_conut = 0
for k, v in keylist.items():
    if v > 1:
        print(f"{k}: {v}")
        print(f"    From: {zip_list[k]}")
        dup_conut += v-1
print(f"Number of duplicated files: {dup_conut}")
