import os
import requests
import tqdm
from google.cloud import storage

# Function to fetch models from HuggingFace
def fetch_models_from_huggingface():
    url = 'https://huggingface.co/api/models'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Failed to fetch models from HuggingFace')

# Function to upload file to Google Cloud Storage
def upload_to_gcs(bucket_name, source_file, destination_blob):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)

    # Uploading the file
    with tqdm.tqdm(total=os.path.getsize(source_file), unit='B', unit_scale=True, desc=source_file) as pbar:
        blob.upload_from_filename(source_file)
        pbar.update(os.path.getsize(source_file))

# Main function
if __name__ == '__main__':
    try:
        models = fetch_models_from_huggingface()
        bucket_name = 'your_gcs_bucket_name'  # Replace with your bucket name

        for model in models:
            model_id = model['id']
            model_file = f'{model_id}.bin'  # Example for binary model files

            # Download the model file
            with requests.get(f'https://huggingface.co/{model_id}/resolve/main/{model_file}', stream=True) as r:
                if r.status_code == 200:
                    with open(model_file, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

                    # Upload to GCS
                    upload_to_gcs(bucket_name, model_file, model_file)
                else:
                    print(f'Error downloading {model_id}: {r.status_code}')
    except Exception as e:
        print(f'An error occurred: {str(e)}')
