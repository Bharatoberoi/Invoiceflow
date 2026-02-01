# 🚀 InvoiceFlow - Quick Deployment Guide

## ⚡ Fastest Way to Deploy (5 Minutes)

### Step 1: Open PowerShell as Administrator

```powershell
# Go to project directory
cd c:\Users\HP\OneDrive\Desktop\projects\Langraph_chatbot

# Allow script execution (one time)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run the automated deployment script
.\deploy-all.ps1
```

The script will ask for:
- Your GitHub username
- Your Google Cloud Project ID

**That's it!** The script will handle everything.

---

## 📋 What the Script Does

1. ✅ Verifies prerequisites (Git, gcloud)
2. ✅ Creates GitHub remote
3. ✅ Pushes code to GitHub
4. ✅ Authenticates with Google Cloud
5. ✅ Deploys to Cloud Run
6. ✅ Returns your service URL

---

## 🔧 Manual Steps (If Script Doesn't Work)

```powershell
# Step 1: Get GitHub ready
$github_username = Read-Host "GitHub username"
$project_id = Read-Host "Google Cloud Project ID"

# Step 2: Navigate to project
cd c:\Users\HP\OneDrive\Desktop\projects\Langraph_chatbot

# Step 3: Push to GitHub
git remote add origin "https://github.com/$github_username/invoiceflow.git"
git branch -M main
git push -u origin main

# Step 4: Deploy to Cloud Run
gcloud config set project $project_id
gcloud run deploy invoiceflow --source . --platform managed --region us-central1 --allow-unauthenticated --memory 4Gi
```

---

## 🎯 What You Need Before Starting

- ✅ GitHub account (create at https://github.com if needed)
- ✅ Google Cloud account (create at https://cloud.google.com if needed)
- ✅ Google Cloud SDK installed
- ✅ Git installed
- ✅ PowerShell (Windows)

### Quick Check
```powershell
git --version
gcloud --version
```

If these show version numbers, you're ready!

---

## 📍 After Deployment

Your app will be at: `https://invoiceflow-XXXXX.a.run.app`

You can:
- Visit the URL in your browser
- Share it with others
- Update it by pushing new code to GitHub

---

## 🆘 Troubleshooting

### "GitHub authentication failed"
→ Use a Personal Access Token instead of password
→ Generate at: https://github.com/settings/tokens

### "Cloud Run deployment failed"
→ Check: `gcloud run logs read invoiceflow`
→ Make sure gcloud is authenticated: `gcloud auth login`

### "Script won't run"
→ Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
→ Then run script again

---

## 📞 Commands to Know

```powershell
# View your deployment
gcloud run services describe invoiceflow

# See logs
gcloud run logs read invoiceflow --limit 50

# Update after changes
git add .
git commit -m "Update message"
git push
gcloud run deploy invoiceflow --source .

# Delete deployment (if needed)
gcloud run services delete invoiceflow
```

---

## ✨ You're Ready!

### Option 1: Automated (Recommended)
```powershell
.\deploy-all.ps1
```

### Option 2: Manual
Follow the manual steps above

**Either way, your app will be live in minutes! 🎉**
