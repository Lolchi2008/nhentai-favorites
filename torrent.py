import csv
import requests
import time
import random
import os
from urllib.parse import unquote

#Thanks chatGPT

# Initialize a session
session = requests.Session()

# Set custom headers to mimic a real browser
headers = {
    'User-Agent': '#change me',
    'Cookie': '#change me',
    'Referer': 'https://nhentai.net/login/',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
}

def sanitize_filename(filename):
    """Sanitize the filename by removing or replacing invalid characters."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def download_file(url, headers):
    with requests.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()
        # Extracting the filename from the Content-Disposition header
        content_disposition = r.headers.get('Content-Disposition')
        if content_disposition:
            filename = content_disposition.split('filename*=')[-1].split("''")[-1]
            filename = unquote(filename)  # Decode URL-encoded filename
        else:
            filename = url.split('/')[-2] + ".txt"  # Default filename if none is provided
        filename = sanitize_filename(filename)  # Sanitize the filename
        # Ensure directory exists
        os.makedirs('downloads', exist_ok=True)
        filepath = os.path.join('downloads', filename)
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return filepath

def main():
    ids_file = 'id.csv'  # Path to your CSV file containing IDs

    with open(ids_file, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            file_id = row[0]  # Extract file ID from the row
            # Updated URL pattern to include '/g/' before the file ID
            url = f"https://nhentai.net/g/{file_id}/download"
            print(f"Attempting to download file from {url}...")  # Informative message before download
            try:
                # Corrected: Now passing 'headers' as an argument to download_file
                downloaded_filepath = download_file(url, headers)
                print(f"Downloaded to '{downloaded_filepath}' successfully.")  # Success message
            except Exception as e:
                print(f"Failed to download from '{url}'. Error: {e}")  # Error message
            time.sleep(random.uniform(1.5, 5))  # Random delay between 1.5 and 3 seconds

if __name__ == "__main__":
    main()
