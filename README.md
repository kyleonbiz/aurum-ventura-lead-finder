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

## Development Roadmap

- [ ] Phase 1: Backend API with business discovery
- [ ] Phase 2: Web frontend with search and export
- [ ] Phase 3: Desktop app packaging
- [ ] Phase 4: Advanced filtering and sorting
- [ ] Phase 5: User accounts and saved searches
- [ ] Phase 6: Performance optimization and scaling
