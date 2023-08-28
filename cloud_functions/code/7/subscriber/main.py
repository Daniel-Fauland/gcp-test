import json
import base64
from google.cloud import bigquery

def pubsub_handler(event, context):
    # Retrieve the JSON payload from the Pub/Sub message
    pubsub_message = event['data']
    decoded_message = base64.b64decode(pubsub_message).decode('utf-8')  # Decode and convert to string
    print(f"Printing pubsub message received: {decoded_message}")
    data_dict = json.loads(decoded_message)
    project_id = data_dict["project_id"]
    dataset_name = data_dict["dataset_name"]
    table_name = data_dict["table_name"]
    row_count = data_dict["row_count"]
    csv_size = data_dict["csv_size"]
    blob_size = data_dict["blob_size"]
    timestamp = data_dict["timestamp"]

    bq_client = bigquery.Client(project=project_id, location="europe-west3")
    dataset = bq_client.dataset(dataset_name)
    # Get the last inserted ID from BigQuery (assuming the ID column is named 'id')
    query = f"""
        SELECT MAX(id) as last_id FROM {project_id}.{dataset_name}.{table_name}
    """
    query_job = bq_client.query(query)
    query_result = query_job.result()
    for row in query_result:
        last_id = row['last_id']
    if last_id is None:  
        last_id = 0  # Set to 0 in case bq table is empty

    # Increment the last inserted ID
    last_id += 1

    # Insert data into BigQuery table
    table_ref = bq_client.dataset(dataset_name).table(table_name)
    # Fetch the table information, including schema
    table = bq_client.get_table(table_ref)
    # Extract the schema from the table information
    schema = table.schema
    row_to_insert = {
        'id': last_id,
        'csv_rows': row_count,
        'csv_size': csv_size,
        'blob_size': blob_size,
        'inserted': timestamp
    }
    bq_client.insert_rows(table_ref, [row_to_insert], selected_fields=schema)
    print(f"Inserted 1 row into BigQuery table: {project_id}.{dataset_name}.{table_name}")
    return "Run successfull."

