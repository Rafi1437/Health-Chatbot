# Senior Healthcare App - Streamlit Cloud Deployment Script (PowerShell)

Write-Host "🚀 Senior Healthcare App - Streamlit Cloud Deployment Script" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📝 Initializing Git repository..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit: Senior Healthcare App with Admin Portal"
}

# Check if remote is set
$remoteUrl = git remote get-url origin 2>$null
if (-not $remoteUrl) {
    Write-Host "⚠️  Please set up GitHub repository first:" -ForegroundColor Red
    Write-Host "   1. Go to https://github.com" -ForegroundColor White
    Write-Host "   2. Create new repository: senior-healthcare-app" -ForegroundColor White
    Write-Host "   3. Run: git remote add origin https://github.com/YOUR_USERNAME/senior-healthcare-app.git" -ForegroundColor White
    Write-Host "   4. Run this script again" -ForegroundColor White
    exit 1
}

Write-Host "📦 Verifying requirements.txt..." -ForegroundColor Cyan
if (-not (Test-Path "requirements.txt")) {
    Write-Host "❌ requirements.txt not found!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ requirements.txt found" -ForegroundColor Green

Write-Host "📝 Committing latest changes..." -ForegroundColor Yellow
git add .
git commit -m "Update for Streamlit Cloud deployment - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to push to GitHub. Please check your credentials." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🌐 Next Steps for Streamlit Cloud Deployment:" -ForegroundColor Cyan
Write-Host "1. Go to: https://share.streamlit.io/" -ForegroundColor White
Write-Host "2. Click 'Deploy an app'" -ForegroundColor White
Write-Host "3. Select your GitHub repository" -ForegroundColor White
Write-Host "4. Main file path: app.py" -ForegroundColor White
Write-Host "5. Click 'Deploy!'" -ForegroundColor White
Write-Host ""
Write-Host "📋 Deployment Configuration:" -ForegroundColor Yellow
Write-Host "- Repository: senior-healthcare-app" -ForegroundColor White
Write-Host "- Main file: app.py" -ForegroundColor White
Write-Host "- Python version: 3.9" -ForegroundColor White
Write-Host "- Public repository: Yes" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Optional: Add environment variables in Streamlit Cloud:" -ForegroundColor Yellow
Write-Host "- NLTK_DATA = /home/adminuser/.nltk" -ForegroundColor White
Write-Host ""
Write-Host "✅ Your app is ready for deployment!" -ForegroundColor Green
Write-Host "🎉 After deployment, your app will be available at:" -ForegroundColor Green
Write-Host "   https://your-username.streamlit.app/" -ForegroundColor White
