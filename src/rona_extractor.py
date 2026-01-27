from playwright.sync_api import sync_playwright

BASE_URL = "https://jobs.ronainc.ca"

def fetch_jobs_rona(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # Change to True later
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        
        page.goto(f"{BASE_URL}/careers", wait_until="domcontentloaded")
        
        # Wait until at least one job title appears
        page.wait_for_function(
            "document.querySelectorAll('a.text-xl.font-black.uppercase.text-black').length > 0",
            timeout=15000
        )
        
        titles = page.locator("a.text-xl.font-black.uppercase.text-black")
        jobs = []
        for i in range(titles.count()):
            jobs.append({"title": titles.nth(i).inner_text(), "link": "", "location": ""})
        
        browser.close()
        return jobs
