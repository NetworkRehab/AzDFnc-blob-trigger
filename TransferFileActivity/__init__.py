import os
from azure.storage.blob import BlobServiceClient
import azure.functions as func

def main(blob_info: dict) -> str:
    source_connection_string = os.environ["AzureWebJobsStorage"]
    dest_connection_string = os.environ["DestinationStorageConnectionString"]
    
    source_client = BlobServiceClient.from_connection_string(source_connection_string)
    dest_client = BlobServiceClient.from_connection_string(dest_connection_string)
    
    # Get source blob
    source_container = source_client.get_container_client(blob_info['container_name'])
    source_blob = source_container.get_blob_client(blob_info['source_blob_name'])
    blob_data = source_blob.download_blob().readall()
    
    # Transfer to destination
    dest_container = dest_client.get_container_client(os.environ["DestinationContainerName"])
    dest_blob = dest_container.get_blob_client(blob_info['source_blob_name'])
    dest_blob.upload_blob(blob_data, overwrite=True)
    
    return f"Transferred {blob_info['source_blob_name']}"
