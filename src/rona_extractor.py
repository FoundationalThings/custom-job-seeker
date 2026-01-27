from playwright.sync_api import sync_playwright

BASE_URL = "https://jobs.ronainc.ca"

def fetch_jobs_rona(url):
    """Fetch RONA jobs using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the RONA jobs page
        page.goto(f"{BASE_URL}/careers", wait_until="networkidle")
        page.wait_for_selector("a.text-xl.font-black.uppercase.text-black")
        
        titles = page.locator("a.text-xl.font-black.uppercase.text-black")


        jobs = []

        for i in range(titles.count()):            
            jobs.append({
                "title": titles.nth(i).inner_text(),
                "link": "",
                "location": ""
            })
        

        
        # page.goto(f"{BASE_URL}/careers")
      
        # # Wait for dynamic content to load
        # page.wait_for_selector("main")  # RONA list
        
        # # Extract job details
        # jobs = []
        # job_cards = page.locator("div.flex.w-full.items-center")  # RONA job
        # for i in range(job_cards.count()):            
        #     card = job_cards.nth(i)
            
        #     title = card.locator("a.text-xl.font-black.uppercase.text-black").inner_text()
        #     link = card.locator("a.text-xl.font-black.uppercase.text-black").get_attribute("href")
        #     location = ""
        #     # link = card.get_attribute("href")
        #     # location = card.locator("div.job-location").inner_text()
            

        
        browser.close()
        return jobs
