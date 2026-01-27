from playwright.sync_api import sync_playwright

def fetch_jobs_home_depot(url):
    """Fetch Home Depot jobs using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the Home Depot jobs page
        page.goto(url)
        
        # Wait for dynamic content to load
        page.wait_for_selector("ul#job-list-items.jobs-content.jobs-content-exp2")  # Home Depot list
        
        # Extract job details
        jobs = []
        job_cards = page.locator("ul#job-list-items > li > a.job-link")  # Home Depot job
        for i in range(job_cards.count()):            
            card = job_cards.nth(i)
            
            link = card.get_attribute("href")
            title = card.locator("div.job-title").inner_text()
            location = card.locator("div.job-location").inner_text()
            
            jobs.append({
                "title": title,
                "link": link,
                "location": location
            })
        
        browser.close()
        return jobs
