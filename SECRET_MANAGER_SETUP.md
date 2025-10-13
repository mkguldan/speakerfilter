# 🔐 Google Secret Manager Setup Guide

You're using **Google Secret Manager** instead of storing secrets as environment variables - this is the **secure, production-grade approach**! ✅

## What's the Difference?

### ❌ GitHub Secrets → Environment Variables (Less Secure)
- Secrets stored in GitHub
- Injected as environment variables during deployment
- Visible in Cloud Run environment settings
- Anyone with Cloud Run access can see them

### ✅ Google Secret Manager (More Secure - What You're Using!)
- Secrets stored in Google Cloud Secret Manager
- Application fetches secrets at runtime
- Never visible as environment variables
- Proper access control with IAM

---

## 📋 What You Need in GitHub Secrets

Since you're using Google Secret Manager, you only need **5 GitHub Secrets** (not 8!):

### Go to: https://github.com/mkguldan/speakerfilter/settings/secrets/actions

Add only these:

1. **GCP_PROJECT_ID**
   - Value: `speakerfilter`
   - ✅ (Add this)

2. **GCP_SA_KEY**
   - Value: (JSON from service account)
   - ✅ (You already added this!)

3. **FIREBASE_PROJECT_ID**
   - Value: `speakerfilter-1a251`
   - ✅ (Add this)

4. **FIREBASE_SERVICE_ACCOUNT**
   - Value: (JSON from Firebase)
   - ✅ (You already added this!)

5. **BACKEND_URL**
   - Value: (Empty for now, add after first deployment)
   - ⏳ (Add later)

---

## 🔑 What Goes in Google Secret Manager

Your **Airtable credentials** go in Google Secret Manager:

1. **AIRTABLE_API_KEY**
   - Your PAT token (from Airtable account settings)

2. **AIRTABLE_BASE_ID**
   - Format: `appXXXXXXXXXXXXXX`
   - Get from Airtable URL

3. **AIRTABLE_TABLE_NAME**
   - Exact table name (case-sensitive)
   - Example: `2511 Barclays status view`

---

## 🚀 Setup Steps

### Step 1: Add GitHub Secrets (3 new ones)

Go to https://github.com/mkguldan/speakerfilter/settings/secrets/actions

Add:
- `GCP_PROJECT_ID` = `speakerfilter`
- `FIREBASE_PROJECT_ID` = `speakerfilter-1a251`
- (Skip `BACKEND_URL` for now)

You already have:
- ✅ `GCP_SA_KEY`
- ✅ `FIREBASE_SERVICE_ACCOUNT`

---

### Step 2: Create Google Secrets

Run the PowerShell script I created for you:

```powershell
# From your project directory
.\setup_secrets.ps1
```

This script will:
1. Enable Secret Manager API ✅ (Already done!)
2. Create the Airtable secrets in Google Secret Manager
3. Grant Cloud Run access to the secrets
4. Show you the Secret Manager console link

**When prompted:**
- Enter your Airtable Base ID (when you have it)
- Enter your Airtable Table Name (when you have it)

---

### Step 3: View Your Secrets

After running the script, view your secrets at:
https://console.cloud.google.com/security/secret-manager?project=speakerfilter

You should see:
- AIRTABLE_API_KEY ✅
- AIRTABLE_BASE_ID ✅
- AIRTABLE_TABLE_NAME ✅

---

### Step 4: Deploy to Production

```powershell
# Commit and push
git add .
git commit -m "Configure Google Secret Manager for secure credential storage"
git push origin main
```

This will trigger CI/CD and deploy with Secret Manager integration!

---

## 🔧 How It Works

### In Production (Cloud Run):
1. Your app starts on Cloud Run
2. `config.py` detects it's in Cloud Run (checks for `K_SERVICE` env var)
3. Uses `secret_manager.py` to fetch secrets from Google Secret Manager
4. Secrets are loaded securely at runtime
5. ✅ No secrets in environment variables!

### In Local Development:
1. Your app runs locally
2. `config.py` detects it's NOT in Cloud Run
3. Uses `.env` file for credentials
4. You can develop and test locally
5. ✅ Same code works everywhere!

---

## 📝 Local Development Setup

For local testing, you still use a `.env` file:

```bash
# backend/.env
AIRTABLE_API_KEY=your_personal_access_token_here
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX
AIRTABLE_TABLE_NAME=2511 Barclays status view
```

Then run:
```powershell
docker-compose up --build
```

---

## 🎯 Summary: What Goes Where

| Secret | GitHub Secrets | Google Secret Manager | .env (Local) |
|--------|---------------|----------------------|--------------|
| Airtable PAT | ❌ | ✅ | ✅ |
| Airtable Base ID | ❌ | ✅ | ✅ |
| Airtable Table Name | ❌ | ✅ | ✅ |
| GCP Project ID | ✅ | ❌ | ❌ |
| GCP Service Account | ✅ | ❌ | ❌ |
| Firebase Project ID | ✅ | ❌ | ❌ |
| Firebase Service Account | ✅ | ❌ | ❌ |
| Backend URL | ✅ | ❌ | ❌ |

---

## 🔍 Verify Secret Manager Setup

Check if secrets exist:

```powershell
# List all secrets
gcloud secrets list --project=speakerfilter

# View specific secret (metadata only, not the value)
gcloud secrets describe AIRTABLE_API_KEY --project=speakerfilter

# Test access (this will show the actual value - be careful!)
gcloud secrets versions access latest --secret="AIRTABLE_API_KEY" --project=speakerfilter
```

---

## 🆘 Troubleshooting

### "Permission denied" when accessing secrets

Grant Cloud Run access:
```powershell
$PROJECT_NUMBER = gcloud projects describe speakerfilter --format="value(projectNumber)"

gcloud secrets add-iam-policy-binding AIRTABLE_API_KEY `
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" `
    --role="roles/secretmanager.secretAccessor"
```

### "Secret not found"

Create the secret:
```powershell
echo "your-secret-value" | gcloud secrets create SECRET_NAME --data-file=-
```

### Backend can't fetch secrets

Check Cloud Run logs:
```powershell
gcloud run services logs read speaker-filter-backend --region us-central1 --limit 50
```

---

## ✅ Advantages of Your Setup

Using Google Secret Manager:
- ✅ **More Secure** - Secrets never visible as env vars
- ✅ **Audit Logging** - Track who accesses secrets
- ✅ **Automatic Rotation** - Can rotate secrets without redeploying
- ✅ **Fine-grained Access** - IAM controls who can access what
- ✅ **Versioning** - Keep history of secret changes
- ✅ **Best Practice** - Production-grade security

---

## 🎊 Next Steps

1. ✅ Add 3 remaining GitHub Secrets
2. ✅ Run `.\setup_secrets.ps1` to create Google secrets
3. ✅ Push code to GitHub
4. ✅ Watch deployment in GitHub Actions
5. ✅ Get backend URL and add to GitHub Secrets
6. ✅ Done! Your app is running securely!

---

**You're using the secure, production-grade approach! 🎉**



