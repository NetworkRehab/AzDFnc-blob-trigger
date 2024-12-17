import os
from azure.storage.blob import BlobServiceClient
import azure.functions as func

def main(blob_info: dict) -> str:
    source_connection_string = os.environ["AzureWebJobsStorage"]
    client = BlobServiceClient.from_connection_string(source_connection_string)
    
    container = client.get_container_client(blob_info['container_name'])
    cloop_name = f"{blob_info['source_blob_name']}.cloop"
    blob = container.get_blob_client(cloop_name)
    
    blob.upload_blob(b'', overwrite=True)
    return f"Created completion marker {cloop_name}"
