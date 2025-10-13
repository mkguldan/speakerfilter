# PowerShell Script to Set Up Google Secret Manager
# Run this after you have your Airtable Base ID and Table Name

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Google Secret Manager Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if gcloud is installed
try {
    gcloud --version | Out-Null
} catch {
    Write-Host "❌ Error: gcloud CLI is not installed" -ForegroundColor Red
    exit 1
}

# Set project
Write-Host "Setting project to speakerfilter..." -ForegroundColor Yellow
gcloud config set project speakerfilter

# Enable Secret Manager API
Write-Host "Enabling Secret Manager API..." -ForegroundColor Yellow
gcloud services enable secretmanager.googleapis.com

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Creating Secrets" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# AIRTABLE_API_KEY
Write-Host "Creating AIRTABLE_API_KEY secret..." -ForegroundColor Yellow
Write-Host "Enter your Airtable Personal Access Token:" -ForegroundColor Cyan
$AIRTABLE_PAT = Read-Host
if ($AIRTABLE_PAT) {
    echo $AIRTABLE_PAT | gcloud secrets create AIRTABLE_API_KEY --data-file=-
    Write-Host "✅ AIRTABLE_API_KEY created" -ForegroundColor Green
} else {
    Write-Host "⚠️  Skipping AIRTABLE_API_KEY (you can add it later)" -ForegroundColor Yellow
}

# AIRTABLE_BASE_ID (you'll need to add this value)
Write-Host ""
Write-Host "Creating AIRTABLE_BASE_ID secret..." -ForegroundColor Yellow
$BASE_ID = Read-Host "Enter your Airtable Base ID (e.g., appXXXXXXXXXX)"
if ($BASE_ID) {
    echo $BASE_ID | gcloud secrets create AIRTABLE_BASE_ID --data-file=-
    Write-Host "✅ AIRTABLE_BASE_ID created" -ForegroundColor Green
} else {
    Write-Host "⚠️  Skipping AIRTABLE_BASE_ID (you can add it later)" -ForegroundColor Yellow
}

# AIRTABLE_TABLE_NAME
Write-Host ""
Write-Host "Creating AIRTABLE_TABLE_NAME secret..." -ForegroundColor Yellow
$TABLE_NAME = Read-Host "Enter your Airtable Table Name (e.g., '2511 Barclays status view')"
if ($TABLE_NAME) {
    echo $TABLE_NAME | gcloud secrets create AIRTABLE_TABLE_NAME --data-file=-
    Write-Host "✅ AIRTABLE_TABLE_NAME created" -ForegroundColor Green
} else {
    Write-Host "⚠️  Skipping AIRTABLE_TABLE_NAME (you can add it later)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Granting Access to Cloud Run" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Get project number
$PROJECT_NUMBER = gcloud projects describe speakerfilter --format="value(projectNumber)"
Write-Host "Project number: $PROJECT_NUMBER" -ForegroundColor Blue

# Grant Cloud Run service account access to secrets
Write-Host "Granting secret access to Cloud Run service account..." -ForegroundColor Yellow

gcloud secrets add-iam-policy-binding AIRTABLE_API_KEY `
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" `
    --role="roles/secretmanager.secretAccessor"

if ($BASE_ID) {
    gcloud secrets add-iam-policy-binding AIRTABLE_BASE_ID `
        --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" `
        --role="roles/secretmanager.secretAccessor"
}

if ($TABLE_NAME) {
    gcloud secrets add-iam-policy-binding AIRTABLE_TABLE_NAME `
        --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" `
        --role="roles/secretmanager.secretAccessor"
}

Write-Host "✅ Permissions granted" -ForegroundColor Green

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your secrets are now in Google Secret Manager:" -ForegroundColor Yellow
Write-Host "- AIRTABLE_API_KEY" -ForegroundColor White
if ($BASE_ID) { Write-Host "- AIRTABLE_BASE_ID" -ForegroundColor White }
if ($TABLE_NAME) { Write-Host "- AIRTABLE_TABLE_NAME" -ForegroundColor White }
Write-Host ""
Write-Host "View secrets at: https://console.cloud.google.com/security/secret-manager?project=speakerfilter" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. The backend code has been updated to use Secret Manager" -ForegroundColor White
Write-Host "2. Deploy your application with: git push origin main" -ForegroundColor White
Write-Host ""



