import os
import shutil
from PIL import Image # You need pillow library: pip insall Pillow
from PIL.ExifTags import TAGS
from datetime import datetime

# Specify the source directory containing the files
source_dir = "/your/source/folder/address"

# Specify the main destination directory
main_dest_dir = "/your/destination/folder/address/"


# Function to extract the date from the EXIF data (if applicable) or file creation date
def get_date(file_path):
    try:
        # Attempt to get date from EXIF data
        image = Image.open(file_path)
        exif_data = image._getexif()
        if exif_data:
            date_time_str = exif_data.get(36867)  # Tag for DateTimeOriginal
            if date_time_str:
                return datetime.strptime(date_time_str, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass  # Ignore errors if not an image or EXIF data is missing

    # Fall back to file creation date
    file_creation_time = os.path.getctime(file_path)
    return datetime.fromtimestamp(file_creation_time)

# Iterate through all files in the source directory
for filename in os.listdir(source_dir):
    file_path = os.path.join(source_dir, filename)
    date_time = get_date(file_path)

    if date_time:
        # Create the destination directory based on date
        dest_dir = os.path.join(main_dest_dir, f"{date_time.year}/{date_time.month:02d}")
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy(file_path, dest_dir)
        print(f"Copied {filename} to {dest_dir}")
    else:
        # Handle files without date information (Very rare cases)
        print(f"Skipping {filename} due to missing date information")
