import os
import requests
from datetime import datetime

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# 1. Technical Domain Keywords
DOMAINS = '("RTL Design" OR "Physical Design" OR "ASIC" OR "Hardware Design" OR "Digital Design")'

# 2. Experience Level Keywords
LEVELS = '("0 years experience" OR "Fresher" OR "New Grad" OR "Trainee" OR "Entry Level")'

# 3. Location and Platform Filters
# This query tells Google to find DIRECT job pages in India on multiple portals
QUERY = f'{DOMAINS} AND {LEVELS} AND location:India (site:naukri.com/job-listings OR site:linkedin.com/jobs/view OR site:indeed.com/viewjob OR site:workday.com)'

def run_broad_search():
    # We use a 24-hour filter (tbs=qdr:d) to get only today's openings
    search_url = f"https://www.google.com/search?q={QUERY.replace(' ', '+')}&tbs=qdr:d"
    
    date_str = datetime.now().strftime("%d %b %Y")
    
    message = (
        f"🎯 *New Hardware/VLSI Openings: {date_str}*\n\n"
        f"Checked for: RTL, Physical Design, ASIC, and Hardware roles.\n"
        f"Filters: 0 Exp / Freshers / India.\n\n"
        f"🚀 [View Direct Application Links]({search_url})\n\n"
        f"_Platforms: LinkedIn, Naukri, Indeed, and MNC Career Portals._"
    )
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_broad_search()
