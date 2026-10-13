import os
import urllib.request
import zipfile
from pathlib import Path

url = "https://rdm.uq.edu.au/files/8c6e2a00-ef9c-11ed-827d-e762de186848"
target_dir = Path(r"D:\Zephyr\ThreatWeave\data\raw\NF-UNSW-NB15-v2")
target_dir.mkdir(parents=True, exist_ok=True)

# Use urllib
print("Fetching headers...")
req = urllib.request.Request(url, method='HEAD')
try:
    with urllib.request.urlopen(req) as response:
        content_type = response.headers.get('Content-Type')
        size = response.headers.get('Content-Length')
        print(f"Content-Type: {content_type}")
        print(f"Size: {size}")
except Exception as e:
    print(f"HEAD failed: {e}")
    content_type = "unknown"

target_file = target_dir / "NF-UNSW-NB15-v2.csv"
if content_type in ['application/zip', 'application/x-zip-compressed'] or str(size) == "None":
    target_file = target_dir / "dataset.zip"
else:
    # force zip just in case the link redirects to a zip
    target_file = target_dir / "dataset.zip" 

print(f"Downloading to {target_file}...")
urllib.request.urlretrieve(url, target_file)
print("Download complete.")

if zipfile.is_zipfile(target_file):
    print("Extracting ZIP...")
    with zipfile.ZipFile(target_file, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
        print(f"Extracted: {zip_ref.namelist()}")
else:
    print("Not a zip file, renaming to CSV...")
    if target_file.name == "dataset.zip":
        os.rename(target_file, target_dir / "NF-UNSW-NB15-v2.csv")

print("Files in target dir:")
print(os.listdir(target_dir))
