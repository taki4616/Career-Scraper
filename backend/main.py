from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from datetime import datetime
from scraper import JobScraper
import sqlite3

app = FastAPI(title="Job Aggregator API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DB_PATH = "../data/jobs.db"

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            url TEXT,
            source TEXT,
            scraped_at TEXT,
            keyword TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

class JobSearchRequest(BaseModel):
    keyword: str = "python"
    limit_per_source: int = 10

class Job(BaseModel):
    title: str
    company: str
    location: str
    url: str
    source: str
    scraped_at: str

scraper = JobScraper()

@app.get("/")
def read_root():
    return {
        "message": "Job Aggregator API",
        "version": "1.0",
        "endpoints": {
            "/scrape": "POST - Scrape jobs by keyword",
            "/jobs": "GET - Get all stored jobs",
            "/jobs/search": "GET - Search jobs by keyword",
            "/jobs/source/{source}": "GET - Get jobs by source"
        }
    }

@app.post("/scrape")
async def scrape_jobs(request: JobSearchRequest, background_tasks: BackgroundTasks):
    """Scrape jobs based on keyword"""
    try:
        jobs = scraper.scrape_all(
            keyword=request.keyword,
            limit_per_source=request.limit_per_source
        )
        
        # Save to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        for job in jobs:
            cursor.execute("""
                INSERT INTO jobs (title, company, location, url, source, scraped_at, keyword)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                job['title'],
                job['company'],
                job['location'],
                job['url'],
                job['source'],
                job['scraped_at'],
                request.keyword
            ))
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": f"Scraped {len(jobs)} jobs for keyword '{request.keyword}'",
            "jobs": jobs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs")
def get_all_jobs(limit: int = 100):
    """Get all stored jobs"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        jobs = []
        for row in rows:
            jobs.append({
                "id": row[0],
                "title": row[1],
                "company": row[2],
                "location": row[3],
                "url": row[4],
                "source": row[5],
                "scraped_at": row[6],
                "keyword": row[7]
            })
        
        return {"jobs": jobs, "count": len(jobs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs/search")
def search_jobs(keyword: str):
    """Search jobs by keyword"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM jobs 
            WHERE keyword LIKE ? OR title LIKE ? OR company LIKE ?
            ORDER BY id DESC
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        rows = cursor.fetchall()
        conn.close()
        
        jobs = []
        for row in rows:
            jobs.append({
                "id": row[0],
                "title": row[1],
                "company": row[2],
                "location": row[3],
                "url": row[4],
                "source": row[5],
                "scraped_at": row[6],
                "keyword": row[7]
            })
        
        return {"jobs": jobs, "count": len(jobs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs/source/{source}")
def get_jobs_by_source(source: str):
    """Get jobs from a specific source"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs WHERE source = ? ORDER BY id DESC", (source,))
        rows = cursor.fetchall()
        conn.close()
        
        jobs = []
        for row in rows:
            jobs.append({
                "id": row[0],
                "title": row[1],
                "company": row[2],
                "location": row[3],
                "url": row[4],
                "source": row[5],
                "scraped_at": row[6],
                "keyword": row[7]
            })
        
        return {"jobs": jobs, "count": len(jobs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/jobs")
def clear_all_jobs():
    """Clear all jobs from database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jobs")
        conn.commit()
        conn.close()
        return {"success": True, "message": "All jobs cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
