# 🚀 Get Started - Speaker Prospect Filtering Tool

Welcome! This guide will help you get your Speaker Filtering Tool up and running in production.

## 📋 What You Have

You now have a **complete full-stack application** with:

✅ **FastAPI Backend** - REST API for speaker filtering  
✅ **React Frontend** - Beautiful Material-UI interface  
✅ **Docker Setup** - Containerized for easy deployment  
✅ **CI/CD Pipelines** - Automated GitHub Actions workflows  
✅ **GCP Configuration** - Ready for Cloud Run deployment  
✅ **Firebase Configuration** - Ready for Hosting deployment  
✅ **Complete Documentation** - Step-by-step guides  

## 🎯 Choose Your Path

### Path A: Quick Local Development (5 minutes)

Perfect for testing and development:

```bash
# 1. Set up backend
cd backend
cp .env.example .env
# Edit .env with your Airtable credentials
pip install -r requirements.txt
uvicorn api:app --reload

# 2. In new terminal, set up frontend
cd frontend
npm install
npm start

# Done! Backend at http://localhost:8000, Frontend at http://localhost:3000
```

### Path B: Docker Local Development (3 minutes)

Run everything with Docker:

```bash
# 1. Configure backend
cd backend
cp .env.example .env
# Edit .env with your Airtable credentials

# 2. Run everything
cd ..
docker-compose up --build

# Done! Backend at http://localhost:8000, Frontend at http://localhost:3000
```

### Path C: Full Production Deployment (30 minutes)

Deploy to GCP and Firebase with CI/CD:

**Follow these guides in order:**

1. **SETUP_GITHUB.md** (15 min)
   - Create GitHub repository
   - Configure GitHub Secrets
   - Set up GCP service account
   - Initialize Firebase project

2. **README_DEPLOYMENT.md** (15 min)
   - Deploy backend to Cloud Run
   - Deploy frontend to Firebase
   - Configure custom domains (optional)
   - Set up monitoring

## 📚 Documentation Guide

Your project includes comprehensive documentation:

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **GET_STARTED.md** (this file) | Quick start overview | Start here! |
| **README_GITHUB.md** | Main project README | Understanding the project |
| **SETUP_GITHUB.md** | GitHub & CI/CD setup | Setting up repository |
| **README_DEPLOYMENT.md** | Full deployment guide | Deploying to production |
| **QUICKSTART.md** | CLI tool quick start | Using CLI version |
| **README.md** | Original CLI documentation | CLI tool reference |

## 🔑 Required: Airtable Setup

Before anything else, you need Airtable credentials:

### Get Your Credentials

1. **API Key**
   - Go to: https://airtable.com/account
   - Scroll to "API" section
   - Click "Generate API key"
   - Copy the key (starts with "key...")

2. **Base ID**
   - Open your Airtable base in browser
   - URL looks like: `https://airtable.com/[BASE_ID]/...`
   - Copy the Base ID (starts with "app...")

3. **Table Name**
   - Exact name of your table
   - Example: "2511 Barclays status view"
   - Must match exactly (case-sensitive)

### Add to Configuration

**For local development:**
```bash
# backend/.env
AIRTABLE_API_KEY=keyXXXXXXXXXXXXXX
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX
AIRTABLE_TABLE_NAME=2511 Barclays status view
```

**For production (GitHub Secrets):**
- Add these as secrets in your GitHub repository
- See SETUP_GITHUB.md for detailed instructions

## 🎨 What the UI Looks Like

Your application has:

1. **Connection Test Section**
   - Real-time Airtable connectivity check
   - Shows record count and sample columns
   - Expandable for detailed information

2. **Filter Form**
   - Event name input (required)
   - Event title input (optional, for better analysis)
   - Beautiful gradient submit button

3. **Results Section**
   - Three tabs: Confirmed, Intended, Endorsed
   - Summary statistics with chips
   - Export buttons (CSV, JSON, TXT)

4. **Speaker Cards**
   - Compact view with key info
   - Expandable for full details
   - Shows ratings, notes, and analysis

## 🔧 Quick Troubleshooting

### "Connection Error" in UI
→ Check backend is running at correct URL  
→ Verify Airtable credentials in .env  

### "No speakers found"
→ Event name must match exactly (case-sensitive)  
→ Check Workshops column has correct tags  

### CI/CD failing
→ Verify all GitHub Secrets are set  
→ Check service account permissions  
→ Review GitHub Actions logs  

## 📞 Next Steps by Role

### For Developers
1. ✅ Test locally with Docker Compose
2. ✅ Review backend API at http://localhost:8000/docs
3. ✅ Explore frontend code in `frontend/src/`
4. ✅ Set up your preferred IDE

### For DevOps/Deployment
1. ✅ Follow SETUP_GITHUB.md
2. ✅ Configure all GitHub Secrets
3. ✅ Deploy to GCP and Firebase
4. ✅ Set up monitoring and alerts

### For End Users
1. ✅ Access deployed web application
2. ✅ Test Airtable connection
3. ✅ Filter speakers by event
4. ✅ Export results as needed

## 🎯 Quick Command Reference

```bash
# Local Development
docker-compose up --build              # Run full stack
cd backend && uvicorn api:app --reload # Backend only
cd frontend && npm start                # Frontend only

# Testing
curl http://localhost:8000/health      # Backend health
curl http://localhost:8000/api/test-connection  # Test Airtable

# Deployment
git push origin main                    # Trigger CI/CD
gcloud run services list                # View GCP services
firebase hosting:sites:list             # View Firebase sites
```

## 📊 Project Structure

```
speaker-filter/
├── 📁 backend/              # FastAPI backend
│   ├── api.py              # Main API
│   ├── Dockerfile          # Backend container
│   └── requirements.txt    # Python deps
│
├── 📁 frontend/            # React frontend
│   ├── src/
│   │   ├── App.js         # Main app
│   │   └── components/    # React components
│   ├── Dockerfile         # Frontend container
│   └── package.json       # Node deps
│
├── 📁 .github/workflows/  # CI/CD
│   ├── backend-deploy.yml
│   └── frontend-deploy.yml
│
├── docker-compose.yml     # Local dev
└── 📚 Documentation files
```

## ✅ Checklist

Before you start, make sure you have:

- [ ] Airtable account with API access
- [ ] Airtable credentials (API key, Base ID, Table name)
- [ ] Python 3.11+ (for local backend)
- [ ] Node.js 18+ (for local frontend)
- [ ] Docker & Docker Compose (optional, but recommended)
- [ ] Google Cloud account (for production)
- [ ] Firebase account (for production)
- [ ] GitHub account (for CI/CD)

## 🎉 Ready to Go!

Pick your path above and start building!

Need help? Check the relevant documentation:
- Local development issues → README.md
- Deployment issues → README_DEPLOYMENT.md
- GitHub setup → SETUP_GITHUB.md
- General questions → README_GITHUB.md

---

**Happy Filtering! 🎤**



