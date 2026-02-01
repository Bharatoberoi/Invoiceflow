# InvoiceFlow - Complete Deployment Instructions

## Prerequisites Checklist

Before starting, make sure you have:
- [ ] GitHub account (https://github.com)
- [ ] Google Cloud account (https://cloud.google.com)
- [ ] Google Cloud SDK installed (https://cloud.google.com/sdk/docs/install)
- [ ] Git installed on your computer

---

## PART 1: Create & Push to GitHub

### Step 1.1: Create New Repository on GitHub

1. Go to https://github.com/new
2. Fill in the form:
   - **Repository name**: `invoiceflow`
   - **Description**: `AI-Powered Orders & Invoices Assistant`
   - **Visibility**: Public
   - **Initialize**: Leave unchecked
3. Click **Create repository**
4. You'll see a page with your repository URL. Copy it.

### Step 1.2: Run These Commands in PowerShell

```powershell
cd c:\Users\HP\OneDrive\Desktop\projects\Langraph_chatbot

# Set your GitHub username (replace YOUR_USERNAME)
$github_username = "YOUR_USERNAME"
$repo_url = "https://github.com/$github_username/invoiceflow.git"

# Add the remote
git remote add origin $repo_url

# Rename branch to main if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

**Example:**
```powershell
cd c:\Users\HP\OneDrive\Desktop\projects\Langraph_chatbot
$github_username = "johnsmith"
$repo_url = "https://github.com/$github_username/invoiceflow.git"
git remote add origin $repo_url
git branch -M main
git push -u origin main
```

---

## PART 2: Deploy to Google Cloud Run

### Step 2.1: Authenticate with Google Cloud

```powershell
# Open browser to authenticate
gcloud auth login

# Set your project ID (replace YOUR_PROJECT_ID)
gcloud config set project YOUR_PROJECT_ID

# Verify setup
gcloud config list
```

### Step 2.2: Deploy to Cloud Run

```powershell
cd c:\Users\HP\OneDrive\Desktop\projects\Langraph_chatbot

# Option A: Deploy from Local Repository (Recommended for first time)
gcloud run deploy invoiceflow `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --memory 4Gi `
  --timeout 3600 `
  --service-account default

# After successful deployment, you can update from GitHub:
# Option B: Deploy from GitHub Repository
# gcloud run deploy invoiceflow `
#   --source https://github.com/YOUR_USERNAME/invoiceflow.git `
#   --platform managed `
#   --region us-central1 `
#   --allow-unauthenticated `
#   --memory 4Gi
```

### Step 2.3: Get Your Service URL

```powershell
# Display the service URL
gcloud run services describe invoiceflow --region us-central1 --format 'value(status.url)'

# View logs
gcloud run logs read invoiceflow --limit 50
```

---

## Quick Setup Script (Copy & Paste)

### For PowerShell Users

```powershell
# ============================================
# GITHUB SETUP
# ============================================

# Step 1: Set your credentials
$github_username = Read-Host "Enter your GitHub username"
$project_id = Read-Host "Enter your Google Cloud Project ID"

# Step 2: Navigate to project
cd c:\Users\HP\OneDrive\Desktop\projects\Langraph_chatbot

# Step 3: Add GitHub remote
$repo_url = "https://github.com/$github_username/invoiceflow.git"
git remote add origin $repo_url
git branch -M main

# Step 4: Push to GitHub
Write-Host "Pushing code to GitHub..." -ForegroundColor Green
git push -u origin main

Write-Host "✅ Code pushed successfully!" -ForegroundColor Green
Write-Host "Your repository: $repo_url" -ForegroundColor Cyan

# ============================================
# GOOGLE CLOUD SETUP
# ============================================

Write-Host "Setting up Google Cloud..." -ForegroundColor Green

# Step 5: Authenticate
Write-Host "Opening browser for authentication..." -ForegroundColor Yellow
gcloud auth login

# Step 6: Set project
gcloud config set project $project_id

# Step 7: Deploy to Cloud Run
Write-Host "Deploying to Cloud Run..." -ForegroundColor Green
gcloud run deploy invoiceflow `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --memory 4Gi `
  --timeout 3600

# Step 8: Get URL
Write-Host "Deployment complete! Getting your service URL..." -ForegroundColor Green
$service_url = gcloud run services describe invoiceflow --region us-central1 --format 'value(status.url)'

Write-Host "✅ Deployment successful!" -ForegroundColor Green
Write-Host "Visit your app at: $service_url" -ForegroundColor Cyan
Write-Host "GitHub repository: $repo_url" -ForegroundColor Cyan

# View logs
Write-Host "View logs with: gcloud run logs read invoiceflow --limit 50" -ForegroundColor Yellow
```

---

## Troubleshooting

### GitHub Push Issues

**Error: "fatal: remote origin already exists"**
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/invoiceflow.git
git push -u origin main
```

**Error: "Authentication failed"**
- Create a Personal Access Token on GitHub
- Use token instead of password when prompted

### Cloud Run Deployment Issues

**Error: "Project not found"**
```powershell
gcloud projects list  # Find your project ID
gcloud config set project YOUR_PROJECT_ID
```

**Error: "Build timeout"**
- Increase timeout or check internet connection
- Container image might be too large

**Error: "Resource quota exceeded"**
- Check your Cloud Run quotas
- May need to wait or upgrade billing

---

## Verification Steps

After deployment, verify everything works:

```powershell
# 1. Check Cloud Run service
gcloud run services list

# 2. Check service details
gcloud run services describe invoiceflow --region us-central1

# 3. Check logs for errors
gcloud run logs read invoiceflow --limit 20

# 4. Test health endpoint (replace URL with your service URL)
Invoke-WebRequest https://YOUR_SERVICE_URL/api/health

# 5. View git remote
git remote -v

# 6. Check git commits
git log --oneline
```

---

## Next Steps After Deployment

1. **Test your application**
   - Visit the Cloud Run URL
   - Test with sample queries
   - Check response times

2. **Set up monitoring**
   ```powershell
   gcloud monitoring alerts list
   ```

3. **Configure custom domain** (Optional)
   - Go to Cloud Run console
   - Manage Custom Domains
   - Map your domain

4. **Set up CI/CD** (Optional)
   - Use GitHub Actions for automatic deploys
   - Create `.github/workflows/deploy.yml`

5. **Scale and optimize**
   - Monitor Cloud Run metrics
   - Adjust memory and timeout as needed
   - Consider using Cloud Tasks for background jobs

---

## Support Resources

- Google Cloud Run: https://cloud.google.com/run/docs
- GitHub Docs: https://docs.github.com
- Cloud SDK: https://cloud.google.com/sdk/docs
- Troubleshooting: https://cloud.google.com/run/docs/troubleshooting

---

## One-Liner Summary

```powershell
# After setting $github_username and $project_id:
git remote add origin "https://github.com/$github_username/invoiceflow.git"; git branch -M main; git push -u origin main; gcloud config set project $project_id; gcloud run deploy invoiceflow --source . --platform managed --region us-central1 --allow-unauthenticated --memory 4Gi
```

---

**You're ready to deploy! 🚀**

Follow the steps above and your InvoiceFlow app will be live on Google Cloud Run!
