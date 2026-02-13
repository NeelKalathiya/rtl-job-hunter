import requests
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Your specific hardware keywords
KEYWORDS = '("RTL" OR "Physical Design" OR "ASIC" OR "Hardware") AND (Fresher OR "0 years" OR Trainee)'

def send_to_telegram(company, title, link):
    """Sends each job as a separate notification."""
    message = (
        f"🏢 *Company:* {company}\n"
        f"📌 *Role:* {title}\n"
        f"🔗 [Direct Apply Link]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

def scrape_linkedin_india():
    # Using the LinkedIn 'Guest' API which is more stable for scraping
    search_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={KEYWORDS.replace(' ', '%20')}&location=India&f_TPR=r86400&start=0"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all('li') # LinkedIn Guest API returns list items

        for card in job_cards[:10]: # Check top 10 separate jobs
            try:
                title = card.find('h3', class_='base-search-card__title').text.strip()
                company = card.find('h4', class_='base-search-card__subtitle').text.strip()
                # Get the clean direct link
                link = card.find('a', class_='base-card__full-link')['href'].split('?')[0]
                
                send_to_telegram(company, title, link)
                time.sleep(1) # Small delay to avoid Telegram spam limits
            except:
                continue
    except Exception as e:
        print(f"LinkedIn Error: {e}")

if __name__ == "__main__":
    print("Starting deep scan for India Hardware/VLSI roles...")
    scrape_linkedin_india()
