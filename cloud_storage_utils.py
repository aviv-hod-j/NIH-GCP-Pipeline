from google.cloud import storage
import json
from cloud_storage.cloud_storage_exceptions import CloudStorageConnectionException


def write_to_cloud_storage(bucket_name, data, destination):
    storage_client = None
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination)
        blob.upload_from_string(json.dumps(data))
    except Exception:
        raise CloudStorageConnectionException
    finally:
        storage_client.close()


def read_from_cloud_storage(bucket_name, path):
    storage_client = None
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob_list = bucket.list_blobs(prefix=path)
        blob_list_data = [json.loads(blob.download_as_string()) for blob in blob_list if blob.path.endswith('.json')]
    except Exception:
        raise CloudStorageConnectionException
    finally:
        storage_client.close()
    return blob_list_data

