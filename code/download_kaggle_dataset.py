import kaggle
import os

def download_kaggle_dataset(dataset: str, download_path: str):
    """
    Downloads a Kaggle dataset to the specified local directory.
    
    Args:
        dataset (str): The dataset identifier from Kaggle (e.g., 'thedevastator/airbnb-prices-in-european-cities').
        download_path (str): The local directory where the dataset should be saved.
    """
    # Ensure the download path exists
    os.makedirs(download_path, exist_ok=True)
    
    print(f"Downloading dataset: {dataset} to {download_path}")
    kaggle.api.dataset_download_files(dataset, path=download_path, unzip=True)
    print("Download complete.")

if __name__ == "__main__":
    dataset_name = "thedevastator/airbnb-prices-in-european-cities"
    local_download_path = "/home/viktorija/DE-project/dataset"  # Change this to your desired directory
    
    download_kaggle_dataset(dataset_name, local_download_path)
