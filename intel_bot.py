import requests
import os
import time
import re

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Intel India Workday API URL with filters for Student/Intern and College Graduate
# Filter parameters: Location: India, Job Type: Student/Intern & College Graduate
INTEL_API_URL = "https://intel.wd1.myworkdayjobs.com/wday/cxs/intel/External/jobs"

def send_to_telegram(job_title, job_id, link):
    message = (
        f"💙 *NEW INTEL INDIA OPENING*\n\n"
        f"📌 *Position:* {job_title}\n"
        f"🆔 *Job ID:* {job_id}\n"
        f"🎓 *Type:* Student / Intern / New Grad\n"
        f"🔗 [Apply on Intel Portal]({link})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Telegram Error: {e}")

def scrape_intel():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Workday payload to filter for India + Early Career Job Types
    payload = {
        "appliedFacets": {
            "locationCountry": ["bc33aa3152ec42d4995f4791a106ed09"], # India
            "jobFamilyGroup": [
                "6042070b79e01001f04fa9b468070000", # Student/Intern
                "6042070b79e01001f04f464098900000"  # College Graduate
            ]
        },
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }
    
    try:
        response = requests.post(INTEL_API_URL, headers=headers, json=payload, timeout=20)
        data = response.json()
        
        jobs = data.get('jobPostings', [])
        for job in jobs:
            title = job.get('title')
            job_id = job.get('bulletFields', [None])[0] # Usually contains the JR number
            path = job.get('externalPath')
            full_link = f"https://intel.wd1.myworkdayjobs.com/External{path}"
            
            if title and full_link:
                send_to_telegram(title, job_id, full_link)
                time.sleep(1.5) # Safety delay
                
    except Exception as e:
        print(f"Intel Scrape Error: {e}")

if __name__ == "__main__":
    scrape_intel()
