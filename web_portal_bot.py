import requests
from bs4 import BeautifulSoup
import os
import time

BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Your Hardware Keywords
TECH = '("RTL" OR "Physical Design" OR "ASIC" OR "Hardware")'
EXP = '("Fresher" OR "0 years" OR "Trainee" OR "New Grad")'

def send_to_telegram(category, company, title, link):
    """Sends each finding as a separate, clear message."""
    icon = "🌐" if category == "Job" else "📣"
    message = (
        f"{icon} *Type:* {category}\n"
        f"🏢 *Company:* {company}\n"
        f"📌 *Role/Post:* {title}\n"
        f"🔗 [VIEW ON LINKEDIN]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
    time.sleep(1.5) # Protects your bot from Telegram spam limits

def search_linkedin_posts():
    """Engine 1: Scans for public LinkedIn POSTS (Hiring Alerts)."""
    # This query targets individual post pages in India
    query = f'site:linkedin.com/posts/ {TECH} {EXP} "India" "hiring"'
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbs=qdr:d"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        res = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        results = soup.find_all('div', class_='g')
        
        count = 0
        for r in results:
            if count >= 5: break # Limit to top 5 posts to avoid spam
            title = r.find('h3').text[:50] + "..." if r.find('h3') else "LinkedIn Post"
            link = r.find('a')['href']
            send_to_telegram("Post Alert", "LinkedIn User", title, link)
            count += 1
    except: pass

def scrape_linkedin_jobs():
    """Engine 2: Scans the LinkedIn Jobs API."""
    li_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={TECH.replace(' ', '%20')}%20{EXP.replace(' ', '%20')}&location=India&f_TPR=r86400"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        res = requests.get(li_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        cards = soup.find_all('li')
        
        count = 0
        for card in cards:
            if count >= 5: break 
            title = card.find('h3', class_='base-search-card__title').text.strip()
            company = card.find('h4', class_='base-search-card__subtitle').text.strip()
            link = card.find('a', class_='base-card__full-link')['href'].split('?')[0]
            send_to_telegram("Job", company, title, link)
            count += 1
    except: pass

if __name__ == "__main__":
    print("Starting Post and Job Scan...")
    search_linkedin_posts()
    scrape_linkedin_jobs()
