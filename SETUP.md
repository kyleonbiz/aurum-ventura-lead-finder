# Aurum Ventura Lead Finder - Setup Guide

Complete setup instructions for running the backend, web frontend, and desktop application.

## Prerequisites

- Python 3.8+
- Node.js 16+ and npm
- Git

## Project Structure

```
aurum-ventura-lead-finder/
├── backend/           # Flask API
├── web/              # React web app
├── desktop/          # Electron desktop app
└── docs/             # Documentation
```

## Quick Start (All Components)

### 1. Backend Setup

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Seed sample data
python seed_data.py
# Output: ✓ Seeded 18 businesses

# Start server
python app.py
# Server running at http://localhost:5000
```

### 2. Web Frontend Setup

```bash
cd web
npm install
npm start
# Opens http://localhost:3000 in browser
```

### 3. Desktop App Setup

```bash
cd desktop
npm install
npm start
# Launches Electron window
```

## Running Each Component Separately

### Backend Only
```bash
cd backend
source venv/bin/activate  # or: venv\Scripts\activate (Windows)
python app.py
```
- API available at `http://localhost:5000`
- Health check: `GET http://localhost:5000/health`

### Web Frontend Only
```bash
cd web
npm start
```
- Opens at `http://localhost:3000`
- Requires backend running on `http://localhost:5000`

### Desktop App Only
```bash
cd desktop
npm install
npm start
```
- Launches native application window
- Requires backend running
- Requires React build (run `npm run build` in web/)

## API Endpoints

### Search API
- `GET /api/search/businesses?industry=<industry>&city=<city>&state=<state>`
- `GET /api/search/industries`
- `GET /api/search/locations?industry=<industry>`
- `GET /api/search/stats`

### Export API
- `POST /api/export/csv` - Export as CSV
- `POST /api/export/excel` - Export as Excel
- `POST /api/export/json` - Export as JSON

### Health Check
- `GET /health` - Service status

## Database

The application uses SQLite by default (development).

### Initialize Database
```bash
cd backend
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### Seed Sample Data
```bash
cd backend
python seed_data.py
```

### Reset Database
```bash
cd backend
rm aurum_ventures.db  # Delete the database file
python seed_data.py   # Reseed with sample data
```

## Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///aurum_ventures.db
PORT=5000
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
LOG_LEVEL=INFO
```

### Web Frontend

Create a `.env` file in the `web/` directory:

```
REACT_APP_API_URL=http://localhost:5000/api
```

## Development

### Backend Development
- API changes: Restart Flask server
- Database changes: Update `models.py`, recreate database
- New routes: Create in `routes/` directory, register in `app.py`

### Frontend Development
- Component changes: Hot reload (React dev server)
- Styling: Tailwind CSS (already configured)
- API calls: Update `src/App.js`

### Desktop Development
- UI changes: Edit React code, rebuild web app
- Electron changes: Restart electron (`npm start`)
- Packaging: Run `npm run dist`

## Building for Production

### Backend
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Web Frontend
```bash
cd web
npm run build
# Outputs to web/build/ directory
```

### Desktop Application
```bash
cd desktop
npm run dist
# Creates installer in dist/ directory
# Windows: .exe and portable .zip
# macOS: .dmg
# Linux: .AppImage and .deb
```

## Troubleshooting

### Backend won't start
- Check Python version: `python --version`
- Check if port 5000 is in use: `lsof -i :5000`
- Verify all dependencies installed: `pip list`

### Web app won't connect to backend
- Ensure backend is running: `curl http://localhost:5000/health`
- Check CORS configuration in `backend/app.py`
- Check browser console for errors (F12)

### Desktop app won't launch
- Ensure web app is built: `cd web && npm run build`
- Check backend is running
- Check Electron console for errors: `npm start` (dev mode shows console)

### Database errors
- Delete database: `rm backend/aurum_ventures.db`
- Reinitialize: `cd backend && python seed_data.py`

## Sample Data

The database includes 18 sample businesses:
- **New York**: 7 businesses (Plumbing, Electrician)
- **Los Angeles**: 5 businesses (Plumbing, Electrician)
- **Chicago**: 6 businesses (Plumbing, Electrician)

Test the search with:
- Industry: "plumbing" or "electrician"
- City: "New York", "Los Angeles", or "Chicago"

## Next Steps

1. Test all three components (backend, web, desktop)
2. Try searching for businesses
3. Export results in different formats
4. Build desktop installer for distribution
5. Deploy backend to production server

## Support

For issues or questions:
1. Check the API health: `GET http://localhost:5000/health`
2. Review error logs in console
3. Check `.env` configuration
4. Verify all dependencies are installed

## License

Proprietary - Aurum Ventura
