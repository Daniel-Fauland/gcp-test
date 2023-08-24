# GCP Cloud Functions

This section will cover a few hands-on tutorials using GCP Cloud Functions and GCP Scheduler.

Contents:

1. [Cloud Functions HTTP trigger without authentication](#1-cloud-functions-http-trigger-without-authentication)
2. [Cloud Functions HTTP trigger with authentication](#2-cloud-functions-http-trigger-with-authentication)
3. [Parameterize script in cloud functions](#3-parameterize-script-in-cloud-functions)
4. [Schedule a non paremterized cloud function using Cloud Scheduler](#4-schedule-a-non-paremterized-cloud-function-using-cloud-scheduler)
5. [Schedule a parameterized cloud function using gcloud command line](#5-schedule-a-parameterized-cloud-function-using-gcloud-command-line)

In case you don't have your own python script for testing you can use the provided scripts for each chapter.

| Chapter                                                                           | Python script                                                                                                                 |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [chapter 1](#1-cloud-functions-http-trigger-without-authentication)               | [1-dbz_db-cloud_function-short.py](./code/1/1-dbz_db-cloud_function-short.py)                                                 |
| [chapter 2](#2-cloud-functions-http-trigger-with-authentication)                  | [1-dbz_db-cloud_function-short.py](./code/1/1-dbz_db-cloud_function-short.py)                                                 |
| [chapter 3](#3-parameterize-script-in-cloud-functions)                            | [3-dbz_db-cloud_function-short-parameterized.py](./code/3/3-dbz_db-cloud_function-short-parameterized.py)                     |
| [chapter 4](#4-schedule-a-non-paremterized-cloud-function-using-cloud-scheduler)  | [1-dbz_db-cloud_function-short.py](./code/1/1-dbz_db-cloud_function-short.py)                                                 |
| [chapter 5](#5-schedule-a-parameterized-cloud-function-using-gcloud-command-line) | [5-dbz_db-cloud_function-short-parameterized-scheduled.py](./code/5/5-dbz_db-cloud_function-short-parameterized-scheduled.py) |
| [chapter 6](#6-trigger-action-based-on-event-using-pubsub)                        | [publisher/main.py](./code/6/publisher/main.py) & [subscriber/main.py](./code/6/subscriber/main.py)                           |

As these scripts will create files in a csv storage bucket make sure you [create a gcp storage bucket](https://cloud.google.com/storage/docs/creating-buckets) and you adjust the gcp credentials _project_id_ & _bucket_name_ (in function _start_script_) in the python file.

## 1. Cloud Functions HTTP trigger without authentication

(Use [1-dbz_db-cloud_function-short.py](./code/1/1-dbz_db-cloud_function-short.py) if you don't have your own python script).

Simplest form of cloud function. HTTP trigger without authentication means that everyone who knows the url can trigger the functions from any console everywhere in the world without needing any kind of authentication.
In order to configue a cloud function without authentication follow these steps:

0. Make sure the GCP credentials are set accordingly in the python script (project & bucket name). The variables are in the function start_script
1. Go to Cloud Functions in GCP
2. Click on create function
3. Use 2nd gen env if possible (more features like higher runtime)
4. Choose a function name (e.g. _"db-func"_) and your preferred region (e.g. _"europe-west3"_)
5. Choose HTTP Trigger (usually preselected) and check _"Allow unauthenticated invocations"_
6. In the runtime section select your memory. (1Gib needed for this example)
7. Timeout let's you decide after how much time the function will abort (at least 15 minutes is needed for this example)
8. In the connections section you can select which traffic is allowed for your script. (_"Allow all traffic"_ is needed for this example as it pulls data from external websites)
9. Click on _"next"_ and select your runtime. (Choose python 3.10 or higher for this example)
10. Add your script to _main.py_
11. Define the _"Entry point"_. Here you can specify which function is called when the cloud function is triggered. Make sure that your function takes on argument which will always be sent when triggering the cloud function and returns something as otherwise you will get an error in the logs and also in the terminal in case you called the function manually. (Choose _start_script_ for this example)
12. Make sure to include all necessary packages in the _requirements.txt_ file. If you are using google.cloud storage package in your script it might be necessary to include the following as well in order to prevent import errors:

    ```shell
    google-api-core==2.11.1 ; python_version >= "3.10" and python_version < "4.0"
    google-auth==2.17.3 ; python_version >= "3.10" and python_version < "4.0"
    google-cloud-core==2.3.3 ; python_version >= "3.10" and python_version < "4.0"
    google-cloud-storage==2.10.0 ; python_version >= "3.10" and python_version < "4.0"
    google-crc32c==1.5.0 ; python_version >= "3.10" and python_version < "4.0"
    google-resumable-media==2.5.0 ; python_version >= "3.10" and python_version < "4.0"
    googleapis-common-protos==1.60.0 ; python_version >= "3.10" and python_version < "4.0"
    ```

13. Click _"deploy"_
14. Once deployment is complete you can trigger the cloud function from the console of your choice.

    General code snippet:

    ```shell
    curl <cloud-function-url>
    ```

    Example code snippet:

    ```shell
    curl https://europe-west3-propane-nomad-396712.cloudfunctions.net/db-func
    ```

15. You can check the logs in GCP within your clound function. All kind of print statements and/or erros and warnings in your python script will be displayed here.

## 2. Cloud Functions HTTP trigger with authentication

(Use [1-dbz_db-cloud_function-short.py](./code/1/1-dbz_db-cloud_function-short.py) if you don't have your own python script).

Prerequisites:

- Install the [GCP CLI](https://cloud.google.com/sdk/docs/install) to your local machine in case you want to trigger the cloud functions from your pc. After installing set your gcp project and test if it's working properly by executing the following statement in your terminal:

  ```shell
  gcloud auth login
  ```

- Check if your GCP role has has the necessary access:
  1. On the GCP go to IAM & ADMIN --> IAM
  2. Check your role (e.g. "Owner")
  3. Go to roles (scroll down a bit on the left menu bar)
  4. Find your rolen and open it
  5. Make sure that _"cloudfunctions.functions.invoke"_ is listed here

Follow the basic steps mentioned above but include following changes:

- Create a new cloud function and choose a different name (e.g. _"db-func-auth"_)
- Choose HTTP Trigger (usually preselected) and check _"Require authentication"_
- Once deployment is complete you can trigger the cloud function from the console of your choice:

  General code snippet:

  ```shell
  curl  -H "Authorization: bearer $(gcloud auth print-identity-token)" <cloud-function-url>
  ```

  Example code snippet:

  ```shell
  curl  -H "Authorization: bearer $(gcloud auth print-identity-token)" https://europe-west3-propane-nomad-396712.cloudfunctions.net/db-func-auth
  ```

## 3. Parameterize script in cloud functions

(Use [3-dbz_db-cloud_function-short-parameterized.py](./code/3/3-dbz_db-cloud_function-short-parameterized.py) if you don't have your own python script).

You can also parameterize your script in cloud functions. This is always recommended as you can use the same script for different instances/projects. Follow the basic steps mentioned in part 2 but include the following changes:

- Create a new cloud function and choose a different name (e.g. _"db-func-auth-params"_)
- In the code part make sure that you retrieve the arguments using the POST method:
  ```python
  project_id = request.form.get('project_id')  # use form.get for POST
  bucket_name = request.form.get('bucket_name')  # use form.get for POST
  ```
- You should also configure a return if no arguments were passed (as the script will continue and may fail at a later stage due to _None_ values) and/or define default values:

  ```python
  if project_id is None or bucket_name is None:
      return 'Error: Missing required parameters. You need the following curl command format:\ncurl -X POST -H "Authorization: bearer $(gcloud auth print-identity-token)" -d "project_id=your-project-id" -d "bucket_name=your-bucket" <cloud-function-url>'
  if project_id == "your-project-id" and bucket_name == "your-bucket":
      project_id = "default-project-id"
      bucket_name = "default-bucket"
  ```

- Once your cloud function is deployed you can use a terminal of your choice to call the cloud function and pass variables:

  General code snippet:

  ```shell
  curl -X POST -H "Authorization: bearer $(gcloud auth print-identity-token)" -d "project_id=your-project-id" -d "bucket_name=your-bucket" <cloud-function-url>
  ```

  Example code snippet:

  ```shell
  curl -X POST -H "Authorization: bearer $(gcloud auth print-identity-token)" -d "project_id=propane-nomad-396712" -d "bucket_name=de-storage-447" https://europe-west3-propane-nomad-396712.cloudfunctions.net/db-func-auth-params
  ```

## 4. Schedule a non paremterized cloud function using Cloud Scheduler

(Use [1-dbz_db-cloud_function-short.py](./code/1/1-dbz_db-cloud_function-short.py) if you don't have your own python script).

We will schedule the cloud function deployed in step 3.
Note that it is not possible to pass arguments

1. Go to Cloud Scheduler and click _"Create job"_
2. Choose your preferred name, region and give a description
3. Enter your desired frequency as a cron time. A tool to easily setup your desired cron schedule is called [crontab guru](https://crontab.guru). In our example we will use the following cron time to run the script every day at 6am.
   ```shell
   0 6 * * *
   ```
4. In order to avoid any conflicts with timezones affected by Daylight Saving Time (DST) it is recommended to choose _"Coordinated Universal Time (UTC)"_ as the timezone
5. Under the section _"Configure the execution"_ choose _"HTTP"_ as the target type
6. Enter your cloud functions url
7. HTTP method is "_POST_" in most cases
8. If your cloud function needs authentication you must add a Header. Name 1 = "Authentication" and Value 1 = "_your-identity-token_". You can get the identity token by running the following command in your terminal (GCP CLI required):
   ```shell
   gcloud auth print-identity-token
   ```
9. Under the section _"Configure optional settings"_ you can specify the retries amount in case your cloud function fails.
10. With the option _"Attempt deadline config"_ you can configure when the cloud scheduler will abort the task. The maximum duration that can be selected is 30 minutes. Therefore it effectively limits the runtime of a scheduled cloud function to 30 minutes as it will abort otherwise. (For this example select 30 minutes)
11. Create the schedule. **Note:** The _"Status of last execution"_ will only update after the script either finishes sucessfully or throws any kind of exception

## 5. Schedule a parameterized cloud function using gcloud command line

(Use [5-dbz_db-cloud_function-short-parameterized-scheduled.py](./code/5/5-dbz_db-cloud_function-short-parameterized-scheduled.py) if you don't have your own python script).

Following the steps mentioned in [chapter 4](#4-schedule-a-non-paremterized-cloud-function-using-cloud-scheduler) won't work if you want to pass variables with cloud scheduler.
However it is possible to pass a json object.

1. An adjustment in the python script is needed to process json
   ```python
   data = request.get_json()  # Get the JSON data from the payload
   project_id = data.get('project_id')
   bucket_name = data.get('bucket_name')
   ```
2. In the header part we need to set _Content-Type=application/json_ otherwise python only retrieves _None_ values for the json object
3. In the message body part we can specify the json we want to pass to the python script
4. It's possible to completely configure/deploy the cloud scheduler using gcloud. It can be used from any terminal as long as it has gcloud CLI installed, the user is authenticated and has the permission (_cloudscheduler.jobs.create_) to create a cloud schedule job.

   General code snippet:

   ```shell
   gcloud scheduler jobs create http <schedule-name> \
   --schedule="0 4 * * *" \
   --http-method=POST \
   --uri="your-cloud-functions-url" \
   --message-body='{"project_id": "your-project-id", "bucket_name": "your-bucket"}' \
   --headers="Authorization=Bearer $(gcloud auth print-identity-token),Content-Type=application/json" \
   --attempt-deadline=1800s \
   --location='your-region'
   ```

   Example code snippet:

   ```shell
   gcloud scheduler jobs create http db-scheduler-gcloud \
   --schedule="0 4 * * *" \
   --http-method=POST \
   --uri="https://europe-west3-propane-nomad-396712.cloudfunctions.net/dokkan-battle-function-parameterized" \
   --message-body='{"project_id": "propane-nomad-396712", "bucket_name": "de-storage-447"}' \
   --headers="Authorization=Bearer $(gcloud auth print-identity-token),Content-Type=application/json" \
   --attempt-deadline=1800s \
   --location='europe-west3'
   ```

5. Optional: It's also possible to manully trigger the cloud function and pass a json object using _curl_:

   General code snippet:

   ```shell
   curl -X POST -H "Authorization: bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" -d '{"project_id": "your-project-id", "bucket_name": "your-bucket-name"}' <cloud-function-url>
   ```

   Example code snippet:

   ```shell
   curl -X POST -H "Authorization: bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" -d '{"project_id": "propane-nomad-396712", "bucket_name": "de-storage-447"}' https://europe-west3-propane-nomad-396712.cloudfunctions.net/dokkan-battle-function-parameterized
   ```

## 6. Trigger action based on event using Pub/Sub

(Use [6-dbz_db-cloud_function-short-pubsub.py)](./code/6/publisher/6-dbz_db-cloud_function-short-pubsub.py) and [6-pubsub-action.py](./code/6/subscriber/6-pubsub-action.py) if you don't have your own python script)

If you want to schedule certain tasks event based instead instead of time based you can use a service like [Pub/Sub](https://cloud.google.com/pubsub/docs/overview). The example python script will create files in the gcp storage bucket with a timestamp. One way of deleting older files within this bucket is to setup a "clean-up" cloud function that is triggered whenever cloud scheduler successfully executed the main cloud function. In this particular use case, alternative (faster) solutions are available, such as implementing file retention within a GCP storage bucket. However, it's important to note that these alternatives are static in nature. They would consistently delete files once the defined retention period is met, regardless of whether cloud functions have effectively generated these files.
In order to setup a Pub/Sub a few steps are necessary:

1.  Prepare a script for another cloud function that will be triggered by the Pub/Sub setup. (e.g. [6-pubsub-action.py](./code/6/subscriber/6-pubsub-action.py))
2.  In your main cloud function script you need to specify a publish message for your Pub/Sub setup. Therefore you need to add something like this at the end of your sript:

    ```python
    from google.cloud import pubsub_v1

        # Publish a message to the Pub/Sub topic
        publisher = pubsub_v1.PublisherClient()
        topic_path = f'projects/{project_id}/topics/{topic_name}'
        data = {"project_id": project_id, "bucket_name": bucket_name}
        publisher.publish(topic_path, data=data)
    ```

    It's a good idea to parameterize the main cloud function and the second cloud function that will be triggered by your Pub/Sub setup so that you only need to changes variables in your cloud scheduler

3.  Now you need to create the Pub/Sub topic where your main cloud function can actually publish a message to. This can be done easily via gcloud in terminal.

    General code snippet:

    ```shell
    gcloud pubsub topics <topic-name>
    ```

    Example code snippet:

    ```shell
    gcloud pubsub topics create db-topic
    ```

4.  Now deploy the main function using http trigger. This function will later be triggered by cloud scheduler. This can also be deployed via gcloud command.

    General code snippet:

    ```shell
    gcloud functions deploy <function-name> \
    --runtime=python310 \
    --trigger-http \
    --entry-point=entry_point \
    --region=region \
    --max-instances=1 \
    --timeout=3500s \
    --memory=1GiB \
    --service-account=<your-service-acc> \
    --ingress-settings=all \
    --gen2 \
    --source=./path/to/directory/
    ```

    Example code snippet:

    ```shell
    gcloud functions deploy db-func-pubsub \
    --runtime=python310 \
    --trigger-http \
    --entry-point=start_script \
    --region=europe-west3 \
    --max-instances=1 \
    --timeout=3500s \
    --memory=1GiB \
    --service-account=973117053722-compute@developer.gserviceaccount.com \
    --ingress-settings=all \
    --no-allow-unauthenticated \
    --gen2 \
    --source=./cloud_functions/code/6/publisher/
    ```

5.  Now deploy the other cloud function using Pub/Sub trigger which will be executed once the main cloud function publishes a message on a topic this function is subscribed to.

    General code snippet:

    ```shell
    gcloud functions deploy <function-name> \
    --runtime=python310 \
    --trigger-topic=<topic-name> \
    --entry-point=pubsub_handler \
    --region=region \
    --max-instances=1 \
    --timeout=60s \
    --memory=256MiB \
    --service-account=<your-service-acc> \
    --ingress-settings=all \
    --gen2 \
    --source=./path/to/directory/
    ```

    Example code snippet:

    ```shell
    gcloud functions deploy func-pubsub-subscriber \
    --runtime=python310 \
    --trigger-topic=db-topic \
    --entry-point=pubsub_handler \
    --region=europe-west3 \
    --max-instances=1 \
    --timeout=120s \
    --memory=256MiB \
    --service-account=973117053722-compute@developer.gserviceaccount.com \
    --ingress-settings=all \
    --allow-unauthenticated \
    --gen2 \
    --source=./cloud_functions/code/6/subscriber/
    ```

6.  Optional: Deploy a Cloud scheduler that will run your pubsub function on a daily basis.

    General code snippet:

    ```shell
    gcloud scheduler jobs create http db-scheduler-pubsub \
    --schedule="0 4 * * *" \
    --http-method=POST \
    --uri="your-cloud-functions-url" \
    --message-body='{"project_id": "your-project-id", "bucket_name": "your-bucket", "topic_name": "your-topic"}' \
    --headers="Authorization=Bearer $(gcloud auth print-identity-token),Content-Type=application/json" \
    --attempt-deadline=1800s \
    --location='your-region'
    ```

    Example code snippet:

    ```shell
    gcloud scheduler jobs create http <schedule-name> \
    --schedule="0 4 * * *" \
    --http-method=POST \
    --uri="https://europe-west3-propane-nomad-396712.cloudfunctions.net/db-func-pubsub" \
    --message-body='{"project_id": "propane-nomad-396712", "bucket_name": "de-storage-447", "prefix_path": "dokkan-battle", "topic_name": "db-topic"}' \
    --headers="Authorization=Bearer $(gcloud auth print-identity-token),Content-Type=application/json" \
    --attempt-deadline=1800s \
    --location='europe-west3'
    ```
