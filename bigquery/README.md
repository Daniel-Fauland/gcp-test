# GCP BigQuery

This section will cover a few hands-on tutorials using GCP BigQuery

**Contents:**

- [Create BQ dataset](#create-bq-dataset)
- [Create BQ table](#create-bq-table)
- [Grant member or service account dataset/table access]()

## Create BQ dataset

A BQ table is always part of a dataset therefore it's necessary to create a dataset before being able to deploy a table. This can be done easily via bq (part of gcloud cli):

General code snippet:

```shell
bq --location=<your-region> mk --description "<your-description>" <dataset-name>
```

Example code snippet:

```shell
bq --location=europe-west3 mk --description "Dataset for my gcp data" my_data
```

## Create BQ table

Before creating a BQ table make sure you have created a [dataset](#create-bq-dataset).
The easiest way to create a BQ table is via standard SQL commands:

General code snippet:

```sql
CREATE TABLE <project-id>.<dataset_name>.<table_name> (
  field1 <data-type> NOT NULL,
  field2 <data-type> OPTIONS (description="<your-description>")
);
```

Example code snippet:

```sql
CREATE TABLE propane-nomad-396712.my_data.db_table (
  id INT64 NOT NULL,
  csv_rows INT64 OPTIONS (description="Number of rows in csv"),
  csv_size FLOAT64 OPTIONS (description="csv file size in pandas"),
  blob_size FLOAT64 OPTIONS (description="blob file size in cloud storage"),
  inserted TIMESTAMP NOT NULL OPTIONS (description="UTC Timestamp")
);
```

**Note:** BigQuery uses SQL but it has many peculiarities like not supporting primary/foreign keys, etc. Therefore should check the available options on the [BigQuery docs](https://cloud.google.com/bigquery/docs).

## Grant member or service account dataset/table access

In order to grant a member or service account access to a specific dataset or table you can use sql.

General code snippet:

```sql
GRANT `roles/<resoure>.<type>`
ON SCHEMA `<project-id>`.<your-dataset>
TO "serviceAccount:<your-service-acc>";
```

Example code snippet:

```sql
GRANT `roles/bigquery.user`
ON SCHEMA `propane-nomad-396712`.my_data.my_table
TO "serviceAccount:sa-func-b@propane-nomad-396712.iam.gserviceaccount.com";
```
