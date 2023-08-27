import json
import base64
from google.cloud import storage

def pubsub_handler(event, context):
    # Retrieve the JSON payload from the Pub/Sub message
    pubsub_message = event['data']
    decoded_message = base64.b64decode(pubsub_message).decode('utf-8')  # Decode and convert to string
    print(f"Printing pubsub message received: {decoded_message}")
    data_dict = json.loads(decoded_message)
    project_id = data_dict["project_id"]
    bucket_name = data_dict["bucket_name"]
    prefix_path = data_dict["prefix_path"]

    client = storage.Client(project=project_id)
    bucket = client.get_bucket(bucket_name)  # Get the bucket
    blobs = bucket.list_blobs(prefix=prefix_path)  # List objects

    # Sort the blobs by creation time default is oldest first
    sorted_blobs = sorted(blobs, key=lambda blob: blob.time_created, reverse=True)

    # Keep the newest 4 blobs and delete the rest
    if len(sorted_blobs) > 4:
        blobs_to_delete = sorted_blobs[4:]
        for blob in blobs_to_delete:
            blob.delete()
            print(f"Deleted: {blob.name}")

