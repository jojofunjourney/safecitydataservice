#!/bin/bash

# Configuration
PROJECT_ID="safecitydataservice"
SERVICE_NAME="stage-safecitydataservice"
REGION="us-west1"
REPO_NAME="repo-safecitydataservice"
IMAGE_NAME="image-safecitydataservice"
IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:latest"

# Environment Variables
ENV_VARS="ENVIRONMENT=prod,SOCRATA_APP_TOKEN=zgP7IfVHvCEOhh1CZCFMqQcjm,GCS_BUCKET_NAME=city-crime-data"

# Authenticate with Google Cloud
echo "Authenticating with Google Cloud..."
gcloud auth login
gcloud auth configure-docker ${REGION}-docker.pkg.dev
gcloud auth application-default set-quota-project $PROJECT_ID
gcloud config set project $PROJECT_ID

# Create Artifact Registry repository if it doesn't exist
echo "Creating Artifact Registry repository..."
gcloud artifacts repositories create $REPO_NAME --repository-format=docker --location=$REGION --description="Docker repository for SafeCityDataService" || true

# Build the container image locally
echo "Building the container image locally..."
docker build -t $IMAGE .

# Push the image to Artifact Registry
echo "Pushing the image to Artifact Registry..."
docker push $IMAGE

# Deploy the container to Cloud Run
echo "Deploying the container to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE \
    --platform managed \
    --region $REGION \
    --set-env-vars $ENV_VARS \
    --allow-unauthenticated \
    --port 8000

# Print the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')
echo "Service deployed to: $SERVICE_URL"

# Print recent logs
echo "Recent logs:"
gcloud run logs read --service $SERVICE_NAME --region $REGION --limit 50