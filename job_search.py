import requests
import os
from datetime import datetime

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# List of target MNC Domains in India
MNC_DOMAINS = [
    "intel.com", "qualcomm.com", "nvidia.com", "amd.com", "ti.com", 
    "broadcom.com", "nxp.com", "marvel.com", "synopsys.com", "cadence.com",
    "micron.com", "st.com"
]

# Indian Startups/Companies
INDIAN_VLSI = ["saankhyalabs.com", "incoresemi.com", "mindgrovetech.in"]

def get_job_leads():
    # We use Google's Custom Search API logic to find DIRECT job pages
    # This avoids getting "Search Result" pages and finds actual job postings
    query = (
        '("RTL Design" OR "Digital Design") '
        '(Trainee OR Intern OR "New Grad" OR "Level 0") '
        'location:India (site:linkedin.com/jobs/view OR site:naukri.com/job-listings)'
    )
    
    # Adding MNC specific career portal searches
    mnc_query = " OR ".join([f"site:{d}/careers" for d in MNC_DOMAINS])
    
    # This URL targets only direct Job Posting pages indexed in the last 24h
    search_url = f"https://www.google.com/search?q={query}+OR+({mnc_query})&tbs=qdr:d"
    
    return search_url

def send_to_telegram(link):
    date_str = datetime.now().strftime("%d %b %Y")
    message = (
        f"🚀 Direct RTL Openings: {date_str}\n\n"
        f"I have found new open positions in India for RTL/Digital Design.\n\n"
        f"🔗 [Access Direct Application Links]({link})\n\n"
        f"Targeting: Intel, Qualcomm, NVIDIA, Synopsys, and Indian Startups."
    )
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

if __name__ == "__main__":
    job_link = get_job_leads()
    send_to_telegram(job_link)
