#!/bin/bash

# Define variables
IMAGE_NAME="safecitywalkdataservice"
CONTAINER_NAME="safecitywalkdataservice_container"
GOOGLE_CREDENTIALS_FILE="safecitydataservice.json"

# Build the Docker image
docker build -t $IMAGE_NAME .

# Run the Docker container
docker run -d \
  --name $CONTAINER_NAME \
  --env-file .env.docker \
  -v $(pwd)/$GOOGLE_CREDENTIALS_FILE:/app/google_credentials.json \
  -p 8000:80 \
  $IMAGE_NAME