# Deploy Frontend to Firebase Hosting

Your backend is live at: `https://speaker-filter-backend-u7gfeexixa-uc.a.run.app`

Now let's deploy the frontend so it's accessible from anywhere!

## Quick Start (Easiest Path)

### Step 1: Login to Firebase

```powershell
firebase login
```

This will open your browser. Login with your Google account.

### Step 2: Check Your Projects

```powershell
firebase projects:list
```

You should see your GCP project "speakerfilter" listed. If not, you'll need to enable Firebase.

### Step 3: Link to Your Project

If "speakerfilter" appears in the list:
```powershell
cd frontend
firebase use speakerfilter
```

If it doesn't appear, enable Firebase first (see "Enable Firebase" section below).

### Step 4: Build the Frontend

```powershell
# Set the backend URL for production
$env:REACT_APP_API_URL="https://speaker-filter-backend-u7gfeexixa-uc.a.run.app"

# Build
npm run build
```

### Step 5: Deploy to Firebase

```powershell
firebase deploy --only hosting
```

### Step 6: Access Your App! 🎉

Firebase will give you a URL like:
```
https://speakerfilter.web.app
```

Open it in your browser and use your app from anywhere!

---

## Enable Firebase (If Needed)

If your GCP project doesn't have Firebase enabled:

### Option A: Via Firebase Console (Easiest)

1. Go to: https://console.firebase.google.com/
2. Click "Add project"
3. Select "Use an existing Google Cloud project"
4. Choose: **speakerfilter**
5. Follow the wizard (enable Google Analytics if you want)
6. Click "Continue" and wait for setup
7. Go back to Step 3 above

### Option B: Via Command Line

```powershell
# Add Firebase to your GCP project
gcloud services enable firebase.googleapis.com --project=speakerfilter
```

Then go to Firebase Console to complete setup.

---

## Alternative: Deploy via GitHub Actions (Automated)

This sets up automatic deployment whenever you push code.

### Prerequisites

You need these GitHub secrets:
- `BACKEND_URL` ✅ (already have this)
- `FIREBASE_PROJECT_ID`
- `FIREBASE_SERVICE_ACCOUNT`

### Step 1: Get Firebase Service Account

1. Go to: https://console.firebase.google.com/
2. Select your project (speakerfilter)
3. Click the gear icon ⚙️ > Project Settings
4. Go to "Service accounts" tab
5. Click "Generate new private key"
6. Download the JSON file
7. Open it in a text editor and copy ALL the contents

### Step 2: Add GitHub Secrets

Go to: https://github.com/mkguldan/speakerfilter/settings/secrets/actions

Add these secrets:

**FIREBASE_PROJECT_ID**
```
speakerfilter
```

**FIREBASE_SERVICE_ACCOUNT**
```json
{
  "type": "service_account",
  "project_id": "speakerfilter",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  ...entire JSON content...
}
```

### Step 3: Update Firebase Config

Update `frontend/.firebaserc`:
```json
{
  "projects": {
    "default": "speakerfilter"
  }
}
```

### Step 4: Trigger Deployment

```powershell
git add frontend/.firebaserc
git commit -m "Configure Firebase project"
git push origin main
```

The GitHub Action will automatically:
1. Build the frontend with the backend URL
2. Deploy to Firebase Hosting
3. Give you the live URL

---

## Troubleshooting

### Error: "Project not found"

**Solution**: Enable Firebase on your GCP project first (see "Enable Firebase" section)

### Error: "Permission denied"

**Solution**: Make sure you're logged in:
```powershell
firebase login --reauth
```

### Error: "Site not found"

**Solution**: Initialize Firebase Hosting:
```powershell
cd frontend
firebase init hosting

# When asked:
# - Use existing project: speakerfilter
# - Public directory: build
# - Single-page app: Yes
# - Overwrite index.html: No
```

### Build Error: "REACT_APP_API_URL not found"

**Solution**: Set the environment variable before building:
```powershell
$env:REACT_APP_API_URL="https://speaker-filter-backend-u7gfeexixa-uc.a.run.app"
npm run build
```

---

## Comparison: Local vs Firebase

| Feature | Local (localhost:3000) | Firebase Hosting |
|---------|------------------------|------------------|
| **Access** | Only on your machine | Anywhere in the world |
| **URL** | http://localhost:3000 | https://speakerfilter.web.app |
| **Setup** | Already running ✅ | Need to deploy |
| **Speed** | Instant changes | Rebuild & redeploy |
| **Cost** | Free | Free (Spark plan) |
| **SSL** | No | Yes (automatic HTTPS) |
| **Sharing** | Cannot share | Anyone can access |

---

## Quick Deploy Commands (All-in-One)

If you just want to deploy quickly:

```powershell
# 1. Login to Firebase
firebase login

# 2. Go to frontend directory
cd frontend

# 3. Link to your project
firebase use speakerfilter

# 4. Build with backend URL
$env:REACT_APP_API_URL="https://speaker-filter-backend-u7gfeexixa-uc.a.run.app"
npm run build

# 5. Deploy!
firebase deploy --only hosting

# 6. Get your URL
firebase hosting:sites:list
```

---

## After Deployment

### View Your Live App

```powershell
# Get the hosting URL
firebase hosting:sites:list
```

Or go to: https://console.firebase.google.com/project/speakerfilter/hosting

### Update the App

To deploy changes:

```powershell
cd frontend

# Make your changes to the code...

# Rebuild
$env:REACT_APP_API_URL="https://speaker-filter-backend-u7gfeexixa-uc.a.run.app"
npm run build

# Deploy
firebase deploy --only hosting
```

### View Deployment History

```powershell
firebase hosting:channel:list
```

Or in Firebase Console: Hosting > Release history

---

## Your Current Status

- ✅ Backend deployed: https://speaker-filter-backend-u7gfeexixa-uc.a.run.app
- ✅ Frontend running locally: http://localhost:3000
- ⏳ Frontend on Firebase: Not deployed yet

Choose your path:
- **For testing**: Keep using localhost:3000 (it works!)
- **For production**: Follow the steps above to deploy to Firebase

---

## Need Help?

If you get stuck:
1. Check the error message
2. Look in the Troubleshooting section above
3. Check Firebase Console: https://console.firebase.google.com/
4. Check GitHub Actions logs (if using automated deployment)

**The easiest way**: Use the "Quick Deploy Commands" section above! 🚀

