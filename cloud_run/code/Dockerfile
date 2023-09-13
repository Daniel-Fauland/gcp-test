# Use an official Python runtime as a parent image
FROM python:3.11

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
# gunicorn is needed for docker
RUN pip install -r requirements.txt
RUN pip install gunicorn  

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
# main = your python file to start the web application
# app = the flask app instance
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
