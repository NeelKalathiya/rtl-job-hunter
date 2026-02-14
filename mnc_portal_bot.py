import requests
from bs4 import BeautifulSoup
import os
import time
import re # Added for Job ID extraction

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Technical Domains & Level
TECH = '("RTL" OR "Physical Design" OR "ASIC" OR "Hardware")'
LEVEL = '("Fresher" OR "0 years" OR "New Grad" OR "Trainee")'

def send_to_telegram(company_name, job_id, link):
    # This now includes the Job ID in the message
    message = (
        f"🏢 *Company: {company_name}*\n"
        f"🆔 *Job ID:* {job_id}\n"
        f"🚀 [View Direct {company_name} India Openings]({link})\n"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

def run_company_portal_scan():
    # Targeted search strings for specific MNC portals in India
    companies = {
        "Intel": f"site:intel.com {TECH} {LEVEL} India",
        "NVIDIA": f"site:nvidia.com {TECH} {LEVEL} India",
        "Qualcomm": f"site:qualcomm.com {TECH} {LEVEL} India",
        "AMD": f"site:amd.com {TECH} {LEVEL} India",
        "Synopsys": f"site:synopsys.com {TECH} {LEVEL} India",
        "Cadence": f"site:cadence.com {TECH} {LEVEL} India",
        "Texas Instruments": f"site:ti.com {TECH} {LEVEL} India",
        "Micron": f"site:micron.com {TECH} {LEVEL} India"
    }

    headers = {"User-Agent": "Mozilla/5.0"}
    
    for name, query in companies.items():
        # Google search for the last 24 hours
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbs=qdr:d"
        
        try:
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look at the first search result to try and find a Job ID
            first_result = soup.find('div', class_='g')
            job_id = "Check Link"
            
            if first_result:
                # Search for a 5-8 digit number in the text
                match = re.search(r'\b\d{5,8}\b', first_result.text)
                if match:
                    job_id = match.group(0)
            
            send_to_telegram(name, job_id, search_url)
            time.sleep(1.5) # Prevent Telegram spam block
            
        except Exception as e:
            print(f"Error scanning {name}: {e}")

if __name__ == "__main__":
    run_company_portal_scan()
