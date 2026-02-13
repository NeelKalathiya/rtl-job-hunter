import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Targeted technical domains and experience
KEYWORDS = '("RTL" OR "Physical Design" OR "ASIC" OR "Hardware") AND (Fresher OR "0 years" OR Trainee)'

def send_individual_job(company, title, link):
    """Sends each job as its own separate Telegram message."""
    message = (
        f"🏢 *Company:* {company}\n"
        f"📌 *Role:* {title}\n"
        f"🔗 [Direct Apply Link]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

def scrape_jobs():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    # Platform 1: LinkedIn Public Jobs (India)
    li_url = f"https://www.linkedin.com/jobs/search/?keywords={KEYWORDS.replace(' ', '%20')}&location=India&f_TPR=r86400"
    
    try:
        response = requests.get(li_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Finding the individual job cards
        job_cards = soup.find_all('div', class_='base-card')
        
        for card in job_cards[:5]: # Limit to top 5 most recent to avoid spam
            title = card.find('h3', class_='base-search-card__title').text.strip()
            company = card.find('h4', class_='base-search-card__subtitle').text.strip()
            link = card.find('a', class_='base-card__full-link')['href'].split('?')[0]
            
            # This sends EACH job as a separate message to you
            send_individual_job(company, title, link)
            
    except Exception as e:
        print(f"Scraping error: {e}")

if __name__ == "__main__":
    scrape_jobs()
