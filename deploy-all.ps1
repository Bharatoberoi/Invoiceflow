# InvoiceFlow - Automated GitHub & Cloud Run Deployment Script
# This script automates the entire deployment process

param(
    [string]$GitHubUsername,
    [string]$ProjectId,
    [string]$Region = "us-central1",
    [string]$ServiceName = "invoiceflow"
)

# Colors for output
$Green = [System.ConsoleColor]::Green
$Yellow = [System.ConsoleColor]::Yellow
$Cyan = [System.ConsoleColor]::Cyan
$Red = [System.ConsoleColor]::Red

function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════╗" -ForegroundColor $Cyan
    Write-Host "║ $Text" -ForegroundColor $Cyan
    Write-Host "╚═══════════════════════════════════════════════════════╝" -ForegroundColor $Cyan
    Write-Host ""
}

function Write-Success {
    param([string]$Text)
    Write-Host "✅ $Text" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Text)
    Write-Host "⚠️  $Text" -ForegroundColor $Yellow
}

function Write-Error {
    param([string]$Text)
    Write-Host "❌ $Text" -ForegroundColor $Red
}

function Test-Prerequisites {
    Write-Header "CHECKING PREREQUISITES"
    
    $all_good = $true
    
    # Check Git
    if (Get-Command git -ErrorAction SilentlyContinue) {
        Write-Success "Git is installed"
    } else {
        Write-Error "Git is not installed. Please install Git first."
        $all_good = $false
    }
    
    # Check gcloud
    if (Get-Command gcloud -ErrorAction SilentlyContinue) {
        Write-Success "Google Cloud SDK is installed"
    } else {
        Write-Error "Google Cloud SDK is not installed. Download from https://cloud.google.com/sdk/docs/install"
        $all_good = $false
    }
    
    # Check if in correct directory
    if (Test-Path "c:\Users\HP\OneDrive\Desktop\projects\Langraph_chatbot\server.py") {
        Write-Success "Project directory found"
    } else {
        Write-Error "Project directory not found"
        $all_good = $false
    }
    
    if (-not $all_good) {
        Write-Error "Prerequisites not met. Please install missing tools and try again."
        exit 1
    }
    
    Write-Success "All prerequisites met!"
}

function Get-UserInput {
    Write-Header "GATHERING INFORMATION"
    
    if (-not $GitHubUsername) {
        $GitHubUsername = Read-Host "Enter your GitHub username"
    }
    if (-not $ProjectId) {
        $ProjectId = Read-Host "Enter your Google Cloud Project ID"
    }
    
    Write-Host ""
    Write-Host "Configuration:" -ForegroundColor $Cyan
    Write-Host "  GitHub Username: $GitHubUsername"
    Write-Host "  Project ID: $ProjectId"
    Write-Host "  Service Name: $ServiceName"
    Write-Host "  Region: $Region"
    Write-Host ""
    
    $confirm = Read-Host "Is this correct? (y/n)"
    if ($confirm -ne "y") {
        Write-Error "Deployment cancelled"
        exit 1
    }
}

function Push-ToGitHub {
    Write-Header "PUSHING CODE TO GITHUB"
    
    try {
        Set-Location "c:\Users\HP\OneDrive\Desktop\projects\Langraph_chatbot"
        
        # Check if remote exists
        $existing_remote = git remote get-url origin 2>$null
        if ($existing_remote) {
            Write-Warning "Remote already exists: $existing_remote"
            Write-Warning "Removing existing remote..."
            git remote remove origin
        }
        
        $RepoUrl = "https://github.com/$GitHubUsername/invoiceflow.git"
        
        Write-Host "Adding remote: $RepoUrl"
        git remote add origin $RepoUrl
        
        Write-Host "Configuring branch..."
        git branch -M main
        
        Write-Host "Pushing to GitHub..."
        git push -u origin main
        
        Write-Success "Code pushed to GitHub successfully!"
        Write-Host "Repository URL: https://github.com/$GitHubUsername/invoiceflow" -ForegroundColor $Cyan
        
    } catch {
        Write-Error "Failed to push to GitHub: $_"
        exit 1
    }
}

function Deploy-ToCloudRun {
    Write-Header "DEPLOYING TO GOOGLE CLOUD RUN"
    
    try {
        Set-Location "c:\Users\HP\OneDrive\Desktop\projects\Langraph_chatbot"
        
        Write-Host "Setting Google Cloud project..."
        gcloud config set project $ProjectId
        
        Write-Host "Deploying to Cloud Run..."
        Write-Warning "This may take several minutes..."
        
        gcloud run deploy $ServiceName `
            --source . `
            --platform managed `
            --region $Region `
            --allow-unauthenticated `
            --memory 4Gi `
            --timeout 3600 `
            --set-env-vars PORT=8080
        
        Write-Success "Deployment completed!"
        
        # Get service URL
        $ServiceUrl = gcloud run services describe $ServiceName --region $Region --format 'value(status.url)'
        
        Write-Host ""
        Write-Header "DEPLOYMENT SUCCESSFUL!"
        Write-Host "Service Name: $ServiceName" -ForegroundColor $Cyan
        Write-Host "Service URL: $ServiceUrl" -ForegroundColor $Green
        Write-Host "Repository: https://github.com/$GitHubUsername/invoiceflow" -ForegroundColor $Cyan
        Write-Host "Region: $Region" -ForegroundColor $Cyan
        
    } catch {
        Write-Error "Deployment failed: $_"
        exit 1
    }
}

function Show-NextSteps {
    Write-Header "NEXT STEPS"
    
    $ServiceUrl = gcloud run services describe $ServiceName --region $Region --format 'value(status.url)' 2>$null
    
    Write-Host "1. Visit your app:" -ForegroundColor $Cyan
    Write-Host "   $ServiceUrl" -ForegroundColor $Green
    
    Write-Host ""
    Write-Host "2. View deployment logs:" -ForegroundColor $Cyan
    Write-Host "   gcloud run logs read $ServiceName --limit 50" -ForegroundColor $Green
    
    Write-Host ""
    Write-Host "3. Update after making changes:" -ForegroundColor $Cyan
    Write-Host "   git add ." -ForegroundColor $Green
    Write-Host "   git commit -m 'Your message'" -ForegroundColor $Green
    Write-Host "   git push" -ForegroundColor $Green
    Write-Host "   gcloud run deploy $ServiceName --source ." -ForegroundColor $Green
    
    Write-Host ""
    Write-Host "4. View Cloud Run console:" -ForegroundColor $Cyan
    Write-Host "   https://console.cloud.google.com/run" -ForegroundColor $Green
    
    Write-Host ""
}

# Main execution
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor $Green
Write-Host "║  🚀 InvoiceFlow - Automated Deployment Script             ║" -ForegroundColor $Green
Write-Host "║  GitHub + Google Cloud Run                                ║" -ForegroundColor $Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor $Green

# Execute deployment steps
Test-Prerequisites
Get-UserInput
Push-ToGitHub
Deploy-ToCloudRun
Show-NextSteps

Write-Header "DEPLOYMENT COMPLETE!"
Write-Success "Your InvoiceFlow application is now live! 🎉"
