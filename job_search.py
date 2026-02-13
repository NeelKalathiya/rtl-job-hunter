import os
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Runs without a window
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

def find_india_rtl_jobs():
    driver = get_driver()
    # Direct LinkedIn search for India-based RTL roles posted in last 24h
    url = "https://www.linkedin.com/jobs/search/?keywords=RTL%20Design%20Trainee%20OR%20New%20Grad&location=India&f_TPR=r86400"
    
    jobs = []
    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        cards = soup.find_all('div', class_='base-card') # Common card for LinkedIn jobs

        for card in cards[:8]: # Check top 8 new openings
            title = card.find('h3', class_='base-search-card__title').text.strip()
            company = card.find('h4', class_='base-search-card__subtitle').text.strip()
            # This extracts the actual direct job link
            raw_link = card.find('a', class_='base-card__full-link')['href'].split('?')[0]
            
            jobs.append(f"🏢 {company}\n📌 {title}\n🔗 [Direct Apply Link]({raw_link})")
    finally:
        driver.quit()
    return jobs

def send_telegram(jobs):
    if not jobs:
        msg = "🔍 No new direct RTL Trainee openings found in India today."
    else:
        msg = f"🚀 New RTL India Direct Openings ({datetime.now().strftime('%d %b')})\n\n" + "\n\n---\n\n".join(jobs)
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    found_jobs = find_india_rtl_jobs()
    send_telegram(found_jobs)
