import os
import shutil
from datetime import datetime

# Paths
source_dir = r"C:\Users\Justi\McCasland\artifacts\x-scrape\TMBSPACESHIPS\20260416-150310\downloaded-media"
assets_dir = r"C:\Users\Justi\McCasland\assets\TMBSPACESHIPS"

# Twitter epoch
TWITTER_EPOCH = 1288834974657

files = os.listdir(source_dir)
moved_count = 0

for f in files:
    if f.startswith('.'): continue # Skip hidden files if any

    full_source = os.path.join(source_dir, f)
    if not os.path.isfile(full_source): continue
    
    parts = f.split('-')
    if len(parts) >= 1:
        snowflake_str = parts[0]
        try:
            snowflake = int(snowflake_str)
            # Calculate timestamp
            ts = ((snowflake >> 22) + TWITTER_EPOCH) / 1000.0
            dt = datetime.fromtimestamp(ts)
            
            # Format folder and file name
            year_str = dt.strftime('%Y')
            month_str = dt.strftime('%m')
            date_str = dt.strftime('%Y%m%d_%H%M%S')
            
            # Target directory: ~/assets/TMBSPACESHIPS/YYYY/MM
            target_folder = os.path.join(assets_dir, year_str, month_str)
            os.makedirs(target_folder, exist_ok=True)
            
            # New filename
            new_filename = f"{date_str}_{f}"
            full_target = os.path.join(target_folder, new_filename)
            
            # Move file
            shutil.move(full_source, full_target)
            moved_count += 1
            
        except ValueError:
            print(f"Skipping {f}, not a valid snowflake ID.")
    else:
        print(f"Skipping {f}, doesn't match expected pattern.")

print(f"Successfully moved {moved_count} files into {assets_dir}.")
