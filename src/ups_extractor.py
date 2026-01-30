from playwright.sync_api import sync_playwright

def fetch_jobs_ups(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the jobs page
        page.goto(url)
        
        # Wait for dynamic content to load
        page.wait_for_selector(".results-state")  # the UPS jobslist
        
        # Extract job details
        jobs = []
        job_cards = page.locator('[data-ph-at-id="jobs-list-item"]')
        for i in range(job_cards.count()):
            card = job_cards.nth(i)
            title = card.locator('[data-ph-at-id="job-link"]').inner_text()
            link = card.locator('[data-ph-at-id="job-link"]').get_attribute("href")
            location = card.locator(".job-location").inner_text()
            
            jobs.append({
                "title": title,
                "link": link,
                "location": location
            })
        
        browser.close()
        return jobs
