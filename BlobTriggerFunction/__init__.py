import os
import logging
import azure.functions as func
import azure.durable_functions as df

async def main(myblob: func.InputStream, starter: str) -> None:
    client = df.DurableOrchestrationClient(starter)
    
    # Only trigger for .trg files
    if not myblob.name.endswith('.trg'):
        return

    instance_id = await client.start_new("FileTransferOrchestrator", None, {
        "trigger_blob_name": myblob.name,
        "source_blob_name": myblob.name.replace('.trg', ''),
        "container_name": myblob.blob_properties.container
    })
    
    logging.info(f"Started orchestration with ID = '{instance_id}'")