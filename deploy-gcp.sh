#!/bin/bash
# Deploy to Google Cloud Run - Production Deployment Script

echo "🚀 Deploying Vira Assistant to Google Cloud Run..."

# Configuration
PROJECT_ID=$(gcloud config get-value project)
SERVICE_NAME="vira-assistant"
REGION="us-central1"

# Check if gcloud CLI is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI not found. Please install it first."
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build Docker image
echo "🏗️  Building Docker image..."
gcloud builds submit \
    --tag gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --region $REGION \
    --timeout=600 \
    --machine-type=e2-highmem-2 \
    .

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --memory=512Mi \
    --cpu=1 \
    --port=5000 \
    --min-instances=0 \
    --max-instances=10 \
    --set-env-vars="FLASK_ENV=production" \
    --quiet

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
    --region $REGION \
    --format="value(status.url)")

echo "✅ Deployment complete!"
echo "🌐 Your Vira Assistant is available at: $SERVICE_URL"
echo "📊 Monitor your deployment at: https://console.cloud.google.com/run"

# Set up monitoring
echo "📈 Setting up monitoring..."
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME" \
    --limit=5 \
    --format="table(timestamp,textPayload)" \
    --region=$REGION

echo "🔗 Quick links:"
echo "   - Service URL: $SERVICE_URL"
echo "   - Cloud Console: https://console.cloud.google.com/run"
echo "   - Logs: https://console.cloud.google.com/logs"
