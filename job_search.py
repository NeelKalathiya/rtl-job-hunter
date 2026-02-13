import requests
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Keywords for India
TECH = '("RTL" OR "Physical Design" OR "ASIC" OR "Hardware")'
EXP = '("Fresher" OR "0 years" OR "Trainee" OR "New Grad")'

def send_to_telegram(title, company, link):
    """Sends a clear message. Added a delay to prevent Telegram '429 Too Many Requests' error."""
    message = (
        f"🎯 *New Opening Found*\n\n"
        f"🏢 *Company:* {company}\n"
        f"📌 *Role:* {title}\n\n"
        f"🔗 [APPLY DIRECTLY HERE]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
        time.sleep(1.5) # REQUIRED: Prevents bot from being banned by Telegram
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

def scrape_linkedin():
    """Scans LinkedIn for all India hardware roles posted today."""
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={TECH.replace(' ', '%20')}%20{EXP.replace(' ', '%20')}&location=India&f_TPR=r86400"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        for card in soup.find_all('li'):
            title = card.find('h3', class_='base-search-card__title').text.strip()
            company = card.find('h4', class_='base-search-card__subtitle').text.strip()
            link = card.find('a', class_='base-card__full-link')['href'].split('?')[0]
            send_to_telegram(title, company, link)
    except: pass

def deep_mnc_scan():
    """Finds direct apply pages indexed by Google for top MNCs."""
    mncs = {
        "Intel India": f"site:intel.com/content/www/in {TECH} {EXP}",
        "NVIDIA India": f"site:nvidia.com/en-in {TECH} {EXP}",
        "Qualcomm": f"site:qualcomm.com/company/careers {TECH} {EXP} India",
        "Synopsys": f"site:synopsys.com/careers {TECH} {EXP} India",
        "Naukri.com": f"site:naukri.com/job-listings {TECH} {EXP}"
    }
    for name, query in mncs.items():
        search_link = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbs=qdr:d"
        # Since scraping Workday/internal portals directly is blocked, 
        # we give you the Google link that bypasses the 'Login Wall'.
        send_to_telegram("Direct Portal Scan", name, search_link)

if __name__ == "__main__":
    print("Starting Unlimited Scan...")
    scrape_linkedin()
    deep_mnc_scan()
