import requests
from bs4 import BeautifulSoup
import os
import time

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# STRICT KEYWORDS: Using quotes forces the engine to match EXACTLY
# This prevents "Lead" or "Senior" roles from appearing.
TECH = '("RTL" OR "Physical Design" OR "ASIC" OR "Hardware")'
LEVEL = '("Fresher" OR "0 years" OR "Trainee" OR "Entry Level" OR "New Grad")'
NOT_WANTED = '-"Lead" -"Senior" -"Principal" -"Staff" -"Manager"'

def send_to_telegram(category, company, title, link):
    """Sends every finding without limits. 1.5s delay is required."""
    message = (
        f"🚀 *TYPE: {category}*\n\n"
        f"🏢 *Company:* {company}\n"
        f"📌 *Role:* {title}\n"
        f"🔗 [VIEW ON LINKEDIN]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
        time.sleep(1.5) # Protection from Telegram ban
    except: pass

def get_unlimited_linkedin_leads():
    # 1. SEARCH FOR JOBS (STRICT)
    # We use the search query to EXCLUDE senior roles
    query = f'{TECH} AND {LEVEL} {NOT_WANTED}'
    li_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={query.replace(' ', '%20')}&location=India&f_TPR=r604800&start=0"
    
    # 2. SEARCH FOR POSTS (STRICT via Google)
    # This is the only way to find individual 'Hiring' posts
    post_query = f'site:linkedin.com/posts/ {TECH} {LEVEL} "India" "hiring" {NOT_WANTED}'
    google_url = f"https://www.google.com/search?q={post_query.replace(' ', '+')}&tbs=qdr:w&num=20"

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    # ENGINE 1: JOBS
    try:
        res = requests.get(li_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        for card in soup.find_all('li'):
            try:
                title = card.find('h3', class_='base-search-card__title').text.strip()
                # Secondary check: If "Senior" or "Lead" is in title, SKIP IT
                if any(x in title.lower() for x in ["lead", "senior", "manager", "staff", "principal"]):
                    continue
                company = card.find('h4', class_='base-search-card__subtitle').text.strip()
                link = card.find('a', class_='base-card__full-link')['href'].split('?')[0]
                send_to_telegram("JOB OPENING", company, title, link)
            except: continue
    except: pass

    # ENGINE 2: POSTS
    try:
        res = requests.get(google_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        for r in soup.find_all('div', class_='g'):
            try:
                link = r.find('a')['href']
                if "/posts/" in link:
                    title = r.find('h3').text if r.find('h3') else "LinkedIn Post"
                    # Check title for senior keywords
                    if any(x in title.lower() for x in ["lead", "senior", "manager"]):
                        continue
                    send_to_telegram("HIRING POST", "LinkedIn User", title, link)
            except: continue
    except: pass

if __name__ == "__main__":
    get_unlimited_linkedin_leads()
