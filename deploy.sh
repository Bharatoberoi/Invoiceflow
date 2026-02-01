#!/bin/bash
# InvoiceFlow Deployment Script for Google Cloud Run

set -e

echo "🚀 InvoiceFlow Cloud Run Deployment Script"
echo "=========================================="
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK is not installed. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get configuration from user
read -p "Enter your GitHub username: " github_username
read -p "Enter your Google Cloud Project ID: " project_id
read -p "Enter desired Cloud Run service name (default: invoiceflow): " service_name
service_name=${service_name:-invoiceflow}
read -p "Enter Cloud Run region (default: us-central1): " region
region=${region:-us-central1}

echo ""
echo "📝 Configuration:"
echo "   GitHub Username: $github_username"
echo "   Project ID: $project_id"
echo "   Service Name: $service_name"
echo "   Region: $region"
echo ""

# Authenticate with Google Cloud
echo "🔐 Authenticating with Google Cloud..."
gcloud auth login
gcloud config set project $project_id

# Deploy to Cloud Run
echo ""
echo "🐳 Building and deploying to Cloud Run..."
echo ""

gcloud run deploy $service_name \
  --source . \
  --platform managed \
  --region $region \
  --allow-unauthenticated \
  --memory 4Gi \
  --timeout 3600 \
  --set-env-vars PORT=8080

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Service URL:"
gcloud run services describe $service_name --region $region --format 'value(status.url)'
echo ""
echo "📜 View logs:"
echo "   gcloud run logs read $service_name --limit 50"
echo ""
echo "💡 Next steps:"
echo "   1. Visit the service URL above to access InvoiceFlow"
echo "   2. Monitor logs with: gcloud run logs read $service_name"
echo "   3. Check DEPLOYMENT.md for more information"
echo ""
