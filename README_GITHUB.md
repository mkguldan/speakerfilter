# 🎤 Speaker Prospect Filtering Tool

A full-stack web application for filtering and organizing speaker prospects from Airtable. Automatically categorizes speakers into Confirmed, Intended, and Endorsed groups with intelligent rating-based filters and content fit analysis.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)

## ✨ Features

### 🎯 Smart Filtering
- **Three Categories**: Automatically organize speakers into Confirmed, Intended, and Endorsed
- **Rating-Based Logic**: Filters by Axel's rating (≥92) or IR Speaking Engagement (≥3.8)
- **Intelligent Exclusions**: Automatically excludes "not reached", "not available", and "DON'T CONTACT" entries
- **Region Support**: Optional region-based filtering

### 📊 Content Analysis
- **Call Notes Extraction**: Automatically extracts "In sum" sections and dates
- **Rating Aggregation**: Combines ratings from Axel, Jelena, and IR engagement
- **Content Fit Analysis**: AI-powered analysis comparing speaker abstracts to event topics
- **Abstract Processing**: Extracts and displays speaker abstracts and titles

### 💼 Professional UI
- **Modern Material Design**: Beautiful, responsive interface with Material-UI
- **Real-time Connection Test**: Verify Airtable connectivity before filtering
- **Expandable Speaker Cards**: Detailed information on demand
- **Multiple Export Formats**: Download results as CSV, JSON, or TXT

### 🚀 Deployment Ready
- **Backend**: FastAPI on GCP Cloud Run with auto-scaling
- **Frontend**: React on Firebase Hosting with global CDN
- **CI/CD**: Automated deployments via GitHub Actions
- **Docker Support**: Full Docker Compose setup for local development

---

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │         │                 │
│  React Frontend │◄───────►│  FastAPI Backend│◄───────►│    Airtable     │
│  (Firebase)     │   API   │  (Cloud Run)    │   API   │    Database     │
│                 │         │                 │         │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

### Tech Stack

**Backend:**
- Python 3.11
- FastAPI (REST API)
- PyAirtable (Airtable integration)
- Pandas (data processing)
- Uvicorn (ASGI server)

**Frontend:**
- React 18
- Material-UI (MUI)
- Axios (API client)
- React Hooks

**Infrastructure:**
- Google Cloud Run (Backend)
- Firebase Hosting (Frontend)
- GitHub Actions (CI/CD)
- Docker & Docker Compose

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)
- Airtable account with API access

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/speaker-filter.git
cd speaker-filter
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Airtable credentials

# Run backend
uvicorn api:app --reload --port 8000
```

Backend runs at: http://localhost:8000

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with backend URL (http://localhost:8000)

# Run frontend
npm start
```

Frontend runs at: http://localhost:3000

### 4. Docker Compose (Alternative)

```bash
# From project root
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

---

## 📖 Usage

### Web Interface

1. **Test Connection**: Verify Airtable connection status
2. **Enter Event Details**:
   - Event Name (required): e.g., "2511 Barclays"
   - Event Title (optional): e.g., "Digital Transformation in Finance"
3. **Filter Speakers**: Click "Filter Speakers" button
4. **Review Results**: Browse categorized speakers in tabs
5. **Export Data**: Download as CSV, JSON, or TXT

### API Endpoints

```bash
# Health check
GET /health

# Test Airtable connection
GET /api/test-connection

# Filter speakers
POST /api/filter-speakers
{
  "event_name": "2511 Barclays",
  "event_title": "Optional Event Title"
}

# Export data
GET /api/export/{format}?event_name=2511%20Barclays
```

Full API documentation: http://localhost:8000/docs

---

## 🔍 How It Works

### Filtering Logic

#### Confirmed Speakers
- Contains tag: `[Event Name] Confirmed`
- All confirmed speakers included automatically

#### Intended Speakers
- Contains tag: `[Event Name] Intended`
- **Excludes:**
  - `[Event Name] not reached`
  - `[Event Name] not available`
  - Activity notes with "DON'T CONTACT"
- **Includes if:**
  - Axel's rating ≥ 94 → "Good option"
  - Axel's rating 92-93 → "Lower rating"
  - IR Speaking Engagement ≥ 3.8 (regardless of Axel's rating)

#### Endorsed Speakers
- Contains tag: `[Event Name] Endorsed`
- Same filtering rules as Intended Speakers

### Data Extraction

The tool automatically extracts:
- **Call Notes**: "In sum" sections and dates
- **Jelena's Comments**: Ratings and first two lines
- **Abstract**: Titles and content
- **Ratings**: Axel, Jelena, and IR engagement scores
- **Content Fit**: AI-generated analysis of speaker-event alignment

---

## 🌐 Deployment

### Deploy to Production

Comprehensive deployment guide: [README_DEPLOYMENT.md](./README_DEPLOYMENT.md)

**Quick Deploy:**

1. **Create GCP Project**
2. **Create Firebase Project**
3. **Configure GitHub Secrets**
4. **Push to main branch**

Automated CI/CD handles the rest!

### Required GitHub Secrets

- `GCP_PROJECT_ID`
- `GCP_SA_KEY`
- `FIREBASE_PROJECT_ID`
- `FIREBASE_SERVICE_ACCOUNT`
- `AIRTABLE_API_KEY`
- `AIRTABLE_BASE_ID`
- `AIRTABLE_TABLE_NAME`
- `BACKEND_URL`

---

## 📁 Project Structure

```
speaker-filter/
├── backend/                # FastAPI backend
│   ├── api.py             # Main API application
│   ├── airtable_fetcher.py # Airtable integration
│   ├── filters.py         # Filtering logic
│   ├── text_extractor.py  # Text parsing utilities
│   ├── output_generator.py # Export functionality
│   ├── config.py          # Configuration
│   ├── Dockerfile         # Backend container
│   └── requirements.txt   # Python dependencies
│
├── frontend/              # React frontend
│   ├── public/           # Static assets
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API service
│   │   ├── App.js       # Main app component
│   │   └── index.js     # Entry point
│   ├── Dockerfile       # Frontend container
│   ├── firebase.json    # Firebase config
│   └── package.json     # Node dependencies
│
├── .github/
│   └── workflows/       # CI/CD pipelines
│       ├── backend-deploy.yml
│       └── frontend-deploy.yml
│
├── docker-compose.yml   # Local development
├── README.md           # This file
└── README_DEPLOYMENT.md # Deployment guide
```

---

## 🛠️ Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
flake8 .
black .

# Frontend linting
cd frontend
npm run lint
```

### Environment Variables

**Backend (.env):**
```env
AIRTABLE_API_KEY=your_api_key
AIRTABLE_BASE_ID=your_base_id
AIRTABLE_TABLE_NAME=your_table_name
```

**Frontend (.env):**
```env
REACT_APP_API_URL=http://localhost:8000
```

---

## 📊 Airtable Requirements

### Required Columns

Your Airtable table must have these columns:

- `Name` - Speaker name
- `Workshops` - Event tags
- `Axel's rating` - Numeric rating
- `Notes speaker calls` - Call notes with "In sum" sections
- `Jelena's comments` - Comments with ratings
- `Region` - Geographic region
- `Abstract` - Speaker abstract
- `Company` - Speaker's company
- `IR Speaking engagement` - IR ratings
- `Activity notes` - Activity log

Column names can be customized in `backend/config.py`.

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License.

---

## 🆘 Support

### Common Issues

**Connection Error:**
- Verify Airtable credentials
- Check API key permissions
- Ensure base ID is correct

**No Speakers Found:**
- Verify event name matches exactly (case-sensitive)
- Check Workshop column tags
- Review filtering logic

**Deployment Failed:**
- Check GitHub Secrets configuration
- Verify GCP/Firebase permissions
- Review CI/CD logs

### Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Material-UI Documentation](https://mui.com/)
- [Airtable API](https://airtable.com/developers/web/api/introduction)
- [GCP Cloud Run](https://cloud.google.com/run/docs)
- [Firebase Hosting](https://firebase.google.com/docs/hosting)

---

## 🎯 Roadmap

- [ ] Add user authentication (Firebase Auth)
- [ ] Implement speaker search and filtering
- [ ] Add email notification system
- [ ] Create speaker comparison view
- [ ] Add analytics dashboard
- [ ] Implement caching for better performance
- [ ] Add bulk operations support
- [ ] Create mobile app version

---

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for event organizers**



