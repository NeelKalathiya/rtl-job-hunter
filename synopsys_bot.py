import requests
from bs4 import BeautifulSoup
import os
import time

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Synopsys India Interns/Temp category URL
SYNOPSYS_URL = "https://careers.synopsys.com/category/interns-temp-jobs/44408/8675664/1"

def send_to_telegram(job_title, job_id, link):
    message = (
        f"💎 *NEW SYNOPSYS INTERN OPENING*\n\n"
        f"📌 *Position:* {job_title}\n"
        f"🆔 *Job ID:* {job_id}\n"
        f"📍 *Location:* India\n"
        f"🔗 [Apply on Synopsys Portal]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Error: {e}")

def scrape_synopsys():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(SYNOPSYS_URL, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Synopsys uses section/article blocks for jobs
        job_sections = soup.find_all('section', id='search-results-list')
        if not job_sections:
            return

        # Look for individual job entries
        jobs = soup.find_all('li')
        
        for job in jobs:
            text = job.get_text()
            # Only process if it's an Indian opening
            if "India" in text:
                try:
                    title_elem = job.find('h2')
                    title = title_elem.text.strip() if title_elem else "Internship Position"
                    
                    # Extract Job ID (usually 5 digits in Synopsys listings)
                    import re
                    job_id_match = re.search(r'Job ID:\s*(\d+)', text)
                    job_id = job_id_match.group(1) if job_id_match else "N/A"
                    
                    link_elem = job.find('a')
                    link = "https://careers.synopsys.com" + link_elem['href'] if link_elem else SYNOPSYS_URL
                    
                    send_to_telegram(title, job_id, link)
                    time.sleep(2) # Safety delay
                except:
                    continue
                    
    except Exception as e:
        print(f"Scrape Error: {e}")

if __name__ == "__main__":
    scrape_synopsys()
