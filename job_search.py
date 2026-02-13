import requests
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# 2026 Hardware Keywords for India
ROLES = '("RTL" OR "Physical Design" OR "ASIC" OR "Hardware" OR "Digital Design")'
EXP = '("Fresher" OR "0 years" OR "Trainee" OR "New Grad")'

def send_to_telegram(company, title, apply_link):
    """Sends a formatted alert with a direct clickable button."""
    message = (
        f"🚀 *DIRECT OPENING FOUND*\n\n"
        f"🏢 *Company:* {company}\n"
        f"📌 *Role:* {title}\n\n"
        f"✅ [CLICK TO APPLY DIRECTLY]({apply_link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
        time.sleep(1.5) # Prevents Telegram spam block
    except Exception as e:
        print(f"Telegram Error: {e}")

def get_linkedin_direct_links():
    """Extracts direct 'View Job' links from LinkedIn India."""
    # This URL targets the public 'Job View' pages directly
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={ROLES.replace(' ', '%20')}%20{EXP.replace(' ', '%20')}&location=India&f_TPR=r86400"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        for card in soup.find_all('li'):
            title = card.find('h3', class_='base-search-card__title').text.strip()
            company = card.find('h4', class_='base-search-card__subtitle').text.strip()
            # This generates the clean direct-view link
            raw_link = card.find('a', class_='base-card__full-link')['href'].split('?')[0]
            send_to_telegram(company, title, raw_link)
    except: pass

def get_mnc_direct_links():
    """Generates direct 'Deep Search' links for MNC portals to bypass login walls."""
    # These queries find the ACTUAL job-listing pages indexed by search engines
    mnc_targets = {
        "Intel India": f"site:intel.com/content/www/in {ROLES} {EXP}",
        "Qualcomm India": f"site:qualcomm.com/company/careers {ROLES} {EXP}",
        "NVIDIA India": f"site:nvidia.com/en-in/about-nvidia/careers {ROLES} {EXP}",
        "Synopsys": f"site:synopsys.com/careers {ROLES} {EXP} India",
        "Naukri Direct": f"site:naukri.com/job-listings {ROLES} {EXP}"
    }
    for company, query in mnc_targets.items():
        # This link opens a GOOGLE page pre-filtered for the Apply button of that company
        deep_link = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbs=qdr:d"
        send_to_telegram(company, "Latest Portal Openings", deep_link)

if __name__ == "__main__":
    print("Starting Deep Scan for India 2026 Hardware roles...")
    get_linkedin_direct_links()
    get_mnc_direct_links()
