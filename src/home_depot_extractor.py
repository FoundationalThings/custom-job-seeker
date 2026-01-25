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
        # job_cards = page.locator("li")  # Home Depot job
        # for i in range(job_cards.count()):            
        #     card = job_cards.nth(i)
        #     all_info = card.locator("a.job-link").get_attribute("data-job")
        #     title = all_info["title"]
        #     link = all_info["url"]
                                                                
        #     #title = card.locator(".job-title").inner_text()
        #     #link = card.locator("a.job-link").get_attribute("href")
        #     location = card.locator("a.job-location").inner_text()
            
        #     jobs.append({
        #         "title": title,
        #         "link": link,
        #         "location": location
        #     })

        jobs.append({"title": page, "link": "N/A", "location": "N/A"})
        
        browser.close()
        return jobs
