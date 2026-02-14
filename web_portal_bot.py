import requests
from bs4 import BeautifulSoup
import os
import time
import re

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Keywords
KEYWORDS = '("RTL" OR "Physical Design" OR "ASIC" OR "Hardware") AND (Fresher OR "0 years" OR Trainee)'

def send_to_telegram(type_label, company, title, link):
    """Sends each finding as a separate notification."""
    message = (
        f"📣 *Type:* {type_label}\n"
        f"🏢 *Company/Source:* {company}\n"
        f"📌 *Details:* {title}\n"
        f"🔗 [Direct Link]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
        time.sleep(1.5) # Prevents Telegram spam block
    except Exception as e:
        print(f"Telegram Error: {e}")

def scrape_linkedin_jobs():
    """Engine 1: Scans LinkedIn Job Section."""
    search_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={KEYWORDS.replace(' ', '%20')}&location=India&f_TPR=r604800&start=0"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all('li')

        for card in job_cards[:5]:
            try:
                title = card.find('h3', class_='base-search-card__title').text.strip()
                company = card.find('h4', class_='base-search-card__subtitle').text.strip()
                link = card.find('a', class_='base-card__full-link')['href'].split('?')[0]
                send_to_telegram("JOB OPENING", company, title, link)
            except: continue
    except Exception as e:
        print(f"Job Scrape Error: {e}")

def search_linkedin_posts():
    """Engine 2: Scans LinkedIn POSTS via Google (Bypasses Login)."""
    # Searching for posts from the last 7 days to get more results
    query = f'site:linkedin.com/posts/ {KEYWORDS} "India" "hiring"'
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbs=qdr:w"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='g')

        for res in results[:5]: # Limit to top 5 posts
            try:
                link = res.find('a')['href']
                title = res.find('h3').text if res.find('h3') else "LinkedIn Post"
                if "/posts/" in link:
                    send_to_telegram("HIRING POST", "LinkedIn Post", title, link)
            except: continue
    except Exception as e:
        print(f"Post Search Error: {e}")

if __name__ == "__main__":
    print("Starting combined Job and Post scan...")
    # Run both engines
    scrape_linkedin_jobs()
    search_linkedin_posts()
