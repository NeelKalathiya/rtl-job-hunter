import requests
from bs4 import BeautifulSoup
import os
import time
import random

BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Updated Keywords for broader reach
TECH = '("RTL" OR "Physical Design" OR "ASIC" OR "VLSI")'
EXP = '("Fresher" OR "0 years" OR "Trainee" OR "New Grad")'

def send_to_telegram(category, company, title, link):
    message = (
        f"🌐 *Type:* {category}\n"
        f"🏢 *Company:* {company}\n"
        f"📌 *Role:* {title}\n"
        f"🔗 [VIEW ON LINKEDIN]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
    time.sleep(2) # Increased delay to avoid Telegram & LinkedIn rate limits

def scrape_linkedin_jobs():
    # 1. Use a fresh User-Agent to avoid '0 results' block
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    ]
    
    # 2. Optimized Guest API URL for India
    # f_TPR=r604800 is the filter for the 'Past Week' to ensure we find results
    li_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={TECH.replace(' ', '%20')}%20{EXP.replace(' ', '%20')}&location=India&f_TPR=r604800&start=0"
    
    headers = {"User-Agent": random.choice(user_agents)}
    
    try:
        res = requests.get(li_url, headers=headers, timeout=15)
        if res.status_code != 200:
            print(f"LinkedIn blocked the request. Status Code: {res.status_code}")
            return

        soup = BeautifulSoup(res.text, 'html.parser')
        # LinkedIn uses 'li' for job cards in this API
        cards = soup.find_all('li')
        
        print(f"Found {len(cards)} potential jobs.") # For GitHub Logs
        
        count = 0
        for card in cards:
            if count >= 10: break 
            
            try:
                # Using the specific classes for the Guest API
                title = card.find('h3', class_='base-search-card__title').get_text(strip=True)
                company = card.find('h4', class_='base-search-card__subtitle').get_text(strip=True)
                link = card.find('a', class_='base-card__full-link')['href'].split('?')[0]
                
                send_to_telegram("Job Opening", company, title, link)
                count += 1
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"Scrape Error: {e}")

if __name__ == "__main__":
    scrape_linkedin_jobs()
