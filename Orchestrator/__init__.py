import azure.functions as func
import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    blob_info = context.get_input()
    
    # Transfer file with retry policy
    retry_options = df.RetryOptions(
        first_retry_interval_in_milliseconds=5000,
        max_number_of_attempts=3
    )
    
    try:
        # Transfer the file
        yield context.call_activity_with_retry(
            "TransferFileActivity",
            retry_options,
            blob_info
        )
        
        # Create completion marker
        yield context.call_activity(
            "CreateCompletionMarkerActivity",
            blob_info
        )
        
        return f"Successfully processed {blob_info['source_blob_name']}"
    
    except Exception as e:
        return f"Failed to process {blob_info['source_blob_name']}: {str(e)}"

main = df.Orchestrator.create(orchestrator_function)
