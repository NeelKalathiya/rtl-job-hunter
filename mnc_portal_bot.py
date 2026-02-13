import requests
from bs4 import BeautifulSoup
import os
import time

BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Targeted MNC subdomains for India
MNC_SITES = '(site:intel.com/content/www/in OR site:nvidia.com/en-in OR site:qualcomm.com/company/careers OR site:ti.com/careers)'
KEYWORDS = '("RTL" OR "Physical Design" OR "ASIC") AND (Trainee OR Fresher OR "0 years")'

def get_mnc_jobs():
    query = f"{MNC_SITES} {KEYWORDS}"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbs=qdr:d"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='g')
        
        count = 0
        for res in results:
            if count >= 10: break # STRICT LIMIT: 10 messages
            
            link = res.find('a')['href']
            text = res.text
            
            # Logic to extract a likely Job ID (usually 5-8 digits)
            import re
            job_id_match = re.search(r'\b\d{5,8}\b', text)
            job_id = job_id_match.group(0) if job_id_match else "Check Link"
            
            # Extract company name from URL
            company = "MNC"
            for c in ["Intel", "NVIDIA", "Qualcomm", "Texas Instruments"]:
                if c.lower() in link.lower(): company = c
            
            msg = f"🏢 *MNC:* {company}\n🆔 *Job ID:* {job_id}\n🔗 [Apply Directly]({link})"
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                          json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
            count += 1
            time.sleep(1) # Safety delay
    except:
        pass

if __name__ == "__main__":
    get_mnc_jobs()
