#!/bin/bash

# Variables (update these as needed)
PROJECT_ID="safecitydataservice"   # Replace with your Google Cloud Project ID
REGION="us-west1"                  # Use a valid region for Cloud Run
SERVICE_NAME="safecitydataservice" # Name of the Cloud Run service
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME:latest"
ENVIRONMENT=${1:-prod}             # Default to 'prod' if not specified

# Log in to Docker (if necessary)
docker login

# Pull the base image manually to ensure it's available
docker pull python:3.12-slim

# Build and tag the Docker image
docker build -t "$IMAGE_NAME" .

# Push the image to Google Container Registry
docker push "$IMAGE_NAME"

# Deploy to Google Cloud Run
gcloud run deploy "$SERVICE_NAME" \
  --image "$IMAGE_NAME" \
  --platform managed \
  --region "$REGION" \
  --service-account "safecitydataservice-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --allow-unauthenticated \
  --env-vars-file="cloudrun.$ENVIRONMENT.yaml" \
  --set-secrets SOCRATA_APP_TOKEN=SOCRATA_APP_TOKEN:latest \
  --memory 512Mi

echo "Deployment to Google Cloud Run completed for service: $SERVICE_NAME with ENV=$ENVIRONMENT"
