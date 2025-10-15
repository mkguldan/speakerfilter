# Complete CI/CD Pipeline Setup via GitHub Actions

This guide will set up automatic deployment for both backend (Cloud Run) and frontend (Firebase) whenever you push to GitHub.

## 🎯 Current Status

- ✅ Backend workflow configured (`.github/workflows/backend-deploy.yml`)
- ✅ Frontend workflow configured (`.github/workflows/frontend-deploy.yml`)
- ✅ Backend currently deploying automatically
- ⏳ Frontend needs secrets configured

## 📋 Required GitHub Secrets

You need to configure these secrets in your GitHub repository.

### Go to GitHub Secrets
**https://github.com/mkguldan/speakerfilter/settings/secrets/actions**

---

## 🔑 Secrets to Add

### 1. GCP_PROJECT_ID ✅ (Should already exist)
```
speakerfilter
```

### 2. GCP_SA_KEY ✅ (Should already exist)
This is the service account JSON key you created earlier.

To verify it exists:
1. Go to GitHub Secrets page
2. Look for `GCP_SA_KEY`
3. If it exists, you're good! ✅

If it doesn't exist, create it:
```json
{
  "type": "service_account",
  "project_id": "speakerfilter",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "github-actions@speakerfilter.iam.gserviceaccount.com",
  ...
}
```

### 3. BACKEND_URL (Update or create this)
```
https://speaker-filter-backend-u7gfeexixa-uc.a.run.app
```

### 4. FIREBASE_PROJECT_ID (New secret)
```
speakerfilter
```

### 5. FIREBASE_SERVICE_ACCOUNT (New secret - Most Important!)

This requires generating a Firebase service account key.

#### How to Get Firebase Service Account:

**Step A: Enable Firebase on Your Project**

1. Go to: **https://console.firebase.google.com/**
2. Click "Add project"
3. Select **"Use an existing Google Cloud project"**
4. Choose: **speakerfilter**
5. Accept the terms
6. Enable Google Analytics (optional)
7. Click "Continue" and wait for Firebase to be added

**Step B: Generate Service Account Key**

1. In Firebase Console, click the gear icon ⚙️ next to "Project Overview"
2. Click **"Project settings"**
3. Go to the **"Service accounts"** tab
4. Click **"Generate new private key"**
5. Click **"Generate key"** (a JSON file will download)
6. Open the JSON file in a text editor
7. Copy **ALL** the contents (the entire JSON object)

**Step C: Add to GitHub Secrets**

1. Go to: https://github.com/mkguldan/speakerfilter/settings/secrets/actions
2. Click "New repository secret"
3. Name: `FIREBASE_SERVICE_ACCOUNT`
4. Value: Paste the entire JSON contents from the downloaded file
5. Click "Add secret"

The JSON should look like:
```json
{
  "type": "service_account",
  "project_id": "speakerfilter",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBA...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-xxxxx@speakerfilter.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

---

## 📝 Complete Secrets Checklist

Before proceeding, make sure ALL these secrets are configured:

- [ ] `GCP_PROJECT_ID` = `speakerfilter`
- [ ] `GCP_SA_KEY` = (GitHub Actions service account JSON)
- [ ] `BACKEND_URL` = `https://speaker-filter-backend-u7gfeexixa-uc.a.run.app`
- [ ] `FIREBASE_PROJECT_ID` = `speakerfilter`
- [ ] `FIREBASE_SERVICE_ACCOUNT` = (Firebase service account JSON)

---

## 🚀 Activate CI/CD Pipeline

Once all secrets are configured:

### Option 1: Push to GitHub (Automatic Trigger)

```powershell
git add frontend/.firebaserc
git commit -m "Configure Firebase project for CI/CD"
git push origin main
```

This will trigger:
1. ✅ Backend deployment (if backend files changed)
2. ✅ Frontend deployment (because frontend/.firebaserc changed)

### Option 2: Manual Trigger via GitHub UI

1. Go to: https://github.com/mkguldan/speakerfilter/actions
2. Click "Deploy Frontend to Firebase" workflow
3. Click "Run workflow" button
4. Select branch: `main`
5. Click "Run workflow"

---

## 📊 Monitor Deployments

### Backend Deployment
- URL: https://github.com/mkguldan/speakerfilter/actions/workflows/backend-deploy.yml
- Triggers: When files in `backend/` change
- Deploys to: Cloud Run
- Result: https://speaker-filter-backend-u7gfeexixa-uc.a.run.app

### Frontend Deployment
- URL: https://github.com/mkguldan/speakerfilter/actions/workflows/frontend-deploy.yml
- Triggers: When files in `frontend/` change
- Deploys to: Firebase Hosting
- Result: https://speakerfilter.web.app (or similar)

---

## 🎉 After First Successful Deployment

### Get Your Frontend URL

After the first successful frontend deployment:

1. Go to Firebase Console: https://console.firebase.google.com/project/speakerfilter/hosting
2. Look for "Domains" section
3. You'll see your public URL, typically: `https://speakerfilter.web.app`

Or via command line:
```powershell
firebase hosting:sites:list --project speakerfilter
```

### Test Your App

1. Open the Firebase Hosting URL in your browser
2. Upload your CSV file
3. Enter event name: `2511 Barclays`
4. Click "Filter Speakers"
5. You should see results! 🎉

---

## 🔄 How CI/CD Works

### Automatic Deployment Flow

```
┌─────────────────────────────────────────────────────┐
│  You make changes locally                           │
│  git add . && git commit -m "..." && git push       │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  GitHub detects changes                             │
└────────────────┬────────────────────────────────────┘
                 │
                 ├─────────────────┬──────────────────┐
                 ▼                 ▼                  ▼
         ┌───────────────┐ ┌──────────────┐ ┌────────────────┐
         │ Backend files │ │Frontend files│ │  Both changed  │
         │   changed?    │ │   changed?   │ │                │
         └───────┬───────┘ └──────┬───────┘ └───────┬────────┘
                 │                │                  │
                 ▼                ▼                  ▼
         ┌───────────────┐ ┌──────────────┐ ┌────────────────┐
         │ Build & Push  │ │ Build React  │ │  Deploy both   │
         │  Docker Image │ │     App      │ │  automatically │
         └───────┬───────┘ └──────┬───────┘ └───────┬────────┘
                 │                │                  │
                 ▼                ▼                  ▼
         ┌───────────────┐ ┌──────────────┐ ┌────────────────┐
         │ Deploy to     │ │ Deploy to    │ │   Done! ✅     │
         │  Cloud Run    │ │  Firebase    │ │                │
         └───────────────┘ └──────────────┘ └────────────────┘
```

### When Deployments Trigger

**Backend Deployment Triggers When:**
- Files in `backend/` directory change
- `.github/workflows/backend-deploy.yml` changes
- Manual trigger via GitHub UI

**Frontend Deployment Triggers When:**
- Files in `frontend/` directory change
- `.github/workflows/frontend-deploy.yml` changes
- Manual trigger via GitHub UI

### What Gets Built

**Backend:**
- Docker image with FastAPI app
- Pushed to Artifact Registry
- Deployed to Cloud Run
- ~2-3 minutes

**Frontend:**
- React app built with `npm run build`
- Environment variable `REACT_APP_API_URL` injected
- Static files deployed to Firebase Hosting
- ~3-4 minutes

---

## 🐛 Troubleshooting

### Frontend Deployment Fails: "Permission denied"

**Cause**: Firebase service account not configured or invalid

**Fix**:
1. Verify `FIREBASE_SERVICE_ACCOUNT` secret exists
2. Regenerate the Firebase service account key
3. Make sure you copied the ENTIRE JSON contents

### Frontend Deployment Fails: "Project not found"

**Cause**: Firebase not enabled on the project

**Fix**:
1. Go to https://console.firebase.google.com/
2. Add project and link to "speakerfilter"
3. Enable Firebase Hosting

### Backend Deployment Fails: "Permission denied"

**Cause**: GCP service account missing permissions

**Fix**: (Should already be done, but just in case)
```powershell
gcloud projects add-iam-policy-binding speakerfilter \
    --member="serviceAccount:github-actions@speakerfilter.iam.gserviceaccount.com" \
    --role="roles/run.admin"
```

### Environment Variable Not Working

**Cause**: `BACKEND_URL` secret not set or incorrect

**Fix**:
1. Go to GitHub Secrets
2. Update `BACKEND_URL` to: `https://speaker-filter-backend-u7gfeexixa-uc.a.run.app`
3. Re-run the workflow

### Workflow Doesn't Trigger

**Cause**: Changes not in the right directory

**Fix**: Make sure you're changing files in `frontend/` or `backend/` directories, not root files.

---

## 🎓 Best Practices

### 1. Test Locally First
Always test changes locally before pushing:
```powershell
# Backend
cd backend
python -m uvicorn api:app --reload

# Frontend
cd frontend
npm start
```

### 2. Use Feature Branches
For major changes, use branches:
```powershell
git checkout -b feature/my-new-feature
# Make changes...
git push origin feature/my-new-feature
# Create PR on GitHub
```

### 3. Monitor Deployments
After pushing, check:
- GitHub Actions: https://github.com/mkguldan/speakerfilter/actions
- Cloud Run logs: `gcloud run services logs read speaker-filter-backend --region us-central1`
- Firebase logs: https://console.firebase.google.com/project/speakerfilter/hosting

### 4. Rollback if Needed
If a deployment breaks something:

**Backend:**
```powershell
# List revisions
gcloud run revisions list --service speaker-filter-backend --region us-central1

# Rollback to previous revision
gcloud run services update-traffic speaker-filter-backend \
    --to-revisions REVISION_NAME=100 \
    --region us-central1
```

**Frontend:**
```powershell
# View deployment history
firebase hosting:releases:list --project speakerfilter

# Rollback to previous version (via Firebase Console)
# Go to: Hosting > Release history > "Roll back"
```

---

## 📈 What You Get

After setup:

✅ **Automatic Backend Deployments**
- Push code → Automatic build → Deploy to Cloud Run
- Zero manual steps

✅ **Automatic Frontend Deployments**
- Push code → Automatic build → Deploy to Firebase
- Zero manual steps

✅ **Environment Management**
- Backend URL automatically injected into frontend
- No manual environment file updates

✅ **Deployment History**
- Track all deployments in GitHub Actions
- See what was deployed when

✅ **Fast Iterations**
- Change code, push, wait 3-5 minutes, live!
- No manual deployment commands needed

---

## 🎯 Next Steps

1. ✅ Enable Firebase on your GCP project
2. ✅ Generate Firebase service account key
3. ✅ Add all GitHub secrets
4. ✅ Push to GitHub
5. ✅ Watch your app deploy automatically!
6. 🎉 Share your live URL with others!

---

## 🔗 Quick Links

- **GitHub Repository**: https://github.com/mkguldan/speakerfilter
- **GitHub Actions**: https://github.com/mkguldan/speakerfilter/actions
- **GitHub Secrets**: https://github.com/mkguldan/speakerfilter/settings/secrets/actions
- **Backend (Cloud Run)**: https://speaker-filter-backend-u7gfeexixa-uc.a.run.app
- **Frontend (Firebase)**: https://speakerfilter.web.app (after deployment)
- **Firebase Console**: https://console.firebase.google.com/project/speakerfilter
- **GCP Console**: https://console.cloud.google.com/run?project=speakerfilter

---

**Your CI/CD pipeline is ready to go!** Just add the Firebase secrets and push! 🚀

