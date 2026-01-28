"""
Simple test script to demonstrate the job scraper
Run this after installing dependencies with: pip install -r requirements.txt --break-system-packages
"""

from scraper import JobScraper

def main():
    print("=== Job Aggregator Test ===\n")
    
    # Create scraper instance
    scraper = JobScraper()
    
    # Test scraping
    keyword = "python"
    print(f"Scraping jobs for keyword: '{keyword}'")
    print("This will take a few seconds...\n")
    
    # Scrape from all sources
    jobs = scraper.scrape_all(keyword=keyword, limit_per_source=5)
    
    # Display results
    print(f"\n=== Results ===")
    print(f"Total jobs found: {len(jobs)}\n")
    
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Source: {job['source']}")
        print(f"   Location: {job['location']}")
        print(f"   URL: {job['url'][:50]}..." if len(job['url']) > 50 else f"   URL: {job['url']}")
        print()
    
    # Save to file
    scraper.save_to_file(jobs, "../data/test_jobs.json")
    print("Jobs saved to ../data/test_jobs.json")

if __name__ == "__main__":
    main()
