# Speaker Filter Tool - Repository Initialization Script (PowerShell)
# This script sets up your GitHub repository with all necessary files

$ErrorActionPreference = "Stop"

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Speaker Filter - Repository Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    git --version | Out-Null
} catch {
    Write-Host "❌ Error: git is not installed" -ForegroundColor Red
    Write-Host "Please install git first: https://git-scm.com/downloads"
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "backend\api.py")) {
    Write-Host "❌ Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

Write-Host "Step 1: Initializing Git repository..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 2: Adding all files..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "Step 3: Creating initial commit..." -ForegroundColor Yellow
$status = git status --porcelain
if ($status) {
    git commit -m "Initial commit: Full-stack Speaker Filtering Tool with CI/CD

- FastAPI backend with Airtable integration
- React frontend with Material-UI
- Docker & Docker Compose setup
- GitHub Actions CI/CD pipelines
- GCP Cloud Run deployment config
- Firebase Hosting deployment config
- Comprehensive documentation"
    Write-Host "✅ Initial commit created" -ForegroundColor Green
} else {
    Write-Host "ℹ️  No changes to commit" -ForegroundColor Blue
}

Write-Host ""
Write-Host "Step 4: Setting default branch to 'main'..." -ForegroundColor Yellow
git branch -M main
Write-Host "✅ Default branch set to main" -ForegroundColor Green

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Repository initialized locally! ✅" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Create GitHub repository:" -ForegroundColor White
Write-Host "   - Go to https://github.com/new"
Write-Host "   - Or use: gh repo create speaker-filter --private"
Write-Host ""
Write-Host "2. Add remote and push:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/speaker-filter.git"
Write-Host "   git push -u origin main"
Write-Host ""
Write-Host "3. Configure GitHub Secrets (see SETUP_GITHUB.md):" -ForegroundColor White
Write-Host "   - GCP_PROJECT_ID"
Write-Host "   - GCP_SA_KEY"
Write-Host "   - FIREBASE_PROJECT_ID"
Write-Host "   - FIREBASE_SERVICE_ACCOUNT"
Write-Host "   - AIRTABLE_API_KEY"
Write-Host "   - AIRTABLE_BASE_ID"
Write-Host "   - AIRTABLE_TABLE_NAME"
Write-Host "   - BACKEND_URL (after first deployment)"
Write-Host ""
Write-Host "4. Push to trigger CI/CD:" -ForegroundColor White
Write-Host "   git push origin main"
Write-Host ""
Write-Host "For detailed instructions, see:" -ForegroundColor Yellow
Write-Host "- SETUP_GITHUB.md (GitHub setup)"
Write-Host "- README_DEPLOYMENT.md (Deployment guide)"
Write-Host "- README_GITHUB.md (Full documentation)"
Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan



