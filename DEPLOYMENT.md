# InvoiceFlow Deployment Guide

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Create a new repository with the following details:
   - **Repository name**: `invoiceflow`
   - **Description**: AI-Powered Orders & Invoices Assistant
   - **Visibility**: Public (or Private if preferred)
   - **Initialize**: Leave unchecked (we already have git)
3. Click **Create repository**

## Step 2: Push to GitHub

After creating the repository, you'll see push instructions. Run these commands in your terminal:

```bash
cd c:\Users\HP\OneDrive\Desktop\projects\Langraph_chatbot

# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/invoiceflow.git

# Rename branch to main if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 3: Deploy to Google Cloud Run

### Prerequisites
1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
2. Create a Google Cloud project
3. Enable the Cloud Run API

### Deployment Steps

1. **Authenticate with Google Cloud**:
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

2. **Build and deploy**:
```bash
cd c:\Users\HP\OneDrive\Desktop\projects\Langraph_chatbot

gcloud run deploy invoiceflow \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi \
  --timeout 3600 \
  --set-env-vars PORT=8080
```

### Deployment Options

**Recommended for production** (with authentication):
```bash
gcloud run deploy invoiceflow \
  --source . \
  --platform managed \
  --region us-central1 \
  --no-allow-unauthenticated \
  --memory 4Gi \
  --timeout 3600
```

**Alternative: Deploy from GitHub**:
```bash
gcloud run deploy invoiceflow \
  --source https://github.com/YOUR_USERNAME/invoiceflow.git \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi
```

## Important Notes for Cloud Run Deployment

### Model Loading
The Ollama model (llama3.2) is large (~5GB). For Cloud Run production:
- Consider using a smaller model or external LLM API
- Or pre-build a custom image with the model
- Or use a persistent GCS bucket for model caching

### Vector Database
The ChromaDB data needs to be persistent:
- Store it in Google Cloud Storage (GCS)
- Use Cloud Firestore
- Or re-index on startup (current implementation)

### Environment Variables
Set these in Cloud Run configuration if needed:
- `PORT`: Usually auto-set to 8080 (default in Cloud Run)
- `FLASK_ENV`: Set to 'production'

## Monitoring

View logs:
```bash
gcloud run logs read invoiceflow --limit 50
```

View service details:
```bash
gcloud run services describe invoiceflow
```

## Troubleshooting

1. **Build fails**: Check Docker configuration and Dockerfile
2. **Service timeout**: Increase timeout value or optimize model loading
3. **Memory issues**: Increase memory allocation (4Gi recommended)
4. **PDF not found**: Ensure invoices/ and orders/ directories are included

## Rollback
```bash
gcloud run services update-traffic invoiceflow --to-revisions REVISION_ID=100
```

## Cost Estimation (Approximate)

- **Cloud Run**: $0.00002400 per vCPU-second + $0.0000000417 per MB-second
- **Storage**: ~$0.020 per GB/month
- **Networking**: $0.12 per GB egress

## Next Steps

1. Monitor your deployment
2. Set up CI/CD with GitHub Actions
3. Implement proper error handling and logging
4. Add authentication/authorization
5. Optimize model for production

## Support

For issues or questions:
1. Check Cloud Run console for error logs
2. Review the README.md for architecture details
3. Check TESTING_GUIDE.md for sample queries
