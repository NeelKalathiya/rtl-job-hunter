import requests
from bs4 import BeautifulSoup
import os
import time
import random

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Keywords: Strictly looking for hiring context for the VLSI industry
TECH = '(RTL OR "Physical Design" OR ASIC OR VLSI OR Hardware)'
LEVEL = '(Fresher OR "0 years" OR Trainee OR "New Grad" OR "Trained Fresher")'
ACTION = '(hiring OR "job alert" OR opening OR recruiting)'

def send_to_telegram(title, link):
    message = (
        f"📣 *NEW HIRING POST (Last Week)*\n\n"
        f"📌 *Details:* {title}\n"
        f"🔗 [VIEW ON LINKEDIN]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
        time.sleep(2) # Safety delay for Telegram limits
    except: pass

def hunt_linkedin_posts():
    """Engine: Uses deep keyword patterns to find indexed LinkedIn posts."""
    # Pattern 1: Direct hiring context. Pattern 2: URL-based post discovery.
    queries = [
        f'"{TECH}" "{LEVEL}" "{ACTION}" India LinkedIn',
        f'inurl:linkedin.com/posts/ {TECH} {LEVEL} India'
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    found_links = set()

    for query in queries:
        # tbs=qdr:w filters for the LAST WEEK
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbs=qdr:w"
        
        try:
            response = requests.get(search_url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all potential result blocks
            for g in soup.find_all('div', class_='g'):
                link_tag = g.find('a')
                if not link_tag: continue
                
                link = link_tag['href']
                title = g.find('h3').text if g.find('h3') else "LinkedIn Post"

                # Ensure it's a real LinkedIn post and not a repeat
                if "linkedin.com" in link and "/posts/" in link and link not in found_links:
                    found_links.add(link)
                    send_to_telegram(title, link)
            
            # Prevent Google from flagging your GitHub runner
            time.sleep(random.uniform(5, 10))
            
        except Exception as e:
            print(f"Search failed for query: {e}")

if __name__ == "__main__":
    print("🚀 Hunting for LinkedIn Posts from the last 7 days...")
    hunt_linkedin_posts()
