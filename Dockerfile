# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.7

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# Install production dependencies.
RUN pip install Flask
RUN pip install numpy
RUN pip install six
#RUN pip install scipy
RUN pip install markdown
RUN pip install geopy
#RUN pip install google-cloud-storage
RUN pip install gunicorn
RUN pip install utm
RUN pip install requests-toolbelt
RUN pip install numba
# RUN pip install --upgrade google-api-python-client
# RUN pip install --upgrade google-cloud-storage
# RUN gcloud components install app-engine-python-extras


# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app