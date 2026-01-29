# 🚀 Career-Scraper

A web scraping application that aggregates remote job listings from multiple sources including RemoteOK and WeWorkRemotely. Built with Python (FastAPI + Beautiful Soup) backend and vanilla JavaScript frontend.

## Features

- 🔍 **Multi-Source Scraping**: Scrapes jobs from RemoteOK and WeWorkRemotely
- 🗄️ **SQLite Database**: Stores all scraped jobs locally
- 🎯 **Keyword Search**: Find jobs by technology, role, or company
- 📊 **Statistics Dashboard**: View job counts by source
- 🌐 **REST API**: Full API for programmatic access
- 💻 **Clean UI**: Modern, responsive interface

## Project Structure

```
job-aggregator/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── scraper.py       # Job scraping logic
│   └── requirements.txt # Python dependencies
├── frontend/
│   └── index.html       # Web interface
└── data/
    └── jobs.db          # SQLite database (auto-created)
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt --break-system-packages
```

### 2. Start the Backend

```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

### 3. Open the Frontend

Open `frontend/index.html` in your web browser, or serve it with:

```bash
cd frontend
python -m http.server 3000
```

Then visit `http://localhost:3000`

## Usage

### Web Interface

1. Enter a job keyword (e.g., "python", "javascript", "designer")
2. Set the number of jobs to scrape per source
3. Click "Scrape Jobs" to start scraping
4. Click "Load Saved" to view previously scraped jobs

### API Endpoints

#### Scrape Jobs

```bash
POST http://localhost:8000/scrape
Content-Type: application/json

{
  "keyword": "python",
  "limit_per_source": 10
}
```

#### Get All Jobs

```bash
GET http://localhost:8000/jobs?limit=100
```

#### Search Jobs

```bash
GET http://localhost:8000/jobs/search?keyword=python
```

#### Get Jobs by Source

```bash
GET http://localhost:8000/jobs/source/RemoteOK
```

#### Clear All Jobs

```bash
DELETE http://localhost:8000/jobs
```

## How It Works

### Scraping Process

1. **User Input**: User enters a keyword (e.g., "python")
2. **Request**: Frontend sends POST request to `/scrape` endpoint
3. **Scraping**: Backend scrapes RemoteOK and WeWorkRemotely
4. **Storage**: Jobs are saved to SQLite database
5. **Response**: Jobs are returned to frontend and displayed

### Data Structure

Each job contains:

- `title`: Job title
- `company`: Company name
- `location`: Job location (usually "Remote")
- `url`: Link to job posting
- `source`: Source website (RemoteOK, WeWorkRemotely)
- `scraped_at`: Timestamp of when job was scraped
- `keyword`: Search keyword used

## Customization

### Adding New Job Sources

Edit `backend/scraper.py` and add a new method:

```python
def scrape_new_source(self, keyword: str, limit: int) -> List[Dict]:
    """Scrape jobs from a new source"""
    jobs = []
    # Your scraping logic here
    return jobs
```

Then add it to `scrape_all()` method.

### Modifying the UI

Edit `frontend/index.html` to customize:

- Colors and styling (in the `<style>` section)
- Layout and structure
- API endpoint URL (change `API_URL` in JavaScript)

## Rate Limiting & Ethics

⚠️ **Important**: This scraper includes delays between requests to be respectful to websites. Key practices:

- 2-second delay between different sources
- User-Agent headers to identify the bot
- Limited requests per scraping session
- Only scrapes publicly available data

**Ethical Guidelines**:

- Check `robots.txt` before scraping
- Don't overload servers with requests
- Respect website terms of service
- Use data responsibly

## Troubleshooting

### Backend won't start

- Make sure all dependencies are installed: `pip install -r requirements.txt --break-system-packages`
- Check if port 8000 is available
- Look for error messages in terminal

### Frontend can't connect to API

- Make sure backend is running on port 8000
- Check CORS settings if serving frontend from different domain
- Verify API_URL in `index.html` is correct

### No jobs found

- Some websites may have changed their HTML structure
- Try different keywords
- Check if websites are accessible from your location
- Some sites may block automated requests

## Future Enhancements

- [ ] Add more job sources (Indeed, LinkedIn, etc.)
- [ ] Email alerts for new jobs matching criteria
- [ ] Job filtering by salary, location, experience
- [ ] Scheduled automatic scraping (cron jobs)
- [ ] User authentication and saved searches
- [ ] Machine learning for job recommendations
- [ ] Export jobs to CSV/PDF

## Tech Stack

- **Backend**: Python 3.x, FastAPI, Beautiful Soup, SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: SQLite3

## License

MIT License - feel free to use and modify for your own projects!

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

Built with ❤️ for job seekers everywhere
