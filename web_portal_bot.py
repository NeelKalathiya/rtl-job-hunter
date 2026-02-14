import requests
from bs4 import BeautifulSoup
import os
import time

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# 1. Technical Keywords (Must have one of these)
TECH_KEYS = ["rtl", "physical design", "asic", "hardware", "vlsi", "digital design"]

# 2. Experience Keywords (MUST have one of these)
EXP_KEYS = ["0 year", "fresher", "new grad", "trained fresher", "trainee", "intern", "entry level"]

# 3. Action Keywords - ONLY USED FOR POSTS
ACTION_KEYS = ["hiring", "job alert", "opening", "recruiting", "vacancy"]

def send_to_telegram(category, company, title, link):
    message = (
        f"🎯 *MATCHED ALERT: {category}*\n\n"
        f"🏢 *Source:* {company}\n"
        f"📌 *Details:* {title}\n"
        f"🔗 [VIEW OPENING]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
        time.sleep(1.5) 
    except: pass

def check_criteria(text, is_post=False):
    """Strict logic: Tech + Exp. Posts must also have an Action key."""
    text = text.lower()
    has_tech = any(k in text for k in TECH_KEYS)
    has_exp = any(k in text for k in EXP_KEYS)
    is_senior = any(k in text for k in ["lead", "senior", "principal", "staff", "manager"])
    
    if is_post:
        # Posts must explicitly mention hiring context
        has_action = any(k in text for k in ACTION_KEYS)
        return has_tech and has_exp and has_action and not is_senior
    
    return has_tech and has_exp and not is_senior

def run_unlimited_filtered_scan():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    # --- ENGINE 1: LINKEDIN POSTS (BROADER SEARCH) ---
    # Here we use action words like "hiring" to find recruiter posts
    post_search = 'site:linkedin.com/posts/ ("hiring" OR "job alert") AND ("rtl" OR "asic") "India"'
    google_url = f"https://www.google.com/search?q={post_search.replace(' ', '+')}&tbs=qdr:w&num=30"

    try:
        res = requests.get(google_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        for r in soup.find_all('div', class_='g'):
            title = r.find('h3').text if r.find('h3') else ""
            link = r.find('a')['href']
            if check_criteria(title, is_post=True) and "/posts/" in link:
                send_to_telegram("HIRING POST", "LinkedIn Post", title, link)
    except: pass

    # --- ENGINE 2: LINKEDIN JOBS (STRICT TECHNICAL SEARCH) ---
    # No "hiring" keywords here, just pure job title search
    li_query = '("rtl" OR "physical design" OR "asic")'
    li_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={li_query}&location=India&f_TPR=r604800"

    try:
        res = requests.get(li_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        for card in soup.find_all('li'):
            title = card.find('h3', class_='base-search-card__title').text.strip()
            # Strict filtering for technical and experience fit
            if check_criteria(title, is_post=False):
                company = card.find('h4', class_='base-search-card__subtitle').text.strip()
                link = card.find('a', class_='base-card__full-link')['href'].split('?')[0]
                send_to_telegram("JOB OPENING", company, title, link)
    except: pass

if __name__ == "__main__":
    run_unlimited_filtered_scan()
