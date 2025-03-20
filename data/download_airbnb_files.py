import os
import requests
from bs4 import BeautifulSoup
import wget

# Define the countries you want to download data for
TARGET_COUNTRIES = ["spain"]
BASE_URL = "https://insideairbnb.com/get-the-data/"

def fetch_airbnb_data():
    # Fetch the webpage
    response = requests.get(BASE_URL)
    
    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links on the page
    all_links = soup.find_all("a")

    # Filter only "visualisations/listings.csv" links for target countries
    listings_links = [
        link.get("href") for link in all_links
        if link.get("href") and "visualisations/listings.csv" in link.get("href")
        and any(country in link.get("href").lower() for country in TARGET_COUNTRIES)
    ]

    # Create a directory for downloads
    os.makedirs("airbnb_data", exist_ok=True)

    # Download each file
    for link in listings_links:
        filename_parts = link.split("/")
        country = filename_parts[3]  # Extract country from URL
        region = filename_parts[4]   # Extract region from URL
        city = filename_parts[5]     # Extract city from URL
        release_date = filename_parts[6]  # Extract release date

        # Construct a formatted filename
        file_name = f"{country}_{region}_{city}_{release_date}_listings.csv"
        file_path = os.path.join("airbnb_data", file_name)
        
        try:
        # Remove file if it already exists
            if os.path.exists(file_path):
                os.remove(file_path)

        # Download file
            wget.download(link, file_path)
            print(f"\nDownloaded: {file_name}")
        except Exception as e:
            print(f"Failed to download {file_name}: {e}")

if __name__ == "__main__":
    fetch_airbnb_data()
