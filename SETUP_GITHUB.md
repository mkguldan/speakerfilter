# GitHub Repository Setup Guide

Complete step-by-step instructions for creating your GitHub repository with CI/CD.

## Step 1: Create GitHub Repository

### Option A: Via GitHub Website

1. Go to https://github.com/new
2. Repository name: `speaker-filter` (or your preferred name)
3. Description: "Speaker Prospect Filtering Tool - Filter and organize speaker prospects from Airtable"
4. Visibility: Private (recommended) or Public
5. **Don't** initialize with README (we already have files)
6. Click "Create repository"

### Option B: Via GitHub CLI

```bash
# Install GitHub CLI: https://cli.github.com/

# Login
gh auth login

# Create repository
gh repo create speaker-filter --private --description "Speaker Prospect Filtering Tool"

# Or public
gh repo create speaker-filter --public --description "Speaker Prospect Filtering Tool"
```

## Step 2: Push Code to GitHub

```bash
# Navigate to your project directory
cd G:\IR\AI\speakerfilter

# Initialize git if not already done
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Full-stack speaker filtering tool with CI/CD"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/speaker-filter.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Configure GitHub Secrets

### Navigate to Secrets
1. Go to your repository on GitHub
2. Click "Settings" tab
3. In left sidebar, expand "Secrets and variables"
4. Click "Actions"
5. Click "New repository secret"

### Add Required Secrets

#### Backend Secrets (GCP Cloud Run)

**GCP_PROJECT_ID**
```
Value: your-gcp-project-id
Example: speaker-filter-prod
```

**GCP_SA_KEY**
```
Value: (entire contents of service account JSON key file)
Get from: Google Cloud Console > IAM & Admin > Service Accounts
```

**AIRTABLE_API_KEY**
```
Value: keyXXXXXXXXXXXXXX
Get from: https://airtable.com/account (generate API key)
```

**AIRTABLE_BASE_ID**
```
Value: appXXXXXXXXXXXXXX
Get from: Airtable URL - https://airtable.com/[BASE_ID]/...
```

**AIRTABLE_TABLE_NAME**
```
Value: 2511 Barclays status view
(exact name of your table, case-sensitive)
```

#### Frontend Secrets (Firebase)

**FIREBASE_PROJECT_ID**
```
Value: your-firebase-project-id
Example: speaker-filter-prod (same as GCP project usually)
```

**FIREBASE_SERVICE_ACCOUNT**
```
Value: (entire contents of Firebase service account JSON)
Get from: Firebase Console > Project Settings > Service Accounts > Generate new private key
```

**BACKEND_URL**
```
Value: https://speaker-filter-backend-xxx.run.app
Note: Leave empty initially, update after first backend deployment
```

## Step 4: Create GCP Service Account

### Via GCP Console

1. Go to https://console.cloud.google.com/
2. Select or create project
3. Navigate to "IAM & Admin" > "Service Accounts"
4. Click "Create Service Account"
5. Name: `github-actions`
6. Grant roles:
   - Cloud Run Admin
   - Storage Admin
   - Service Account User
7. Click "Done"
8. Click on the service account
9. Go to "Keys" tab
10. Click "Add Key" > "Create new key"
11. Choose JSON format
12. Download and save securely
13. Copy entire contents to `GCP_SA_KEY` secret

### Via gcloud CLI

```bash
# Create service account
gcloud iam service-accounts create github-actions \
    --display-name="GitHub Actions"

# Get your project ID
PROJECT_ID=$(gcloud config get-value project)

# Grant necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"

# Create key
gcloud iam service-accounts keys create github-actions-key.json \
    --iam-account=github-actions@${PROJECT_ID}.iam.gserviceaccount.com

# Display key (copy to GitHub secret)
cat github-actions-key.json
```

## Step 5: Set Up Firebase

### Create Firebase Project

1. Go to https://console.firebase.google.com/
2. Click "Add project"
3. Option 1: Select existing GCP project
4. Option 2: Create new project
5. Enable Google Analytics (optional)
6. Wait for project creation

### Get Firebase Service Account

1. In Firebase Console, click gear icon > "Project settings"
2. Go to "Service accounts" tab
3. Click "Generate new private key"
4. Confirm and download JSON file
5. Copy entire contents to `FIREBASE_SERVICE_ACCOUNT` secret

### Initialize Firebase in Project

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Navigate to frontend directory
cd frontend

# Initialize (if not done)
firebase init hosting

# Select your project
# Public directory: build
# Single-page app: Yes
# Automatic builds with GitHub: No (we use Actions)

# Update .firebaserc with your project ID
```

## Step 6: Enable GCP APIs

```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    containerregistry.googleapis.com \
    secretmanager.googleapis.com
```

## Step 7: Test CI/CD

### Trigger First Deployment

```bash
# Make a small change
echo "# Test" >> README.md

# Commit and push
git add .
git commit -m "Test CI/CD deployment"
git push origin main
```

### Monitor Deployment

1. Go to GitHub repository
2. Click "Actions" tab
3. Watch workflows run:
   - Deploy Backend to GCP Cloud Run
   - Deploy Frontend to Firebase

### Check Deployment Status

```bash
# Check backend deployment
gcloud run services describe speaker-filter-backend \
    --region us-central1 \
    --format 'value(status.url)'

# Check frontend deployment
firebase hosting:sites:list
```

## Step 8: Update Backend URL

After first backend deployment:

1. Get backend URL from Cloud Run console or terminal
2. Go to GitHub Secrets
3. Update or create `BACKEND_URL` secret
4. Push a change to trigger frontend redeployment

```bash
# Get backend URL
BACKEND_URL=$(gcloud run services describe speaker-filter-backend \
    --region us-central1 \
    --format 'value(status.url)')

echo "Backend URL: $BACKEND_URL"
# Copy this URL and add to BACKEND_URL secret
```

## Step 9: Verify Deployment

### Test Backend

```bash
# Health check
curl https://your-backend-url.run.app/health

# Test Airtable connection
curl https://your-backend-url.run.app/api/test-connection
```

### Test Frontend

1. Open Firebase Hosting URL in browser
2. Test connection should show "Connected"
3. Try filtering speakers

## Troubleshooting

### Workflow Fails: "Authentication failed"
- Check `GCP_SA_KEY` secret is correct
- Verify service account has necessary permissions
- Ensure APIs are enabled

### Backend: "Error fetching records"
- Check Airtable secrets are correct
- Verify API key has access to base
- Test with local backend first

### Frontend: "Network Error"
- Verify `BACKEND_URL` secret is set
- Check CORS settings in backend
- Ensure backend allows unauthenticated requests

### Permission Denied Errors
```bash
# Add Cloud Build service account as Run Admin
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/run.admin"
```

## Security Best Practices

1. **Never commit secrets** to repository
2. **Use environment variables** for all sensitive data
3. **Rotate keys regularly** (every 90 days)
4. **Use least privilege** for service accounts
5. **Enable branch protection** for main branch
6. **Require code reviews** before merging
7. **Set up secret scanning** in GitHub

## Next Steps

After successful setup:

1. ✅ Repository created and code pushed
2. ✅ GitHub Secrets configured
3. ✅ CI/CD workflows running
4. ✅ Backend deployed to Cloud Run
5. ✅ Frontend deployed to Firebase

Continue with:
- Set up custom domains
- Configure monitoring and alerts
- Add authentication
- Set up staging environment
- Configure backup procedures

---

## Quick Reference

### Repository URLs
- **GitHub**: `https://github.com/YOUR_USERNAME/speaker-filter`
- **Backend**: Check Cloud Run console for URL
- **Frontend**: Check Firebase Hosting console for URL

### Important Commands
```bash
# Deploy manually
git push origin main

# View logs
gcloud run services logs read speaker-filter-backend --region us-central1
firebase hosting:channel:deploy production

# Update secrets
gh secret set SECRET_NAME

# View deployments
gh run list
```

---

**Setup Complete!** 🎉

Your Speaker Filtering Tool is now deployed with automated CI/CD!



