from googleapiclient.discovery import build
import google.auth
import requests
from bs4 import BeautifulSoup
from fedex_extractor import fetch_jobs_fedex
from home_depot_extractor import fetch_jobs_home_depot


SPREADSHEET_ID = "1jKdw4CsEbBOarEfYaDODsI88OsNkJBHARB3sV9XaQYQ"
RANGE = "A2:C"

def fetch_jobs(url):
    """Route to correct job extractor based on site."""
    if "fedex" in url.lower():
        return fetch_jobs_fedex(url)
    elif "homedepot" in url.lower():
        return fetch_jobs_home_depot(url)
    else:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"ERROR fetching {url}: {e}")
            return []
  
        soup = BeautifulSoup(resp.text, "html.parser")
        jobs = []
    
        # Example: try to guess job postings
        # Look for common patterns: links containing "job", "career", or a job listing container
        for a in soup.find_all("a", href=True):
            href = a['href']
            text = a.get_text(strip=True)
            if text and ("job" in text.lower() or "position" in text.lower()):
                jobs.append({
                    "title": text,
                    "link": href,
                    "location": None  # will fill if we find location later
                })
    
        return jobs

def main():
    creds, _ = google.auth.default(scopes=[
        "https://www.googleapis.com/auth/spreadsheets.readonly"
    ])
    service = build("sheets", "v4", credentials=creds)

    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE
    ).execute()

    rows = result.get("values", [])
    enabled_companies = []

    for row in rows:
        enabled = row[0].strip().upper() if len(row) > 0 else ""
        company = row[1] if len(row) > 1 else "Unnamed Company"
        url = row[2] if len(row) > 2 else None
        if enabled == "TRUE" and url:
            enabled_companies.append((company, url))

    print("Extracting jobs...")
    for company, url in enabled_companies:
        print(f"\n=== {company} ({url}) ===")
        jobs = fetch_jobs(url)
        if not jobs:
            print("No jobs found or could not fetch page.")
            continue

        for job in jobs:
            print(f"- {job['title']} → {job['link']} ({job['location']})")

if __name__ == "__main__":
    main()
