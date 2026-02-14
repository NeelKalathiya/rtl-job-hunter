import requests
from bs4 import BeautifulSoup
import os
import time
import re

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Keywords for India 2026 Hardware Roles
TECH = '("RTL" OR "Physical Design" OR "ASIC" OR "Hardware")'
EXP = '("Fresher" OR "0 years" OR "Trainee" OR "New Grad")'

def send_to_telegram(category, company, title, link):
    """Sends each finding as a separate message with 1.5s delay."""
    icon = "🏢" if category == "MNC Portal" else "🌐"
    message = (
        f"{icon} *Type:* {category}\n"
        f"🏢 *Company:* {company}\n"
        f"📌 *Role:* {title}\n"
        f"🔗 [APPLY HERE]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
        time.sleep(1.5) # REQUIRED to prevent Telegram spam block
    except: pass

def get_jobs():
    """Engine: Search Google for LinkedIn, Naukri, and MNC Career Sites."""
    # We use Google because it's the only way to get results without a LinkedIn login
    queries = {
        "LinkedIn Jobs": f"site:linkedin.com/jobs/view {TECH} {EXP} India",
        "LinkedIn Posts": f"site:linkedin.com/posts/ {TECH} {EXP} India hiring",
        "MNC Portals": f"(site:intel.com OR site:nvidia.com OR site:qualcomm.com) {TECH} {EXP} India"
    }

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    for category, query in queries.items():
        # Searching the past week ('tbs=qdr:w') to ensure we get results
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbs=qdr:w"
        
        try:
            res = requests.get(search_url, headers=headers, timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Find all search result blocks
            results = soup.find_all('div', class_='g')
            
            count = 0
            for r in results:
                if count >= 4: break # Limit to top 4 per category (Total 12 per hour)
                
                link_tag = r.find('a')
                if not link_tag: continue
                
                link = link_tag['href']
                title = r.find('h3').text if r.find('h3') else "View Opening"
                
                # Extracting company name from link
                company = "MNC"
                for c in ["Intel", "Nvidia", "Qualcomm", "Linkedin", "Naukri"]:
                    if c.lower() in link.lower(): company = c
                
                send_to_telegram(category, company, title, link)
                count += 1
        except Exception as e:
            print(f"Error in {category}: {e}")

if __name__ == "__main__":
    get_jobs()
