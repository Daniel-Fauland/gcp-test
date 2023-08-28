# GCP Cloud Functions

This section will cover a few hands-on tutorials using GCP Cloud Functions and GCP Scheduler.

**Contents:**

1. [Cloud Functions HTTP trigger without authentication](#1-cloud-functions-http-trigger-without-authentication)
2. [Cloud Functions HTTP trigger with authentication](#2-cloud-functions-http-trigger-with-authentication)
3. [Parameterize script in cloud functions](#3-parameterize-script-in-cloud-functions)
4. [Schedule a non paremterized cloud function using Cloud Scheduler](#4-schedule-a-non-paremterized-cloud-function-using-cloud-scheduler)
5. [Schedule a parameterized cloud function using gcloud command line](#5-schedule-a-parameterized-cloud-function-using-gcloud-command-line)
6. [Trigger action based on event using Pub/Sub with 2 different service accounts](#6-trigger-action-based-on-event-using-pubsub-with-2-different-service-accounts)
7. [Insert data from a cloud function into a BigQuery table](#7-insert-data-from-a-cloud-function-into-a-bigquery-table)

In case you don't have your own python script for testing you can use the provided scripts for each chapter.

| Chapter                                                                                      | Python script                                                                                                                 |
| -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [chapter 1](#1-cloud-functions-http-trigger-without-authentication)                          | [1-dbz_db-cloud_function-short.py](./code/1/1-dbz_db-cloud_function-short.py)                                                 |
| [chapter 2](#2-cloud-functions-http-trigger-with-authentication)                             | [1-dbz_db-cloud_function-short.py](./code/1/1-dbz_db-cloud_function-short.py)                                                 |
| [chapter 3](#3-parameterize-script-in-cloud-functions)                                       | [3-dbz_db-cloud_function-short-parameterized.py](./code/3/3-dbz_db-cloud_function-short-parameterized.py)                     |
| [chapter 4](#4-schedule-a-non-paremterized-cloud-function-using-cloud-scheduler)             | [1-dbz_db-cloud_function-short.py](./code/1/1-dbz_db-cloud_function-short.py)                                                 |
| [chapter 5](#5-schedule-a-parameterized-cloud-function-using-gcloud-command-line)            | [5-dbz_db-cloud_function-short-parameterized-scheduled.py](./code/5/5-dbz_db-cloud_function-short-parameterized-scheduled.py) |
| [chapter 6](#6-trigger-action-based-on-event-using-pubsub-with-2-different-service-accounts) | [6/publisher/main.py](./code/6/publisher/main.py) & [6/subscriber/main.py](./code/6/subscriber/main.py)                       |
| [chapter 7](#7-insert-data-from-a-cloud-function-into-a-bigquery-table)                      | [7/publisher/main.py](./code/7/publisher/main.py) & [7/subscriber/main.py](./code/7/subscriber/main.py)                       |

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
6. In the runtime section select your memory
7. Timeout let's you decide after how much time the function will abort
8. In the connections section you can select which traffic is allowed for your script. (_"Allow all traffic"_ is needed for this example as it pulls data from external websites)
9. Click on _"next"_ and select your runtime. (Choose python 3.10 or higher for this example)
10. Add your script to _main.py_
11. Define the _"Entry point"_. Here you can specify which function is called when the cloud function is triggered. Make sure that your function takes on argument which will always be sent when triggering the cloud function and returns something as otherwise you will get an error in the logs and also in the terminal in case you called the function manually. (Choose _start_script_ for this example)
12. Make sure to include all necessary packages in the _requirements.txt_ file. If you are using google.cloud storage package in your script it might be necessary to include the following as well in order to prevent import errors:

    <details>
    <summary>Show requirements:</summary>

    ```shell
    google-api-core==2.11.1 ; python_version >= "3.10" and python_version < "4.0"
    google-auth==2.17.3 ; python_version >= "3.10" and python_version < "4.0"
    google-cloud-core==2.3.3 ; python_version >= "3.10" and python_version < "4.0"
    google-cloud-storage==2.10.0 ; python_version >= "3.10" and python_version < "4.0"
    google-crc32c==1.5.0 ; python_version >= "3.10" and python_version < "4.0"
    google-resumable-media==2.5.0 ; python_version >= "3.10" and python_version < "4.0"
    googleapis-common-protos==1.60.0 ; python_version >= "3.10" and python_version < "4.0"
    ```

    </details>
    <br />

13. Click _"deploy"_
14. Once deployment is complete you can trigger the cloud function from the console of your choice.

    <details>
    <summary>Show general code snippet:</summary>

    ```shell
    curl <cloud-function-url>
    ```

    </details>

    <details open>
    <summary>Show example code snippet:</summary>

    ```shell
    curl https://europe-west3-propane-nomad-396712.cloudfunctions.net/db-func
    ```

    </details>

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

  <details>
  <summary>Show general code snippet:</summary>

  ```shell
  curl  -H "Authorization: bearer $(gcloud auth print-identity-token)" <cloud-function-url>
  ```

  </details>

  <details open>
  <summary>Show example code snippet:</summary>

  ```shell
  curl  -H "Authorization: bearer $(gcloud auth print-identity-token)" https://europe-west3-propane-nomad-396712.cloudfunctions.net/db-func-auth
  ```

  </details>

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

  <details>
  <summary>Show general code snippet:</summary>

  ```shell
  curl -X POST -H "Authorization: bearer $(gcloud auth print-identity-token)" -d "project_id=your-project-id" -d "bucket_name=your-bucket" <cloud-function-url>
  ```

  </details>

  <details open>
  <summary>Show example code snippet:</summary>

  ```shell
  curl -X POST -H "Authorization: bearer $(gcloud auth print-identity-token)" -d "project_id=propane-nomad-396712" -d "bucket_name=de-storage-447" https://europe-west3-propane-nomad-396712.cloudfunctions.net/db-func-auth-params
  ```

  </details>

## 4. Schedule a non parameterized cloud function using Cloud Scheduler

(Use [1-dbz_db-cloud_function-short.py](./code/1/1-dbz_db-cloud_function-short.py) if you don't have your own python script).

**Prerequisites:**
You should create a service account for Cloud scheduler. This is needed in order to invoke cloud functions that require authentication. A guide how to create a service account can be found [here](../iam/README.md).

Schedule the cloud function deployed in step 2. <br />
**Note:** It is not possible to pass arguments this way. If you want to pass one or more arguments through the cloud scheduler refer to [chapter 5](#5-schedule-a-parameterized-cloud-function-using-gcloud-command-line).

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
8. If your cloud function needs authentication you must use OIDC or OAuth. OIDC is preferred as it can be used to authenticate not only internal gcp services but third party services as well.
   It is effectivly not possible to use the identity token as shown in [chapter 2](#2-cloud-functions-http-trigger-with-authentication) or [chapter 3](#3-parameterize-script-in-cloud-functions). You could in theory get the current identity token and add "Authenticaton" as key and your token as value in the HTTP Header. However the identity token runs out after 60 minutes. Therefore using a static token with limited lifespan makes the cloud scheduler effectively useless. This is why you should authenticate your cloud resources with a service account instead. <br />
   Select OIDC as auth header and choose your service account. Audience can be left blank as it will default to your cloud function url anyway.
9. Under the section _"Configure optional settings"_ you can specify the retries amount in case your cloud function fails.
10. With the option _"Attempt deadline config"_ you can configure when the cloud scheduler will abort the task. The maximum duration that can be selected is 30 minutes. Therefore it effectively limits the runtime of a scheduled cloud function to 30 minutes as it will abort otherwise.
11. Create the schedule. **Note:** The _"Status of last execution"_ will only update after the script either finishes sucessfully or returns any kind of exception (assuming permissions are granted to invoke the cloud function)
12. **Important:** You must assign the Invoker role (roles/run.invoker) through Cloud Run for 2nd gen functions if you want to allow the function to receive requests from additional principals or other given authorities in IAM. Therefore you need to grant the cloud function the permission to be invoked by a service account.

    <details>
    <summary>Show general code snippet:</summary>

    ```shell
    gcloud functions add-invoker-policy-binding <function-name> \
        --member="serviceAccount:<service-acc-name>@<project-id>.iam.gserviceaccount.com" \
        --region='<your-region>'
    ```

    </details>

    <details open>
    <summary>Show example code snippet:</summary>

    ```shell
    gcloud functions add-invoker-policy-binding test-func-scheduled \
        --member="serviceAccount:cloud-scheduler@propane-nomad-396712.iam.gserviceaccount.com" \
        --region='europe-west3'
    ```

    </details>

    Keep in mind that it can take a few minutes until the permissions granted this way take effect. If cloud scheduler fails to invoke the cloud function shortly after deploying wait a few minutes and try again.

## 5. Schedule a parameterized cloud function using gcloud command line

(Use [5-dbz_db-cloud_function-short-parameterized-scheduled.py](./code/5/5-dbz_db-cloud_function-short-parameterized-scheduled.py) if you don't have your own python script).

Following the steps mentioned in [chapter 4](#4-schedule-a-non-paremterized-cloud-function-using-cloud-scheduler) won't work if you want to pass variables with cloud scheduler.
However it is possible to pass a json object instead.

1. An adjustment in the python script is needed to process json
   ```python
   data = request.get_json()  # Get the JSON data from the payload
   project_id = data.get('project_id')
   bucket_name = data.get('bucket_name')
   ```
2. In the header part you need to set _Content-Type=application/json_ otherwise python only retrieves _None_ values for the json object
3. In the message body part we can specify the json we want to pass to the python script
4. It's possible to completely configure/deploy the cloud scheduler using gcloud. It can be used from any terminal as long as it has gcloud CLI installed, the user is authenticated and has the permission (_cloudscheduler.jobs.create_) to create a cloud schedule job.

    <details>
    <summary>Show general code snippet:</summary>

   ```shell
   gcloud scheduler jobs create http <schedule-name> \
   --schedule="0 4 * * *" \
   --http-method=POST \
   --uri="your-cloud-functions-url" \
   --message-body='{"project_id": "your-project-id", "bucket_name": "your-bucket"}' \
   --headers="Content-Type=application/json" \
   --attempt-deadline=60s \
   --location='your-region' \
   --oidc--service-account-email=<service-acc-name>@<project-id>.iam.gserviceaccount.com
   ```

   </details>

    <details open>
    <summary>Show example code snippet:</summary>

   ```shell
   gcloud scheduler jobs create http db-scheduler-gcloud \
   --schedule="0 4 * * *" \
   --http-method=POST \
   --uri="https://europe-west3-propane-nomad-396712.cloudfunctions.net/dokkan-battle-function-parameterized" \
   --message-body='{"project_id": "propane-nomad-396712", "bucket_name": "de-storage-447"}' \
   --headers="Content-Type=application/json" \
   --attempt-deadline=1800s \
   --location='europe-west3' \
   --oidc-service-account-email=cloud-scheduler@propane-nomad-396712.iam.gserviceaccount.com
   ```

   </details>

5. You must assign the Invoker role (roles/run.invoker) through Cloud Run for 2nd gen functions if you want to allow the function to receive requests from additional principals or other given authorities in IAM. Therefore you need to grant the cloud function the permission to be invoked by a service account.

    <details>
    <summary>Show general code snippet:</summary>

   ```shell
   gcloud functions add-invoker-policy-binding <function-name> \
       --member="serviceAccount:<service-acc-name>@<project-id>.iam.gserviceaccount.com" \
       --region='<your-region>'
   ```

   </details>

    <details open>
    <summary>Show example code snippet:</summary>

   ```shell
   gcloud functions add-invoker-policy-binding dokkan-battle-function-parameterized \
       --member="serviceAccount:cloud-scheduler@propane-nomad-396712.iam.gserviceaccount.com" \
       --region='europe-west3'
   ```

   </details>

   Keep in mind that it can take a few minutes until the permissions granted this way take effect. If cloud scheduler fails to invoke the cloud function shortly after deploying wait a few minutes and try again.

6. Optional: It's also possible to manully trigger the cloud function and pass a json object using _curl_:

    <details>
    <summary>Show general code snippet:</summary>

   ```shell
   curl -X POST -H "Authorization: bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" -d '{"project_id": "your-project-id", "bucket_name": "your-bucket-name"}' <cloud-function-url>
   ```

   </details>

    <details open>
    <summary>Show example code snippet:</summary>

   ```shell
   curl -X POST -H "Authorization: bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" -d '{"project_id": "propane-nomad-396712", "bucket_name": "de-storage-447"}' https://europe-west3-propane-nomad-396712.cloudfunctions.net/dokkan-battle-function-parameterized
   ```

   </details>

## 6. Trigger action based on event using Pub/Sub with 2 different service accounts

(Use [6/publisher/main.py)](./code/6/publisher/main.py) and [6/subscriber/main.py](./code/6/subscriber/main.py) if you don't have your own python script).

If you want to schedule certain tasks event based instead instead of time based you can use a service like [Pub/Sub](https://cloud.google.com/pubsub/docs/overview). The example python script will create files in the gcp storage bucket with a timestamp. One way of deleting older files within this bucket is to setup a "clean-up" cloud function that is triggered whenever cloud scheduler successfully executed the main cloud function. In this particular use case, alternative (faster) solutions are available, such as implementing file retention within a GCP storage bucket. However, it's important to note that these alternatives are static in nature. They would consistently delete files once the defined retention period is met, regardless of whether cloud functions have effectively generated these files.

In this example 2 different service accounts for function A and function B are used.
In order to setup a Pub/Sub a few steps are necessary:

1.  Prepare a script for another cloud function that will be triggered by the Pub/Sub setup. (e.g. [6/subscriber/main.py](./code/6/subscriber/main.py))
2.  In your main cloud function script you need to specify a publish message for your Pub/Sub setup. Therefore you need to add something like this at the end of your sript:

    ```python
    from google.cloud import pubsub_v1

        # Publish a message to the Pub/Sub topic
        publisher = pubsub_v1.PublisherClient()
        topic_path = f'projects/{project_id}/topics/{topic_name}'
        data = {"project_id": project_id, "bucket_name": bucket_name}
        publisher.publish(topic_path, data=data)
    ```

    It's a good idea to parameterize the main cloud function and the second cloud function that will be triggered by your Pub/Sub setup so that you only need to change variables in your cloud scheduler. The full script can be found in [6/publisher/main.py](./code/6/publisher/main.py).

3.  [Create a service account](../iam/README.md#create-service-account) for cloud function **A** which will be the **publisher** of the pub/sub topic. Choose a name (e.g. _sa-func-a_) and grant the following roles:

    - Pub/Sub Publisher: This role allows the service account to publish messages to a Pub/Sub topic
    - Storage Admin: This role allows the service account to list, view, create and delete buckets & objects in cloud storage (This is needed as the example python script creates files in cloud storage)

4.  [Create a service account](../iam/README.md#create-service-account) for cloud function **B** which will be the **subscribe** to the pub/sub topic. Choose a name (e.g. _sa-func-b_) and grant the following roles:

    - Pub/Sub Subscriber: This role allows the service account to receive messages from a Pub/Sub topic
    - Storage Admin: This role allows the service account to list, view, create and delete buckets & objects in cloud storage (This is needed as the example python script will list objects in the bucket and delete those objects)
    - Cloud Functions Invoker: This role allows the cloud function to invoke another cloud function. This is needed because after receiving a Pub/Sub message this service account will invoke the cloud function B.

    **Note:** If you use the same service account for both cloud functions you would need to grant all the permissions listed for _sa-func-a_ and _sa-func-b_. You can easily check the set roles for your service account using gcloud as demonstrated [here](../iam/README.md#view-roles-granted-to-an-existing-service-account).

5.  Now you need to create the Pub/Sub topic itself where your main cloud function can actually publish a message to. This can be done easily via gcloud in terminal.

    <details>
    <summary>Show general code snippet:</summary>

    ```shell
    gcloud pubsub topics <topic-name>
    ```

    </details>

    <details open>
    <summary>Show example code snippet:</summary>

    ```shell
    gcloud pubsub topics create my-topic
    ```

    </details>

6.  Now deploy the main function using http trigger. This function will later be triggered by cloud scheduler. This can also be deployed via gcloud command.

    <details>
    <summary>Show general code snippet:</summary>

    ```shell
    gcloud functions deploy <function-name> \
    --runtime=python310 \
    --trigger-http \
    --entry-point=entry_point \
    --region=region \
    --max-instances=1 \
    --timeout=60s \
    --memory=256MiB \
    --service-account=<your-service-acc> \
    --ingress-settings=all \
    --no-allow-unauthenticated \
    --gen2 \
    --source=./path/to/directory/
    ```

    </details>

    <details open>
    <summary>Show example code snippet:</summary>

    ```shell
    gcloud functions deploy cf-func-a \
    --runtime=python310 \
    --trigger-http \
    --entry-point=start_script \
    --region=europe-west3 \
    --max-instances=1 \
    --timeout=3500s \
    --memory=1GiB \
    --service-account=sa-func-a@propane-nomad-396712.iam.gserviceaccount.com \
    --ingress-settings=all \
    --no-allow-unauthenticated \
    --gen2 \
    --source=./cloud_functions/code/6/publisher/
    ```

    </details>

7.  Now deploy the other cloud function using Pub/Sub trigger which will be executed once the main cloud function publishes a message on a topic this function is subscribed to.

    <details>
    <summary>Show general code snippet:</summary>

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

    </details>

    <details open>
    <summary>Show example code snippet:</summary>

    ```shell
    gcloud functions deploy cf-func-b \
    --runtime=python310 \
    --trigger-topic=my-topic \
    --entry-point=pubsub_handler \
    --region=europe-west3 \
    --max-instances=1 \
    --timeout=60s \
    --memory=256MiB \
    --service-account=sa-func-b@propane-nomad-396712.iam.gserviceaccount.com \
    --ingress-settings=all \
    --no-allow-unauthenticated \
    --gen2 \
    --source=./cloud_functions/code/6/subscriber/
    ```

    </details>

8.  Optional: Deploy a Cloud scheduler that will run your pubsub function on a daily basis.

    <details>
    <summary>Show general code snippet:</summary>

    ```shell
    gcloud scheduler jobs create http <schedule-name> \
    --schedule="0 4 * * *" \
    --http-method=POST \
    --uri="your-cloud-functions-url" \
    --message-body='{"key": "value"}' \
    --headers="Content-Type=application/json" \
    --attempt-deadline=1800s \
    --location='your-region' \
    --oidc--service-account-email=<service-acc-name>@<project-id>.iam.gserviceaccount.com
    ```

    </details>

    <details open>
    <summary>Show example code snippet:</summary>

    ```shell
    gcloud scheduler jobs create http func-a-scheduler \
    --schedule="0 4 * * *" \
    --http-method=POST \
    --uri="https://europe-west3-propane-nomad-396712.cloudfunctions.net/cf-func-a" \
    --message-body='{"project_id": "propane-nomad-396712", "bucket_name": "de-storage-447", "prefix_path": "dokkan-battle", "topic_name": "my-topic"}' \
    --headers="Content-Type=application/json" \
    --attempt-deadline=1800s \
    --location='europe-west3' \
    --oidc-service-account-email=cloud-scheduler@propane-nomad-396712.iam.gserviceaccount.com
    ```

    </details>

9.  You must assign the Invoker role (roles/run.invoker) through Cloud Run for 2nd gen functions if you want to allow the function to receive requests from additional principals or other given authorities in IAM. Therefore you need to grant the cloud function the permission to be invoked by a service account.

    <details>
    <summary>Show general code snippet:</summary>

    ```shell
    gcloud functions add-invoker-policy-binding <function-name> \
        --member="serviceAccount:<service-acc-name>@<project-id>.iam.gserviceaccount.com" \
        --region='<your-region>'
    ```

    </details>

    <details open>
    <summary>Show example code snippet:</summary>

    ```shell
    gcloud functions add-invoker-policy-binding cf-func-a \
        --member="serviceAccount:cloud-scheduler@propane-nomad-396712.iam.gserviceaccount.com" \
        --region='europe-west3'
    ```

    </details>

    Keep in mind that it can take a few minutes until the permissions granted this way take effect. If cloud scheduler fails to invoke the cloud function shortly after deploying wait a few minutes and try again.

10. You also need to grant the service account of function B (e.g. _sa-func-b_) the permission to invoke function B (e.g. cf-func-b):

    <details>
    <summary>Show general code snippet:</summary>

    ```shell
    gcloud functions add-invoker-policy-binding <function-name> \
        --member="serviceAccount:<service-acc-name>@<project-id>.iam.gserviceaccount.com" \
        --region='<your-region>'
    ```

    </details>

    <details open>
    <summary>Show example code snippet:</summary>

    ```shell
    gcloud functions add-invoker-policy-binding cf-func-b \
        --member="serviceAccount:sa-func-b@propane-nomad-396712.iam.gserviceaccount.com" \
        --region='europe-west3'
    ```

    </details>

    Keep in mind that it can take a few minutes until the permissions granted this way take effect. If cloud scheduler fails to invoke the cloud function shortly after deploying wait a few minutes and try again.yy

## 7. Insert data from a cloud function into a BigQuery table

(Use [6/publisher/main.py)](./code/6/publisher/main.py) and [6/subscriber/main.py](./code/6/subscriber/main.py) if you don't have your own python script).

If you want to store the results or some kind of metadata of a cloud function in a database you can use BigQuery for instance.
The example script used in [chapter 6](#6-trigger-action-based-on-event-using-pubsub-with-2-different-service-accounts) creates a csv file which will be stored on cloud storage. You could for example store the number of rows, the file size and the timestamp of creation in a BQ table.
There are several different ways to implement this assuming the resources deployed in chapter 6 are still active:

1. Only adjust the python code in the [publisher/main.py](./code/6/publisher/main.py) file to send data to BigQuery
2. Create a new cloud function that listens to the same Pub/Sub topic and adjust the json that is being published by the [publisher/main.py](./code/6/publisher/main.py)
3. Create a new cloud function and a new Pub/Sub topic and adjust the code in [publisher/main.py](./code/6/publisher/main.py) to publish a new message to the new Pub/Sub topic

In this tutorial option **3** will be shown:

1. For deploying a BigQuery table refer to this [guide](../bigquery/README.md).
2. An adjustment in the publisher python script is necessary to retrieve the data that should be stored in BigQuery and in order to publish a message to a new Pub/Sub topic:

   ```python
   # Get the data that will later be sent to BigQuery
   def prepare_bigquery_data(df, storage_client, bucket_name, prefix_path, fname, current_timestamp, dataset_name, table_name, project_id):
       row_count = len(df)
       csv_size = int(df.memory_usage(deep=True).sum() / 1024)  # in KB
       blob_name = f'{prefix_path}/{current_timestamp}-{fname}.csv'
       blob = storage_client.get_bucket(bucket_name).get_blob(blob_name)
       blob_size = int(blob.size / 1024)  # in KB
       timestamp = datetime.now()  # UTC timestamp
       bq_data = {"project_id": project_id, "dataset_name": dataset_name, "table_name": table_name, "row_count": row_count, "csv_size": csv_size, "blob_size": blob_size, "timestamp": timestamp}
       return bq_data
   ```

   ```python
   # Publish the message to the new topic
   def start_script(request):
       topic_name2 = data.get('topic_name2')
       dataset_name = data.get('dataset_name')
       table_name = data.get('table_name')
       # ...
       bq_data = prepare_bigquery_data(characters_df, storage_client, bucket_name, prefix_path, fname_characters, timestamp_characters, dataset_name, table_name, project_id)
       # ...
       topic_path = f'projects/{project_id}/topics/{topic_name2}'
       bq_data_str = json.dumps(bq_data).encode('utf-8')  # Convert dictionary to JSON-encoded bytestring
       publisher.publish(topic_path, data=bq_data_str)
       print(f"Printing new json message being published to topic ({topic_name2}): {bq_data}")
   ```

   **Note:** The complete python script can be found in [7/publisher/main.py](./code/7/publisher/main.py)

3. Create a new cloud function that will insert the data in BigQuery. For example [7/subscriber/main.py](./code/7/subscriber/main.py). For this cloud function the bigquery package is required:

   ```shell
   google-cloud-bigquery==3.11.4 ; python_version >= "3.10" and python_version < "4.0"
   ```

4. Create a new Pub/Sub topic:

    <details>
    <summary>Show general code snippet:</summary>

   ```shell
   gcloud pubsub topics <topic-name>
   ```

   </details>

    <details open>
    <summary>Show example code snippet:</summary>

   ```shell
   gcloud pubsub topics create new-topic
   ```

   </details>

5. Now update the publisher function assuming it is still running on gcp using gcloud:

    <details>
    <summary>Show general code snippet:</summary>

   ```shell
   gcloud functions deploy <function-name> \
   --entry-point=entry_point \
   --region=region \
   --source=./path/to/directory/
   ```

   </details>

    <details open>
    <summary>Show example code snippet:</summary>

   ```shell
   gcloud functions deploy cf-func-a \
   --entry-point=start_script \
   --region=europe-west3 \
   --source=./cloud_functions/code/7/publisher/
   ```

   </details>

6. For the new cloud function you can either create a new service account or use an existing service account. In this example the same service account as cloud function B in the previous example will be used.

    <details>
    <summary>Show general code snippet:</summary>

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

   </details>

    <details open>
    <summary>Show example code snippet:</summary>

   ```shell
   gcloud functions deploy cf-func-c \
   --runtime=python310 \
   --trigger-topic=new-topic \
   --entry-point=pubsub_handler \
   --region=europe-west3 \
   --max-instances=1 \
   --timeout=60s \
   --memory=256MiB \
   --service-account=sa-func-b@propane-nomad-396712.iam.gserviceaccount.com \
   --ingress-settings=all \
   --no-allow-unauthenticated \
   --gen2 \
   --source=./cloud_functions/code/7/subscriber/
   ```

7. Now the service account used for the new subscriber functions needs the permission to invoke the new cloud function:

    <details>
    <summary>Show general code snippet:</summary>

   ```shell
   gcloud functions add-invoker-policy-binding <function-name> \
       --member="serviceAccount:<service-acc-name>@<project-id>.iam.gserviceaccount.com" \
       --region='<your-region>'
   ```

   </details>

    <details open>
    <summary>Show example code snippet:</summary>

   ```shell
   gcloud functions add-invoker-policy-binding cf-func-c \
       --member="serviceAccount:sa-func-b@propane-nomad-396712.iam.gserviceaccount.com" \
       --region='europe-west3'
   ```

   </details>

8. Since the new cloud function access BigQuery the underlying service account _sa-func-b_ in this example needs the bigquery.admin role.

    <details>
    <summary>Show general code snippet:</summary>

   ```shell
   gcloud projects add-iam-policy-binding <project-id> \
       --member="serviceAccount:<your-service-acc>@<project-id>.iam.gserviceaccount.com" \
       --role="roles/<resource>.<type>"
   ```

   </details>

    <details open>
    <summary>Show example code snippet:</summary>

   ```shell
   gcloud projects add-iam-policy-binding propane-nomad-396712 \
       --member="serviceAccount:sa-func-b@propane-nomad-396712.iam.gserviceaccount.com" \
       --role="roles/bigquery.admin"
   ```

   </details>

9. Update the cloud scheduler assuming it is still running on gcp

    <details>
    <summary>Show general code snippet:</summary>

   ```shell
   gcloud scheduler jobs update http <schedule-name> \
   --location=<your-region> \
   --message-body='{"updated_key": "updated_value"}'
   ```

   </details>

    <details open>
    <summary>Show example code snippet:</summary>

   ```shell
   gcloud scheduler jobs update http func-a-scheduler \
   --location=europe-west3 \
   --message-body='{"project_id": "propane-nomad-396712", "bucket_name": "de-storage-447", "prefix_path": "dokkan-battle", "topic_name": "my-topic", "topic_name2": "new-topic", "dataset_name": "my_data", "table_name": "db_table"}'
   ```

   </details>

## 8. Cloud function deployment using terraform (COMING SOON)

For deploying a cloud function using terraform refer to this [guide](../terraform/README.md).

## 9. CI/CD: Cloud function deployment based on GitHub push using cloud build (COMING SOON)

It's also possible to use CI/CD tools (like GCP Cloud Build, Jenkins, GitHub Actions, etc.) to automatically deploy resources based on various triggers like code changes. For using cloud build you should always have an own repository instead of using an existing repo which also includes other resources to prevent any possible conflicts. Therefore refer to the guide in this [repo](https://github.com/Daniel-Fauland/gcp-cloudbuild-guide).
