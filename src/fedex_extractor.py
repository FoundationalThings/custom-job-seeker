from playwright.sync_api import sync_playwright

def fetch_jobs_fedex(url):
    """Fetch FedEx jobs using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the FedEx jobs page
        page.goto(url)
        
        # Wait for dynamic content to load
        page.wait_for_selector(".job-result-list")  # Example selector identifying the job list container
        
        # Extract job details
        jobs = []
        job_cards = page.locator(".job-result-list .job-listing")  # Example, adjust selector as needed
        for i in range(job_cards.count()):
            card = job_cards.nth(i)
            title = card.locator(".job-title").inner_text()
            link = card.locator("a").get_attribute("href")
            location = card.locator(".job-location").inner_text()
            
            jobs.append({
                "title": title,
                "link": link,
                "location": location
            })
        
        browser.close()
        return jobs
