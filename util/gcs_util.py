from google.cloud import storage
from util.logger import logger

def upload_to_gcs(csv_data: str, bucket_name: str, blob_name: str):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    logger.info(f"Uploading {blob_name} to {bucket_name}")
    blob.upload_from_string(csv_data, content_type='text/csv')
    logger.info(f"File {blob_name} uploaded to {bucket_name}.")