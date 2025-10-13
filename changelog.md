# Changelog

All notable changes to the Speaker Prospect Filtering Tool will be documented in this file.

## [2.2.0] - 2025-10-03

### Changed - Pivot to CSV Upload (Remove Airtable Dependency)

#### Major Architecture Change
- **Removed Airtable integration** - No longer requires Airtable API/credentials
- **Added CSV file upload** - Upload speaker data directly via web interface
- **File size limit: 1GB** - Process large CSV files up to 1GB
- **Drag-and-drop UI** - Modern file upload interface

#### Backend Changes
- Updated `backend/api.py`:
  - Removed `AirtableFetcher` dependency
  - Added `pandas` for CSV processing
  - Created `/api/upload-csv` endpoint (preview CSV)
  - Created `/api/filter-speakers-csv` endpoint (filter from CSV)
  - Created `/api/export-csv/{format}` endpoint (export from CSV)
  - Added 1GB file size limit checks
  - Added CSV validation and error handling
- Removed `airtable_fetcher.py` dependency from API
- Removed Google Secret Manager integration (no longer needed)
- Updated `backend/config.py` - Reverted to simple env var config
- Updated `backend/Dockerfile` - Increased timeout for large file processing

#### Frontend Changes
- Created `frontend/src/components/FileUpload.js`:
  - Drag-and-drop file upload
  - File size validation (1GB limit)
  - File type validation (.csv only)
  - Visual upload feedback
  - File removal capability
- Updated `frontend/src/App.js`:
  - Added file upload state management
  - Updated filter logic to use uploaded CSV
  - Removed Airtable connection test
  - Added file requirement validation
- Updated `frontend/src/services/api.js`:
  - Changed from JSON requests to `multipart/form-data`
  - Added `uploadCSV()` method
  - Added `filterSpeakersCSV()` method
  - Added `exportSpeakersCSV()` method
- Updated `frontend/src/components/FilterForm.js`:
  - Added `disabled` prop when no file uploaded
  - Updated button text based on state

#### Documentation
- Created `CSV_UPLOAD_GUIDE.md` - Complete CSV upload guide:
  - Required CSV columns
  - How to export from Airtable/Excel/Google Sheets
  - Usage instructions
  - File size limits and performance tips
  - Example CSV format
  - Troubleshooting section
  - Privacy and security info

#### Benefits of CSV Approach
- ✅ **No Airtable setup** - Works immediately without API keys
- ✅ **Flexible data sources** - Accept CSV from anywhere
- ✅ **Offline capable** - No external API dependencies
- ✅ **Large files** - Process up to 1GB CSV files
- ✅ **Quick testing** - Upload and test immediately
- ✅ **Privacy** - Data processed in memory, not stored

#### Migration Notes
- Google Secret Manager configuration no longer needed for now
- Can still deploy without Airtable credentials
- CSV files can be exported from existing Airtable bases
- All existing filtering logic preserved and working

## [2.1.0] - 2025-10-03

### Added - Google Secret Manager Integration (Production Security)

#### Security Enhancement
- Created `backend/secret_manager.py` - Google Secret Manager client
- Updated `backend/config.py` to auto-detect Cloud Run and use Secret Manager
- Modified deployment workflow to remove environment variable injection
- Added `google-cloud-secret-manager` dependency to requirements.txt
- Created `setup_secrets.ps1` - PowerShell script for Secret Manager setup
- Added `SECRET_MANAGER_SETUP.md` - Comprehensive Secret Manager guide
- Implemented automatic fallback to .env for local development
- Configured IAM permissions for Cloud Run to access secrets

#### Benefits
- **Enhanced Security**: Secrets never stored as environment variables in Cloud Run
- **Audit Logging**: Track all secret access via Cloud Audit Logs
- **Version Control**: Secret Manager maintains version history
- **Access Control**: Fine-grained IAM permissions per secret
- **Auto-detection**: Same code works locally (`.env`) and in production (Secret Manager)
- **Zero Code Changes**: Application automatically detects environment

#### Configuration Changes
- Reduced GitHub Secrets requirement from 8 to 5:
  - Removed: AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME
  - These now stored in Google Secret Manager instead
  - Kept: GCP_PROJECT_ID, GCP_SA_KEY, FIREBASE_PROJECT_ID, FIREBASE_SERVICE_ACCOUNT, BACKEND_URL
- Updated backend deployment workflow to not inject Airtable env vars
- Cloud Run now fetches Airtable credentials from Secret Manager at runtime

### Notes
- Airtable API Key → Personal Access Token (PAT) support confirmed
- PAT format: `pat1XXXXXX.XXXXXXXXXXXX` works with existing code
- Local development still uses `.env` file (no changes needed)
- Production automatically uses Secret Manager (detected via K_SERVICE env var)

## [2.0.0] - 2025-10-03

### Added - Full-Stack Web Application with CI/CD

#### Backend API (FastAPI)
- Created `backend/api.py` with comprehensive REST API
- Implemented `/health` endpoint for health checks
- Added `/api/test-connection` for Airtable connectivity testing
- Built `/api/filter-speakers` POST endpoint for speaker filtering
- Created `/api/export/{format}` for CSV, JSON, and text exports
- Added CORS middleware for frontend communication
- Implemented proper error handling and HTTP status codes
- Added request/response Pydantic models for validation

#### Frontend Application (React)
- Built modern React 18 application with Material-UI
- Created `frontend/src/App.js` as main application component
- Implemented `Header.js` component with gradient design
- Built `FilterForm.js` for event input with validation
- Created `ConnectionTest.js` for real-time Airtable status
- Developed `Results.js` with tabbed interface for categories
- Built `SpeakerList.js` and `SpeakerCard.js` for speaker display
- Added expandable speaker cards with detailed information
- Implemented `api.js` service for backend communication
- Created beautiful gradient UI with purple theme
- Added export buttons for CSV, JSON, and TXT formats
- Implemented snackbar notifications for user feedback

#### Docker & Containerization
- Created `backend/Dockerfile` with multi-stage build
- Built `frontend/Dockerfile` with nginx for production
- Added `frontend/nginx.conf` for optimized serving
- Created `docker-compose.yml` for local development
- Added `.dockerignore` files for both frontend and backend
- Implemented health checks in Docker containers

#### CI/CD Pipelines (GitHub Actions)
- Created `.github/workflows/backend-deploy.yml`:
  - Automated backend deployment to GCP Cloud Run
  - Docker image building and pushing to GCR
  - Environment variable injection
  - Service URL extraction
- Built `.github/workflows/frontend-deploy.yml`:
  - Automated frontend deployment to Firebase Hosting
  - React build with production API URL
  - Firebase hosting integration

#### GCP Deployment Configuration
- Created `backend/cloudbuild.yaml` for Cloud Build
- Added `backend/app.yaml` for App Engine (alternative)
- Configured Cloud Run with auto-scaling
- Set up Container Registry integration
- Implemented secret management strategy

#### Firebase Deployment Configuration
- Created `frontend/firebase.json` for hosting config
- Added `frontend/.firebaserc` for project configuration
- Configured SPA routing and caching headers
- Set up production build optimization

#### Documentation
- Created `README_GITHUB.md` - Comprehensive GitHub repository README:
  - Feature overview with badges
  - Architecture diagram
  - Quick start guide
  - Usage instructions
  - API documentation
  - Deployment overview
  - Project structure
  - Development guide
  - Troubleshooting section
- Built `README_DEPLOYMENT.md` - Complete deployment guide:
  - Part 1: Initial setup (GCP, Firebase, GitHub)
  - Part 2: GitHub Secrets configuration
  - Part 3: Local development and testing
  - Part 4: Production deployment procedures
  - Part 5: Configuration management
  - Part 6: Monitoring and maintenance
  - Part 7: Troubleshooting common issues
  - Quick reference commands
- Created `SETUP_GITHUB.md` - Step-by-step GitHub setup:
  - Repository creation instructions
  - GitHub Secrets configuration
  - GCP service account setup
  - Firebase project initialization
  - CI/CD testing procedures
  - Security best practices
- Updated `.gitignore` for full-stack project

### Technical Architecture
- **Backend Stack**: Python 3.11, FastAPI, Uvicorn, PyAirtable, Pandas
- **Frontend Stack**: React 18, Material-UI, Axios, React Hooks
- **Infrastructure**: GCP Cloud Run, Firebase Hosting, Docker
- **CI/CD**: GitHub Actions with automated deployments
- **Monitoring**: Cloud Run metrics, Firebase Analytics ready

### Migration from CLI to Full-Stack
- Preserved all existing filtering logic from CLI version
- Maintained backward compatibility with CLI tool
- All Python modules copied to backend directory
- API wraps existing `airtable_fetcher`, `filters`, `text_extractor`, and `output_generator` modules
- Zero loss of functionality, all features available via web UI

### Security & Best Practices
- Environment variable management with `.env` files
- Service account authentication for GCP
- CORS configuration for secure frontend-backend communication
- Docker security with non-root users
- Secret injection in CI/CD pipelines
- Health check endpoints for monitoring

### Developer Experience
- Hot reload for both frontend and backend
- Docker Compose for one-command local development
- Comprehensive API documentation at `/docs` (Swagger UI)
- Clear error messages and status codes
- Structured logging for debugging

## [1.0.0] - 2025-10-03

### Added
- Initial release of Speaker Prospect Filtering Tool
- Created `config.py` for centralized configuration and Airtable credentials management
- Implemented `airtable_fetcher.py` module for fetching data from Airtable API
- Built `text_extractor.py` utilities for parsing call notes, comments, and ratings:
  - Extract "In sum" sections from call notes with date detection
  - Parse Jelena's comments with rating extraction
  - Extract abstract titles
  - Extract IR speaking engagement ratings
  - Generate content fit analysis based on abstract and event title
- Implemented `filters.py` with comprehensive filtering logic:
  - Filter confirmed speakers by event tag
  - Filter intended speakers with rating thresholds and exclusion rules
  - Filter endorsed speakers with same logic as intended
  - Rating filters: Axel's rating (≥92) or IR rating (≥3.8)
  - Automatic exclusion of "not reached", "not available", and "DON'T CONTACT" entries
  - Region-based filtering support
- Created `output_generator.py` for multiple output formats:
  - CSV export with all speaker details
  - JSON export with structured data and metadata
  - Human-readable text reports with formatted sections
- Built `main.py` CLI application with argument parsing:
  - Event name specification
  - Optional event title for content analysis
  - Output format selection (csv, json, text, all)
  - Custom output filename support
  - Progress tracking and summary statistics
- Added `requirements.txt` with all necessary dependencies:
  - pyairtable for Airtable API integration
  - pandas for data processing
  - python-dotenv for environment variable management
- Created comprehensive `README.md` with:
  - Installation instructions
  - Usage examples and CLI documentation
  - Detailed filtering logic explanation
  - Output format descriptions
  - Troubleshooting guide
  - Customization instructions

### Features
- Three-category speaker organization (Confirmed, Intended, Endorsed)
- Smart rating-based filtering with multiple thresholds
- Automated text extraction from unstructured notes
- Content fit analysis comparing speaker abstracts to event topics
- Multiple output formats for different use cases
- Configurable column mapping for Airtable customization
- Activity notes scanning for exclusion keywords
- Timestamp-based output file naming to prevent overwrites

### Technical Details
- Functional programming approach throughout
- Modular architecture with separated concerns
- Regex-based text parsing for robust extraction
- Environment variable configuration for security
- Error handling and user-friendly error messages
- Command-line interface with argparse

### Additional Files Created
- Created `.gitignore` to exclude sensitive files and outputs
- Added `setup_instructions.txt` with step-by-step setup guide
- Added `QUICKSTART.md` with 5-minute getting started guide
- Created `GET_STARTED.md` - Comprehensive quick start guide for choosing deployment path
- Built `PROJECT_SUMMARY.md` - Complete project overview with file structure and next steps
- Added `INITIALIZE_REPO.sh` - Bash script for Git repository initialization
- Created `INITIALIZE_REPO.ps1` - PowerShell script for Git repository initialization
- Included `test_connection.py` utility script for verifying Airtable setup:
  - Tests API connection
  - Displays available columns
  - Validates column mapping
  - Shows sample workshop tags
  - Provides troubleshooting guidance

