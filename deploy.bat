@echo off
REM InvoiceFlow Deployment Script for Google Cloud Run (Windows)

echo.
echo ======================================
echo 🚀 InvoiceFlow Cloud Run Deployment
echo ======================================
echo.

REM Check if gcloud is installed
where gcloud >nul 2>nul
if errorlevel 1 (
    echo ❌ Google Cloud SDK is not installed.
    echo Please install it from: https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

REM Get configuration from user
set /p github_username="Enter your GitHub username: "
set /p project_id="Enter your Google Cloud Project ID: "
set /p service_name="Enter desired Cloud Run service name (default: invoiceflow): "
if "%service_name%"=="" set service_name=invoiceflow

set /p region="Enter Cloud Run region (default: us-central1): "
if "%region%"=="" set region=us-central1

echo.
echo 📝 Configuration:
echo    GitHub Username: %github_username%
echo    Project ID: %project_id%
echo    Service Name: %service_name%
echo    Region: %region%
echo.

REM Authenticate with Google Cloud
echo 🔐 Authenticating with Google Cloud...
call gcloud auth login
call gcloud config set project %project_id%

REM Deploy to Cloud Run
echo.
echo 🐳 Building and deploying to Cloud Run...
echo.

call gcloud run deploy %service_name% ^
  --source . ^
  --platform managed ^
  --region %region% ^
  --allow-unauthenticated ^
  --memory 4Gi ^
  --timeout 3600 ^
  --set-env-vars PORT=8080

echo.
echo ✅ Deployment complete!
echo.
echo 📊 Service URL:
call gcloud run services describe %service_name% --region %region% --format "value(status.url)"
echo.
echo 📜 View logs:
echo    gcloud run logs read %service_name% --limit 50
echo.
echo 💡 Next steps:
echo    1. Visit the service URL above to access InvoiceFlow
echo    2. Monitor logs with: gcloud run logs read %service_name%
echo    3. Check DEPLOYMENT.md for more information
echo.
pause
