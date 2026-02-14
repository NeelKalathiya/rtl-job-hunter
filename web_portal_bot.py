import requests
from bs4 import BeautifulSoup
import os
import time

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Your Hardware Keywords
KEYWORDS = '("RTL" OR "Physical Design" OR "ASIC" OR "Hardware") AND (Fresher OR "0 years" OR Trainee)'

def send_to_telegram(type_label, company, title, link):
    """Sends every finding. No limits, just a safety delay."""
    message = (
        f"🚀 *UNLIMITED ALERT: {type_label}*\n\n"
        f"🏢 *Source:* {company}\n"
        f"📌 *Details:* {title}\n"
        f"🔗 [Direct Link]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
        # 1.5s is the safety limit to prevent Telegram from blocking your bot
        time.sleep(1.5) 
    except Exception as e:
        print(f"Telegram Error: {e}")

def scrape_all_linkedin_jobs():
    """Engine 1: Scans ALL available public LinkedIn Jobs (India)."""
    # f_TPR=r604800 = Past Week to ensure no opening is missed
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    
    # We check the first 50 results (increments of 25)
    for start in [0, 25]: 
        search_url = f"{base_url}?keywords={KEYWORDS.replace(' ', '%20')}&location=India&f_TPR=r604800&start={start}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        try:
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            job_cards = soup.find_all('li')

            if not job_cards:
                break

            for card in job_cards:
                try:
                    title = card.find('h3', class_='base-search-card__title').text.strip()
                    company = card.find('h4', class_='base-search-card__subtitle').text.strip()
                    link = card.find('a', class_='base-card__full-link')['href'].split('?')[0]
                    send_to_telegram("JOB", company, title, link)
                except: continue
        except Exception as e:
            print(f"Job Scrape Error at start {start}: {e}")

def search_all_linkedin_posts():
    """Engine 2: Scans ALL public LinkedIn Posts via Google."""
    # Searching for posts from the last 7 days
    query = f'site:linkedin.com/posts/ {KEYWORDS} "India" "hiring"'
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbs=qdr:w&num=100"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='g')

        for res in results:
            try:
                link = res.find('a')['href']
                title = res.find('h3').text if res.find('h3') else "LinkedIn Post"
                if "/posts/" in link:
                    send_to_telegram("POST", "LinkedIn Hiring Alert", title, link)
            except: continue
    except Exception as e:
        print(f"Post Search Error: {e}")

if __name__ == "__main__":
    print("Starting Unlimited Scan...")
    scrape_all_linkedin_jobs()
    search_all_linkedin_posts()
