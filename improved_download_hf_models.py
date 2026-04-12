import os
import requests
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to download model

def download_model(model_url, destination_folder):
    try:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        response = requests.get(model_url, stream=True)
        response.raise_for_status()  # Check for HTTP errors

        total_size = int(response.headers.get('content-length', 0))
        file_name = os.path.join(destination_folder, model_url.split('/')[-1])

        with open(file_name, 'wb') as file, tqdm(
            desc=file_name,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                bar.update(len(data))
                file.write(data)

        logging.info(f'Successfully downloaded: {file_name}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Error downloading {model_url}: {e}')
    except Exception as e:
        logging.error(f'Unexpected error: {e}')

# Main script
if __name__ == '__main__':
    models_file = 'KAOSS999_REPOS.txt'
    destination = 'models'

    if os.path.exists(models_file):
        with open(models_file, 'r') as file:
            model_urls = file.readlines()

        for model_url in model_urls:
            download_model(model_url.strip(), destination)
    else:
        logging.error(f'Models file {models_file} does not exist!')