from playwright.sync_api import sync_playwright

def fetch_jobs_fedex(url):
    """Fetch FedEx jobs using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the FedEx jobs page
        page.goto(url)
        
        # Wait for dynamic content to load
        page.wait_for_selector(".results-list")  # FedEx list
        
        # Extract job details
        jobs = []
        job_cards = page.locator(".results-list__item")  # FedEx job
        for i in range(job_cards.count()):
            card = job_cards.nth(i)
            title = card.locator(".results-list__item-title").inner_text()
            link = card.locator("a.results-list__item-title--link").get_attribute("href")
            link = link = "https://careers.fedex.com/" + link
            location = card.locator(".results-list__item-street--label").inner_text()
            
            jobs.append({
                "title": title,
                "link": link,
                "location": location
            })
        
        browser.close()
        return jobs
