import requests
from bs4 import BeautifulSoup
import os
import time

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Keywords
TECH = '("RTL" OR "Physical Design" OR "ASIC" OR "Hardware")'
EXP = '("Fresher" OR "0 years" OR "Trainee" OR "New Grad")'

def send_to_telegram(category, title, link):
    message = (
        f"🎯 *MATCHED ALERT: {category}*\n\n"
        f"📌 *Details:* {title}\n"
        f"🔗 [VIEW ON LINKEDIN]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
        time.sleep(2) # SLOW is safe.
    except: pass

def run_google_bridge_scan():
    """Uses Google to find LinkedIn Jobs/Posts LinkedIn is hiding."""
    # We search the past week (qdr:w) to ensure we find results
    # We search specifically for the LinkedIn Jobs and Posts directories
    queries = [
        f'site:linkedin.com/jobs/view {TECH} {EXP} "India"',
        f'site:linkedin.com/posts/ {TECH} {EXP} "India" "hiring"'
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    for query in queries:
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbs=qdr:w"
        
        try:
            response = requests.get(search_url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Google search results are usually in 'div.g'
            for result in soup.find_all('div', class_='g'):
                link_tag = result.find('a')
                if not link_tag: continue
                
                link = link_tag['href']
                title = result.find('h3').text if result.find('h3') else "LinkedIn Opening"
                
                # Filter out garbage
                if "linkedin.com" in link:
                    category = "JOB" if "/jobs/" in link else "POST"
                    send_to_telegram(category, title, link)
            
            time.sleep(5) # Delay between Google searches to stay safe
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_google_bridge_scan()
