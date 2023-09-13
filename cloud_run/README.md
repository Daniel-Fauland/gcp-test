# Cloud Run

This section will cover a few hands-on tutorials using cloud run.

## Getting started

Before deploying a web application on GCP you need a few things:

- Docker extension in VSC (optional)
- [Docker](https://www.docker.com) local install for building containers locally (optional)
- A web application (e.g. [this one](./code/main.py))

## Containerize your web application

Cloud run can either deploy an already built container or it can containerize your application for you. This sections shows you how you can containerize the web application yourself.

1. Create a _Dockerfile_ in the main project directory of the web application.

   ```shell
   FROM python:3.11
   ENV PYTHONUNBUFFERED True

   ENV APP_HOME /app
   WORKDIR $APP_HOME
   COPY . ./

   RUN pip install -r requirements.txt
   RUN pip install gunicorn

   CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
   ```

2. Create a _.dockerignore_ file and list all files that should not be included in the docker container (optional)

3. Build the docker image.

   <details>
   <summary>General code snippet:</summary>

   ```shell
   docker build -t <image-name> .
   ```

   </details>

   <details open>
   <summary>X86 platform:</summary>

   ```shell
   docker build -t my-flask-app .
   ```

   </details>

   <details open>
   <summary>ARM platform:</summary>

   ```shell
   docker build --platform linux/amd64 -t my-flask-app .
   ```

   </details>

4. Run the docker image locally.

   ```shell
   docker run -e PORT=80 -p 4000:80 my-flask-app
   ```

   **Note:** Dockerizing will not create any files in your directory. You can check the existing docker images with the following command.

   ```shell
   docker images
   ```

   You can also delete a docker images like this:

   ```shell
   docker rmi my-flask-app
   ```

5. Check your web application by opening the following address in the browser.
   ```shell
   http://localhost:4000
   ```

## Deploy docker image to cloud run using gcloud

Google Cloud Run requires that your Docker image is stored in _Artifact Registry_.

- Enable the Artifact Registry API.

  ```shell
  gcloud services enable artifactregistry.googleapis.com
  ```

- Configure Docker to use Artifact Registry as the Docker image repository.

  <details>
  <summary>Show general code snippet:</summary>

  ```shell
  gcloud auth configure-docker <your-region>-docker.pkg.dev
  ```

  </details>

  <details open>
  <summary>Show example code snippet:</summary>

  ```shell
  gcloud auth configure-docker europe-west3-docker.pkg.dev
  ```

  </details>

- Tag your Docker image with the Artifact Registry repository name.

  <details>
  <summary>Show general code snippet:</summary>

  ```shell
  docker tag <image-name> <your-region>-docker.pkg.dev/<project-id>/<artifact-registry-name>/<web-app-name>
  ```

  </details>

  <details open>
  <summary>Show example code snippet:</summary>

  ```shell
  docker tag my-flask-app europe-west3-docker.pkg.dev/propane-nomad-396712/cloud-run/my-flask-app
  ```

  </details>

- Create a new artifact registry. Or you can use the default one.

  <details>
  <summary>Show general code snippet:</summary>

  ```shell
  gcloud artifacts repositories create <repository-name> \
  --repository-format=docker \
  --location=<your-region>
  ```

  </details>

  <details open>
  <summary>Show example code snippet:</summary>

  ```shell
  gcloud artifacts repositories create cloud-run \
  --repository-format=docker \
  --location=europe-west3
  ```

  </details>

  **Note**: You can list your existing repositories with gcloud or by checking the _Artifact Registry_ in the UI.

  ```shell
  gcloud artifacts repositories list --location=europe-west3
  ```

- Push the tagged image to Artifact Registry.

  <details>
  <summary>Show general code snippet:</summary>

  ```shell
  docker tag <image-name> <your-region>-docker.pkg.dev/<project-id>/<artifact-registry-name>/<web-app-name>
  ```

  </details>

  <details open>
  <summary>Show example code snippet:</summary>

  ```shell
  docker push europe-west3-docker.pkg.dev/propane-nomad-396712/cloud-run/my-flask-app
  ```

  </details>

- Now, you can deploy your Flask application to Google Cloud Run using gcloud.

  <details>
  <summary>Show general code snippet:</summary>

  ```shell
  docker tag <image-name> <your-region>-docker.pkg.dev/<project-id>/<artifact-registry-name>/<web-app-name>
  ```

  </details>

  <details open>
  <summary>Show example code snippet:</summary>

  ```shell
  gcloud run deploy my-flask-app \
  --image europe-west3-docker.pkg.dev/propane-nomad-396712/cloud-run/my-flask-app \
  --platform managed \
  --allow-unauthenticated
  ```

  </details>

- Now your web application should be deployed and running. In order to retrieve its url aside from the terminal you deployed the web app you can use the following command.

  <details>
  <summary>Show general code snippet:</summary>

  ```shell
  gcloud run services describe <image-name> --platform managed --region <your-region> --format 'value(status.url)'
  ```

  </details>

  <details open>
  <summary>Show example code snippet:</summary>

  ```shell
  gcloud run services describe my-flask-app --platform managed --region europe-west3 --format 'value(status.url)'
  ```

  </details>
