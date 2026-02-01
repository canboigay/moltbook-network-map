#!/usr/bin/env python3
"""
Try accessing different pages of agents via URL parameters
"""

from playwright.sync_api import sync_playwright
import time

urls_to_try = [
    "https://www.moltbook.com/u?page=2",
    "https://www.moltbook.com/u?offset=60",
    "https://www.moltbook.com/u?skip=60",
    "https://www.moltbook.com/u?limit=200",
    "https://www.moltbook.com/u?page=1&limit=200",
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for url in urls_to_try:
        print(f"\nTrying: {url}")
        page.goto(url, timeout=15000)
        time.sleep(3)
        
        # Count agents
        links = page.query_selector_all('a[href^="/u/"]')
        agents = set()
        for link in links:
            href = link.get_attribute('href')
            if href and href != '/u':
                agents.add(href.replace('/u/', ''))
        
        print(f"  Found {len(agents)} agents")
        if agents:
            print(f"  Sample: {list(agents)[:5]}")
    
    browser.close()
