import requests
import os
from datetime import datetime

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Technical Domains & Level
TECH = '("RTL" OR "Physical Design" OR "ASIC" OR "Hardware")'
LEVEL = '("Fresher" OR "0 years" OR "New Grad" OR "Trainee")'

def send_to_telegram(company_name, link):
    message = (
        f"🏢 *Company: {company_name}*\n"
        f"🚀 [View Direct {company_name} India Openings]({link})\n"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

def run_company_portal_scan():
    # Targeted search strings for specific MNC portals in India
    # Using 'tbs=qdr:d' for results in the last 24 hours
    
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

    for name, query in companies.items():
        # This creates a direct link to the filtered search for THAT company only
        direct_link = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbs=qdr:d"
        send_to_telegram(name, direct_link)

if __name__ == "__main__":
    run_company_portal_scan()
