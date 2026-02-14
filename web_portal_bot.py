import requests
from bs4 import BeautifulSoup
import os
import time

BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def scrape_web_portals():
    # LinkedIn Guest API for India Hardware roles
    li_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=RTL%20Design%20Trainee&location=India&f_TPR=r86400"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        res = requests.get(li_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        cards = soup.find_all('li')
        
        count = 0
        for card in cards:
            if count >= 10: break # STRICT LIMIT: 10 messages
            
            title = card.find('h3', class_='base-search-card__title').text.strip()
            company = card.find('h4', class_='base-search-card__subtitle').text.strip()
            link = card.find('a', class_='base-card__full-link')['href'].split('?')[0]
            
            msg = f"🌐 *Portal:* LinkedIn/Naukri\n🏢 *Company:* {company}\n📌 *Role:* {title}\n🔗 [Apply Link]({link})"
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                          json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
            count += 1
            time.sleep(1)
    except:
        pass
    def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    try:
        response = requests.post(url, json=payload)
        # This will show you exactly why it failed in GitHub Actions
        if response.status_code != 200:
            print(f"❌ Telegram Error {response.status_code}: {response.text}")
        else:
            print(f"✅ Message sent successfully!")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
if __name__ == "__main__":
    scrape_web_portals()
