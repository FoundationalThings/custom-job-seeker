from playwright.sync_api import sync_playwright

def fetch_jobs_home_depot(url):
    """Fetch Home Depot jobs using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the Home Depot jobs page
        page.goto(url)
        
        # Wait for dynamic content to load
        page.wait_for_selector(".jobs-listing")  # Home Depot list
        
        # Extract job details
        jobs = []
        job_cards = page.locator(".job-link")  # Home Depot job
        for i in range(job_cards.count()):
            card = job_cards.nth(i)
            new_badge = card.locator(".new-job-badge").inner_text()
            title = card.locator(".job-title").inner_text()
            if len(new_badge) > 0:
                title = "[ " + new_badge.upper() + "! ] " + title
            link = card.locator("a.job-link").get_attribute("href")
            location = card.locator(".job-location").inner_text()
            
            jobs.append({
                "title": title,
                "link": link,
                "location": location
            })
        
        browser.close()
        return jobs
