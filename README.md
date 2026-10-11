# Aurum Ventura Lead Finder

A simple, powerful desktop and web application for discovering local businesses by industry and location. Export clean, actionable lead lists to CSV or Excel.

## Features

- **Simple Inputs**: Select industry and location
- **Automated Discovery**: Find businesses without manual searching
- **Clean Export**: Download results as CSV or Excel
- **Cross-Platform**: Available as web app and desktop application
- **No Bloat**: No CRM, no email automation, just lead discovery

## Project Structure

```
aurum-ventura-lead-finder/
├── backend/              # Python Flask API
│   ├── app.py
│   ├── models.py
│   ├── routes/
│   ├── services/
│   └── requirements.txt
├── web/                  # React web frontend
│   ├── src/
│   ├── public/
│   └── package.json
├── desktop/              # Electron desktop app
│   ├── main.js
│   ├── preload.js
│   └── package.json
└── docs/                 # Documentation
```

## Getting Started

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Web Frontend Setup
```bash
cd web
npm install
npm start
```

### Desktop App Setup
```bash
cd desktop
npm install
npm start
```

## Technology Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Web Frontend**: React, TypeScript, Tailwind CSS
- **Desktop**: Electron, IPC for backend communication
- **Database**: SQLite (development), PostgreSQL (production)
- **Export**: CSV and XLSX generation

## How It Works

1. User selects industry and location
2. Backend searches business database
3. Results displayed in clean table format
4. User exports to CSV or Excel
5. File downloads to user's computer

## Data Sources

- Public business directories
- Government business registries
- Public APIs (respecting terms of service)

## License

Proprietary - Aurum Ventura

## Complete Features

### Backend API (Phase 1) ✅
- **Search Endpoints**:
  - Search businesses by industry, city, state
  - Get available industries list
  - Get city/state combinations
  - Database statistics
- **Export Endpoints**:
  - Export to CSV (standard format)
  - Export to Excel (formatted with headers)
  - Export to JSON (structured data)
- **Database**:
  - Business records with full contact info
  - Search history tracking
  - Export logging
  - Sample data with 18 businesses

### Web Frontend (Phase 2) ✅
- **User Interface**:
  - Beautiful gradient UI with purple/pink theme
  - Responsive design (mobile, tablet, desktop)
  - Industry/city/state selectors with dynamic loading
  - Real-time data from API
- **Search**:
  - Filter businesses by industry and location
  - Pagination support
  - Error handling and validation
- **Results Display**:
  - Clean table format with sorting
  - Clickable email and website links
  - Quality score badges
  - Copy-friendly business information
- **Export**:
  - One-click download as CSV
  - Excel export with formatting
  - JSON structured export
  - Download status tracking

### Desktop Application (Phase 3) ✅
- **Electron App**:
  - Native application for Windows, macOS, Linux
  - Secure context isolation
  - Development and production modes
  - Keyboard shortcuts and menu system
- **Packaging**:
  - Windows: NSIS installer + portable exe
  - macOS: DMG distribution
  - Linux: AppImage + DEB packages
  - Auto-updater ready
- **Security**:
  - Sandbox enabled
  - No node integration
  - Safe IPC communication
  - Preload script isolation

## Quick Start - All Platforms

### 1. Start Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python seed_data.py       # Load sample data
python app.py             # Start server on port 5000
```

### 2. Start Web Frontend
```bash
cd web
npm install
npm start                 # Opens http://localhost:3000
```

### 3. Start Desktop App
```bash
cd desktop
npm install
npm start                 # Launches desktop window
```

## Testing the Application

### Sample Data
The database includes 18 test businesses across 3 cities:
- **New York, NY**: Plumbing, Electrician services
- **Los Angeles, CA**: Plumbing, Electrician services
- **Chicago, IL**: Plumbing, Electrician services

### Test Search
1. Open web or desktop app
2. Select Industry: "plumbing" or "electrician"
3. Select City: "New York", "Los Angeles", or "Chicago"
4. Click "Search Businesses"
5. Click export button (CSV, Excel, or JSON)

## API Documentation

### Search API
```
GET /api/search/businesses?industry=plumbing&city=New York&state=NY
GET /api/search/industries
GET /api/search/locations?industry=plumbing
GET /api/search/stats
GET /health
```

### Export API
```
POST /api/export/csv
POST /api/export/excel
POST /api/export/json
```

Request body:
```json
{
  "industry": "plumbing",
  "city": "New York",
  "state": "NY"  // optional
}
```

## Architecture

```
┌─────────────┐
│  User Input │
└──────┬──────┘
       │
   ┌───▼────────────────────┐
   │   Frontend Layer       │
   ├───────────────────────┤
   │ ✓ React Web App       │
   │ ✓ Electron Desktop    │
   └────────┬──────────────┘
            │
      HTTP/REST API
            │
   ┌────────▼──────────────┐
   │   Backend Layer       │
   ├───────────────────────┤
   │ ✓ Flask API Server    │
   │ ✓ Search Engine       │
   │ ✓ Export Generator    │
   └────────┬──────────────┘
            │
     SQLite/PostgreSQL
            │
   ┌────────▼──────────────┐
   │   Data Layer          │
   ├───────────────────────┤
   │ ✓ Business Records    │
   │ ✓ Search History      │
   │ ✓ Export Logs         │
   └───────────────────────┘
```

## File Structure

```
.
├── backend/
│   ├── app.py                 # Flask application
│   ├── models.py              # SQLAlchemy models
│   ├── seed_data.py           # Sample data loader
│   ├── routes/
│   │   ├── search.py          # Search endpoints
│   │   └── export.py          # Export endpoints
│   ├── requirements.txt        # Python dependencies
│   └── .env.example           # Environment template
├── web/
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   ├── App.css            # Styles
│   │   └── index.js           # React entry point
│   ├── public/
│   │   ├── index.html         # HTML template
│   │   └── app.js             # Standalone JS version
│   └── package.json           # Node dependencies
├── desktop/
│   ├── main.js                # Electron main process
│   ├── preload.js             # Secure preload script
│   └── package.json           # Electron config
├── SETUP.md                   # Detailed setup guide
├── README.md                  # This file
└── .gitignore
```

## Development Roadmap

- [x] Phase 1: Backend API with business discovery
- [x] Phase 2: Web frontend with search and export
- [x] Phase 3: Desktop app packaging
- [ ] Phase 4: Advanced filtering and sorting
- [ ] Phase 5: User accounts and saved searches
- [ ] Phase 6: Performance optimization and scaling

## Production Deployment

### Backend
```bash
# Install production server
pip install gunicorn

# Run with production settings
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Web Frontend
```bash
# Build optimized bundle
npm run build

# Deploy web/build/ directory to hosting
```

### Desktop
```bash
# Build installers for all platforms
npm run dist

# Outputs to dist/ directory
```

## Troubleshooting

See [SETUP.md](SETUP.md) for detailed troubleshooting guide.

Common issues:
- Backend won't start: Check Python version and port 5000 availability
- Frontend won't connect: Ensure backend is running on port 5000
- Desktop won't launch: Build web app first, ensure backend is running
- Database errors: Delete aurum_ventures.db and run seed_data.py

## License

Proprietary - Aurum Ventura

## Support

For questions or issues:
1. Check the [SETUP.md](SETUP.md) documentation
2. Review API endpoint documentation above
3. Check application logs in console
4. Verify environment configuration
