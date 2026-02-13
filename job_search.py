import requests
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Core Keywords
TECH = '("RTL" OR "Physical Design" OR "ASIC" OR "Hardware")'
LEVEL = '("Fresher" OR "0 years" OR "Trainee")'

def send_to_telegram(title, company, link):
    """Sends a formatted message with a clear button/link."""
    message = (
        f"🎯 *New Opening Found*\n\n"
        f"🏢 *Company:* {company}\n"
        f"📌 *Role:* {title}\n\n"
        f"🔗 [APPLY DIRECTLY HERE]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

def scrape_linkedin_india():
    """Engine 1: Scans LinkedIn for individual India-based jobs."""
    search_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={TECH.replace(' ', '%20')}%20{LEVEL.replace(' ', '%20')}&location=India&f_TPR=r86400"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('li')
        for card in cards[:5]:  # Limit to top 5 to avoid spam
            try:
                title = card.find('h3', class_='base-search-card__title').text.strip()
                company = card.find('h4', class_='base-search-card__subtitle').text.strip()
                link = card.find('a', class_='base-card__full-link')['href'].split('?')[0]
                send_to_telegram(title, company, link)
            except: continue
    except Exception as e: print(f"LinkedIn Error: {e}")

def get_mnc_portal_links():
    """Engine 2: Generates direct 'Daily Scan' links for major MNC portals."""
    mncs = {
        "Intel India": f"site:intel.com {TECH} {LEVEL} India",
        "Qualcomm India": f"site:qualcomm.com {TECH} {LEVEL} India",
        "NVIDIA India": f"site:nvidia.com {TECH} {LEVEL} India",
        "Synopsys": f"site:synopsys.com {TECH} {LEVEL} India",
        "Naukri Scan": f"{TECH} {LEVEL} site:naukri.com/job-listings"
    }
    
    for name, query in mncs.items():
        # This link opens a GOOGLE search PRE-FILTERED for that company's jobs in the last 24h
        direct_search_link = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbs=qdr:d"
        send_to_telegram("Portal Scan", name, direct_search_link)

if __name__ == "__main__":
    print("Starting mixed scan for India...")
    # Get individual LinkedIn jobs first
    scrape_linkedin_india()
    # Get direct company portal search links second
    get_mnc_portal_links()
