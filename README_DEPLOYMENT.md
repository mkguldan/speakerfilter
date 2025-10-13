# Deployment Guide - Speaker Prospect Filtering Tool

This guide covers deploying the full-stack application with backend on GCP Cloud Run and frontend on Firebase Hosting, with automated CI/CD via GitHub Actions.

## Architecture Overview

- **Backend**: FastAPI application deployed on GCP Cloud Run
- **Frontend**: React application deployed on Firebase Hosting
- **CI/CD**: GitHub Actions for automated deployments
- **Database**: Airtable (external service)

---

## Prerequisites

### Required Accounts
1. **GitHub Account** - For code repository and CI/CD
2. **Google Cloud Platform Account** - For backend hosting
3. **Firebase Account** - For frontend hosting (uses same GCP project)
4. **Airtable Account** - For data storage

### Required Tools (for local development)
- Git
- Docker & Docker Compose
- Node.js 18+ and npm
- Python 3.11+
- gcloud CLI (Google Cloud SDK)
- Firebase CLI

---

## Part 1: Initial Setup

### 1.1 Create GitHub Repository

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: Speaker Filtering Tool with deployment config"

# Create repository on GitHub (via web or CLI)
# Then push your code
git remote add origin https://github.com/YOUR_USERNAME/speaker-filter.git
git branch -M main
git push -u origin main
```

### 1.2 Set Up Google Cloud Project

```bash
# Install gcloud CLI if not already installed
# Visit: https://cloud.google.com/sdk/docs/install

# Login to GCP
gcloud auth login

# Create new project
gcloud projects create speaker-filter-PROJECT_ID --name="Speaker Filter Tool"

# Set as default project
gcloud config set project speaker-filter-PROJECT_ID

# Enable required APIs
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    containerregistry.googleapis.com \
    secretmanager.googleapis.com

# Create service account for GitHub Actions
gcloud iam service-accounts create github-actions \
    --display-name="GitHub Actions Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding speaker-filter-PROJECT_ID \
    --member="serviceAccount:github-actions@speaker-filter-PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding speaker-filter-PROJECT_ID \
    --member="serviceAccount:github-actions@speaker-filter-PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding speaker-filter-PROJECT_ID \
    --member="serviceAccount:github-actions@speaker-filter-PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"

# Create and download service account key
gcloud iam service-accounts keys create github-actions-key.json \
    --iam-account=github-actions@speaker-filter-PROJECT_ID.iam.gserviceaccount.com

# Store the contents of this file - you'll need it for GitHub Secrets
```

### 1.3 Set Up Firebase

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase in your project
cd frontend
firebase init hosting

# Select your GCP project or create new one
# Choose 'build' as public directory
# Configure as single-page app: Yes
# Don't overwrite index.html

# Create service account for GitHub Actions
firebase projects:list
# Note your project ID

# Go to Firebase Console > Project Settings > Service Accounts
# Generate new private key and download JSON file
```

---

## Part 2: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

### Add the following secrets:

#### Backend (GCP) Secrets
- `GCP_PROJECT_ID`: Your GCP project ID
- `GCP_SA_KEY`: Contents of `github-actions-key.json`
- `AIRTABLE_API_KEY`: Your Airtable API key
- `AIRTABLE_BASE_ID`: Your Airtable base ID
- `AIRTABLE_TABLE_NAME`: Your Airtable table name

#### Frontend (Firebase) Secrets
- `FIREBASE_PROJECT_ID`: Your Firebase project ID
- `FIREBASE_SERVICE_ACCOUNT`: Contents of Firebase service account JSON
- `BACKEND_URL`: Will be set after first backend deployment (e.g., `https://speaker-filter-backend-xxx.run.app`)

---

## Part 3: Local Development & Testing

### 3.1 Backend Local Setup

```bash
# Navigate to backend directory
cd backend

# Create .env file
cp .env.example .env
# Edit .env with your Airtable credentials

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn api:app --reload --port 8000

# Test backend
curl http://localhost:8000/health
curl http://localhost:8000/api/test-connection
```

### 3.2 Frontend Local Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit to set REACT_APP_API_URL=http://localhost:8000

# Start development server
npm start

# App will open at http://localhost:3000
```

### 3.3 Docker Compose (Full Stack Local)

```bash
# From project root
# Make sure backend/.env exists with your Airtable credentials

# Build and run
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

---

## Part 4: Deploy to Production

### 4.1 Manual Backend Deployment (GCP Cloud Run)

```bash
cd backend

# Build and push image
gcloud builds submit --tag gcr.io/speaker-filter-PROJECT_ID/speaker-filter-backend

# Deploy to Cloud Run
gcloud run deploy speaker-filter-backend \
  --image gcr.io/speaker-filter-PROJECT_ID/speaker-filter-backend \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars AIRTABLE_API_KEY=your_key \
  --set-env-vars AIRTABLE_BASE_ID=your_base_id \
  --set-env-vars AIRTABLE_TABLE_NAME=your_table_name

# Get service URL
gcloud run services describe speaker-filter-backend \
  --region us-central1 \
  --format 'value(status.url)'
```

### 4.2 Manual Frontend Deployment (Firebase)

```bash
cd frontend

# Build with production API URL
REACT_APP_API_URL=https://your-backend-url.run.app npm run build

# Deploy to Firebase
firebase deploy --only hosting

# Get hosting URL
firebase hosting:sites:list
```

### 4.3 Automated Deployment (CI/CD)

Once GitHub Secrets are configured:

1. **Push to main branch** - triggers automatic deployment

```bash
git add .
git commit -m "Update application"
git push origin main
```

2. **Monitor deployments** in GitHub Actions tab

3. **Verify deployments**:
   - Backend: Check Cloud Run console
   - Frontend: Check Firebase Hosting console

---

## Part 5: Configuration & Management

### 5.1 Update Backend Environment Variables

```bash
# Update Cloud Run service
gcloud run services update speaker-filter-backend \
  --region us-central1 \
  --set-env-vars NEW_VAR=value
```

### 5.2 Update Frontend API URL

Update GitHub Secret `BACKEND_URL` and push to trigger redeployment.

### 5.3 View Logs

**Backend Logs:**
```bash
gcloud run services logs read speaker-filter-backend \
  --region us-central1 \
  --limit 50
```

**Frontend Logs:**
- Check Firebase Console → Hosting → Dashboard

### 5.4 Custom Domain Setup

**Backend (Cloud Run):**
```bash
gcloud run domain-mappings create \
  --service speaker-filter-backend \
  --domain api.yourdomain.com \
  --region us-central1
```

**Frontend (Firebase):**
```bash
firebase hosting:channel:deploy production \
  --project speaker-filter-PROJECT_ID

# Then add custom domain in Firebase Console
```

---

## Part 6: Monitoring & Maintenance

### 6.1 Set Up Monitoring

**Cloud Run Monitoring:**
- Go to Cloud Run console
- Select your service
- View Metrics, Logs, and Revisions

**Firebase Analytics:**
- Firebase Console → Analytics
- Set up custom events if needed

### 6.2 Cost Management

**Estimated Monthly Costs (Low Traffic):**
- Cloud Run: $0-5 (Free tier: 2M requests)
- Firebase Hosting: $0 (Free tier: 10GB storage, 360MB/day)
- Airtable: Depends on your plan

**Cost Optimization:**
- Set minimum instances to 0
- Configure appropriate memory/CPU limits
- Use Cloud Run request timeout

### 6.3 Security Best Practices

1. **Never commit secrets** - Always use environment variables
2. **Use Secret Manager** for sensitive data
3. **Enable CORS** properly in backend
4. **Set up authentication** if needed (Firebase Auth)
5. **Regular dependency updates**

---

## Part 7: Troubleshooting

### Common Issues

**Backend won't start:**
- Check environment variables are set
- Verify Airtable credentials
- Check Cloud Run logs

**Frontend can't connect to backend:**
- Verify CORS settings in backend
- Check REACT_APP_API_URL is correct
- Ensure backend allows unauthenticated requests

**CI/CD failing:**
- Verify all GitHub Secrets are set correctly
- Check service account permissions
- Review GitHub Actions logs

### Health Checks

```bash
# Backend health
curl https://your-backend-url.run.app/health

# Backend Airtable connection
curl https://your-backend-url.run.app/api/test-connection

# Frontend health (if custom domain)
curl https://your-frontend-url.web.app/health
```

---

## Quick Reference Commands

```bash
# Local Development
docker-compose up --build              # Run full stack locally
cd backend && uvicorn api:app --reload # Run backend only
cd frontend && npm start                # Run frontend only

# Deployment
git push origin main                    # Trigger CI/CD
gcloud run deploy speaker-filter-backend  # Manual backend deploy
firebase deploy --only hosting          # Manual frontend deploy

# Monitoring
gcloud run services logs read speaker-filter-backend --region us-central1
firebase hosting:sites:list

# Management
gcloud run services update speaker-filter-backend --set-env-vars KEY=value
firebase hosting:channel:list
```

---

## Support

For issues or questions:
1. Check logs in GCP Console and Firebase Console
2. Review GitHub Actions workflow runs
3. Verify all secrets and environment variables
4. Test Airtable connection with `/api/test-connection` endpoint

---

## Next Steps

After successful deployment:
1. Set up custom domains
2. Configure Firebase Analytics
3. Set up monitoring alerts
4. Implement authentication if needed
5. Add rate limiting
6. Set up backup procedures for Airtable data



