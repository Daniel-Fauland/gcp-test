# Terraform

This section will cover a few hands-on tutorials using Terraform.

Testing:

Deploy http cloud function A:

```shell
gcloud functions deploy db-func-pubsub-test \
--runtime=python310 \
--trigger-http \
--entry-point=start_script \
--region=europe-west3 \
--max-instances=1 \
--timeout=3500s \
--memory=1GiB \
--service-account=cloud-function-a@propane-nomad-396712.iam.gserviceaccount.com \
--ingress-settings=all \
--no-allow-unauthenticated \
--gen2 \
--source=./cloud_functions/code/6/publisher/
```

Deploy pubsub cloud function B:

```shell
gcloud functions deploy func-pubsub-subscriber-test \
--runtime=python310 \
--trigger-topic=db-topic \
--entry-point=pubsub_handler \
--region=europe-west3 \
--max-instances=1 \
--timeout=60s \
--memory=256MiB \
--service-account=cloud-function-b@propane-nomad-396712.iam.gserviceaccount.com \
--ingress-settings=all \
--no-allow-unauthenticated \
--gen2 \
--source=./cloud_functions/code/6/subscriber/
```

Deploy cloud scheduler

```shell
gcloud scheduler jobs create http db-scheduler-pubsub-test \
--schedule="0 4 * * *" \
--http-method=POST \
--uri="https://europe-west3-propane-nomad-396712.cloudfunctions.net/db-func-pubsub-test" \
--message-body='{"project_id": "propane-nomad-396712", "bucket_name": "de-storage-447", "prefix_path": "dokkan-battle", "topic_name": "db-topic"}' \
--headers="Content-Type=application/json" \
--attempt-deadline=1800s \
--location='europe-west3' \
--oidc-service-account-email=cloud-scheduler@propane-nomad-396712.iam.gserviceaccount.com
```

Grant invoker role to cloud scheduler to invoke publisher

```shell
gcloud functions add-invoker-policy-binding db-func-pubsub-test \
    --member="serviceAccount:cloud-scheduler@propane-nomad-396712.iam.gserviceaccount.com" \
    --region='europe-west3'
```

Grant invoker role to publisher to invoke subscriber

```shell
gcloud functions add-invoker-policy-binding func-pubsub-subscriber-test \
    --member="serviceAccount:cloud-function-a@propane-nomad-396712.iam.gserviceaccount.com" \
    --region='europe-west3'
```
