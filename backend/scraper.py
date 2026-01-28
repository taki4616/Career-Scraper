import requests
from typing import List, Dict
import time
from datetime import datetime
import json

class JobScraper:
    """Scrapes job listings from multiple sources"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def scrape_remoteok(self, keyword: str = "python", limit: int = 10) -> List[Dict]:
        """Fetch jobs from RemoteOK using their JSON API"""
        jobs = []
        try:
            url = "https://remoteok.com/api"
            response = requests.get(url, headers=self.headers, timeout=30)
            data = response.json()

            # First entry is metadata, real jobs start at index 1
            keyword_lower = keyword.lower()
            count = 0
            for entry in data[1:]:
                if count >= limit:
                    break
                position = entry.get('position', '')
                company = entry.get('company', '')
                tags = [t.lower() for t in entry.get('tags', [])]
                description = entry.get('description', '').lower()

                # Match keyword against position, tags, or description
                if (keyword_lower in position.lower() or
                    keyword_lower in tags or
                    keyword_lower in description):
                    jobs.append({
                        'title': position,
                        'company': company,
                        'location': entry.get('location', 'Remote') or 'Remote',
                        'url': entry.get('url', ''),
                        'source': 'RemoteOK',
                        'scraped_at': datetime.now().isoformat()
                    })
                    count += 1

        except Exception as e:
            print(f"Error scraping RemoteOK: {e}")

        return jobs

    def scrape_himalayas(self, keyword: str = "python", limit: int = 10) -> List[Dict]:
        """Fetch jobs from Himalayas.app API"""
        jobs = []
        try:
            url = "https://himalayas.app/jobs/api?limit=50"
            response = requests.get(url, headers=self.headers, timeout=30)
            data = response.json()

            keyword_lower = keyword.lower()
            count = 0
            for entry in data.get('jobs', []):
                if count >= limit:
                    break
                title = entry.get('title', '')
                excerpt = entry.get('excerpt', '')
                categories = ' '.join(entry.get('categories', []))

                if (keyword_lower in title.lower() or
                    keyword_lower in excerpt.lower() or
                    keyword_lower in categories.lower()):
                    locations = entry.get('locationRestrictions', [])
                    location = ', '.join(locations) if locations else 'Remote'
                    jobs.append({
                        'title': title,
                        'company': entry.get('companyName', 'Unknown'),
                        'location': location,
                        'url': entry.get('applicationLink', ''),
                        'source': 'Himalayas',
                        'scraped_at': datetime.now().isoformat()
                    })
                    count += 1

        except Exception as e:
            print(f"Error scraping Himalayas: {e}")

        return jobs

    def scrape_all(self, keyword: str = "python", limit_per_source: int = 10) -> List[Dict]:
        """Scrape all sources and combine results"""
        all_jobs = []

        print(f"Scraping RemoteOK for '{keyword}'...")
        all_jobs.extend(self.scrape_remoteok(keyword, limit_per_source))
        time.sleep(1)

        print(f"Scraping Himalayas for '{keyword}'...")
        all_jobs.extend(self.scrape_himalayas(keyword, limit_per_source))

        print(f"Found {len(all_jobs)} total jobs")
        return all_jobs
    
    def save_to_file(self, jobs: List[Dict], filename: str = "jobs.json"):
        """Save scraped jobs to JSON file"""
        with open(filename, 'w') as f:
            json.dump(jobs, f, indent=2)
        print(f"Saved {len(jobs)} jobs to {filename}")


if __name__ == "__main__":
    scraper = JobScraper()
    jobs = scraper.scrape_all(keyword="python", limit_per_source=5)
    scraper.save_to_file(jobs, "../data/jobs.json")
