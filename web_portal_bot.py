def search_linkedin_posts():
    """Engine 1: Scans for public LinkedIn POSTS with broader filters."""
    # 1. Broadened keywords to catch more 'Hiring' posts
    # 2. Changed filter to 'tbs=qdr:w' (Last Week) to find more than 1 result
    query = f'site:linkedin.com/posts/ ("Hiring" OR "Opening") AND {TECH} AND {EXP} AND "India"'
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbs=qdr:w"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        results = soup.find_all('div', class_='g')
        
        count = 0
        for r in results:
            if count >= 10: # Increased limit to 10 per your request
                break 
            
            title_element = r.find('h3')
            link_element = r.find('a')
            
            if title_element and link_element:
                title = title_element.text[:60] + "..."
                link = link_element['href']
                send_to_telegram("Post Alert", "LinkedIn User", title, link)
                count += 1
    except Exception as e:
        print(f"Post Search Error: {e}")
