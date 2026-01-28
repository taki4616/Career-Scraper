# Quick Setup Guide

## Option 1: Manual Setup (Recommended)

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt --break-system-packages
```

### Step 2: Start Backend
```bash
python main.py
```
Backend will run on http://localhost:8000

### Step 3: Open Frontend
Open `frontend/index.html` in your browser

---

## Option 2: Using Start Script

```bash
./start.sh
```
Then open `frontend/index.html` in your browser

---

## Option 3: Using Docker

```bash
docker-compose up
```
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

---

## First Time Usage

1. Open the frontend in your browser
2. Enter a keyword (e.g., "python", "javascript", "designer")
3. Click "Scrape Jobs"
4. Wait for results to load (takes 5-10 seconds)
5. View the jobs!

---

## API Testing

Test the API with curl:

```bash
# Scrape jobs
curl -X POST http://localhost:8000/scrape \
  -H "Content-Type: application/json" \
  -d '{"keyword": "python", "limit_per_source": 5}'

# Get all jobs
curl http://localhost:8000/jobs

# Search jobs
curl http://localhost:8000/jobs/search?keyword=python
```

---

## Troubleshooting

**Backend won't start?**
- Make sure Python 3.7+ is installed
- Install dependencies: `pip install -r backend/requirements.txt --break-system-packages`

**Frontend can't connect?**
- Make sure backend is running on port 8000
- Check console for errors (F12 in browser)

**No jobs found?**
- Try different keywords
- Some websites may block automated requests
- Check your internet connection

---

## Next Steps

- Customize the scraper in `backend/scraper.py`
- Add new job sources
- Modify the UI in `frontend/index.html`
- Set up scheduled scraping
- Add more filters and features
