# Terraform

This section will cover a few hands-on tutorials using Terraform.

Testing:

```python
data_dict = {"project_id": "propane-nomad-396712", "dataset_name": "my_data", "table_name": "db_table", "row_count": 1, "csv_size": 1, "blob_size": 0, "timestamp": "2023-08-27T19:13:52.167462"}
project_id = data_dict["project_id"]
dataset_name = data_dict["dataset_name"]
table_name = data_dict["table_name"]
row_count = data_dict["row_count"]
csv_size = data_dict["csv_size"]
blob_size = data_dict["blob_size"]
timestamp = data_dict["timestamp"]

bq_client = bigquery.Client(project=project_id, location="europe-west3")
# Get the last inserted ID from BigQuery (assuming the ID column is named 'id')
query = f"""
    SELECT MAX(id) as last_id FROM {project_id}.{dataset_name}.{table_name}
"""
query_job = bq_client.query(query)
last_id = query_job.result()[0]['last_id']  # Will return 'None' if BQ table is empty
```

```shell
roles/bigquery.user
roles/cloudfunctions.invoker
roles/pubsub.subscriber
roles/storage.admin
```
