#!/bin/bash

# Speaker Filter Tool - Repository Initialization Script
# This script sets up your GitHub repository with all necessary files

set -e  # Exit on error

echo "=================================="
echo "Speaker Filter - Repository Setup"
echo "=================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: git is not installed"
    echo "Please install git first: https://git-scm.com/downloads"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "backend/api.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "Step 1: Initializing Git repository..."
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

echo ""
echo "Step 2: Adding all files..."
git add .

echo ""
echo "Step 3: Creating initial commit..."
if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "ℹ️  No changes to commit"
else
    git commit -m "Initial commit: Full-stack Speaker Filtering Tool with CI/CD

- FastAPI backend with Airtable integration
- React frontend with Material-UI
- Docker & Docker Compose setup
- GitHub Actions CI/CD pipelines
- GCP Cloud Run deployment config
- Firebase Hosting deployment config
- Comprehensive documentation"
    echo "✅ Initial commit created"
fi

echo ""
echo "Step 4: Setting default branch to 'main'..."
git branch -M main
echo "✅ Default branch set to main"

echo ""
echo "=================================="
echo "Repository initialized locally! ✅"
echo "=================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Create GitHub repository:"
echo "   - Go to https://github.com/new"
echo "   - Or use: gh repo create speaker-filter --private"
echo ""
echo "2. Add remote and push:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/speaker-filter.git"
echo "   git push -u origin main"
echo ""
echo "3. Configure GitHub Secrets (see SETUP_GITHUB.md):"
echo "   - GCP_PROJECT_ID"
echo "   - GCP_SA_KEY"
echo "   - FIREBASE_PROJECT_ID"
echo "   - FIREBASE_SERVICE_ACCOUNT"
echo "   - AIRTABLE_API_KEY"
echo "   - AIRTABLE_BASE_ID"
echo "   - AIRTABLE_TABLE_NAME"
echo "   - BACKEND_URL (after first deployment)"
echo ""
echo "4. Push to trigger CI/CD:"
echo "   git push origin main"
echo ""
echo "For detailed instructions, see:"
echo "- SETUP_GITHUB.md (GitHub setup)"
echo "- README_DEPLOYMENT.md (Deployment guide)"
echo "- README_GITHUB.md (Full documentation)"
echo ""
echo "=================================="



