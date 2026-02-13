import requests
import os
from datetime import datetime

# Environment Variables from GitHub Secrets
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Targeted Search for MNCs and LinkedIn
MNC_SITES = '(site:intel.com OR site:qualcomm.com OR site:nvidia.com OR site:amd.com OR site:ti.com OR site:nxp.com OR site:marvel.com OR site:synopsys.com OR site:cadence.com OR site:micron.com)'
LINKEDIN_QUERY = '(site:linkedin.com/jobs/ OR site:linkedin.com/posts/)'

# Advanced RTL Keywords
ROLES = '("RTL Design" OR "Digital Design" OR "ASIC Design" OR "VLSI")'
LEVELS = '(Trainee OR Intern OR "Early Career" OR "New Grad" OR "Level 0")'

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def run_scan():
    # Constructing Google Search URLs with a 24-hour time filter (tbs=qdr:d)
    mnc_link = f"https://www.google.com/search?q={MNC_SITES}+{ROLES}+{LEVELS}&tbs=qdr:d"
    li_link = f"https://www.google.com/search?q={LINKEDIN_QUERY}+{ROLES}+{LEVELS}&tbs=qdr:d"
    
    date_now = datetime.now().strftime("%d %b %Y")
    alert_text = (
        f"🔍 RTL Job Scan: {date_now}\n\n"
        f"🏢 Top MNC Career Pages (24h):\n[Click to View]({mnc_link})\n\n"
        f"🔗 LinkedIn Posts & Jobs (24h):\n[Click to View]({li_link})\n\n"
        f"🚀 Apply fast - New Grad roles fill up quickly!"
    )
    send_to_telegram(alert_text)

if _name_ == "_main_":
    run_scan()
