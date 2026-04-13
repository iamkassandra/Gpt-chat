import os
import requests
from tqdm import tqdm

# Define the Hugging Face account and storage path
hugging_face_account = 'Kaoss999'
storage_path = '/path/to/cloud/storage'

def fetch_all_models(account):
    models_url = f'https://huggingface.co/api/models?filter={account}'
    response = requests.get(models_url)
    response.raise_for_status()
    return response.json()

def download_model(model_id):
    model_url = f'https://huggingface.co/{model_id}/resolve/main/pytorch_model.bin'
    response = requests.get(model_url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    local_filename = os.path.join(storage_path, model_id.split('/')[-1] + '.bin')
    with open(local_filename, 'wb') as f:
        for data in tqdm(response.iter_content(chunk_size=4096), total=total_size // 4096, unit='KB'):
            f.write(data)
    return local_filename

try:
    models = fetch_all_models(hugging_face_account)
    for model in models:
        model_id = model['modelId']
        print(f'Downloading model: {model_id}')
        download_model(model_id)

except requests.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')