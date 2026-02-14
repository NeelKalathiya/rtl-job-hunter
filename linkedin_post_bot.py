import requests
from bs4 import BeautifulSoup
import os
import time

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Keywords: Strictly looking for hiring context
TECH = '("RTL" OR "Physical Design" OR "ASIC" OR "Hardware" OR "VLSI")'
LEVEL = '("Fresher" OR "0 years" OR "Trainee" OR "New Grad" OR "Trained Fresher")'
ACTION = '("hiring" OR "job alert" OR "opening" OR "recruiting")'

def send_to_telegram(title, link):
    message = (
        f"📣 *NEW LINKEDIN POST ALERT*\n\n"
        f"📌 *Details:* {title}\n"
        f"🔗 [VIEW POST ON LINKEDIN]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
        # 1.5s delay to prevent Telegram spam limits
        time.sleep(1.5) 
    except Exception as e:
        print(f"Telegram Error: {e}")

def hunt_linkedin_posts():
    """Uses Google Dorking to find every relevant LinkedIn post."""
    # site:linkedin.com/posts/ targets the specific directory for status updates
    # tbs=qdr:d filters for the last 24 hours
    query = f'site:linkedin.com/posts/ {TECH} {LEVEL} {ACTION} "India"'
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbs=qdr:d&num=50"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Google search results are contained in 'div.g' blocks
        results = soup.find_all('div', class_='g')
        
        if not results:
            print("No new posts found in the last 24 hours.")
            return

        for res in results:
            link_tag = res.find('a')
            if not link_tag: continue
            
            link = link_tag['href']
            title = res.find('h3').text if res.find('h3') else "LinkedIn Hiring Post"
            
            # Ensure it's actually a LinkedIn post link
            if "/posts/" in link:
                # Clean the link (remove Google tracking)
                clean_link = link.split('&')[0]
                send_to_telegram(title, clean_link)
                
    except Exception as e:
        print(f"Error during post hunt: {e}")

if __name__ == "__main__":
    print("🚀 Starting LinkedIn Post Hunter...")
    hunt_linkedin_posts()
