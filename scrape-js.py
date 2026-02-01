#!/usr/bin/env python3
"""
Scrape Moltbook with proper JavaScript rendering
"""

import json
import time

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    import subprocess
    subprocess.run(["pip3", "install", "playwright"], check=True)
    subprocess.run(["playwright", "install", "chromium"], check=True)
    from playwright.sync_api import sync_playwright

def scrape_homepage():
    print("🕸️  Scraping Moltbook with JavaScript rendering")
    print("=" * 50)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Go to homepage with shorter timeout
        print("\n📊 Loading homepage...")
        page.goto("https://www.moltbook.com", timeout=15000)
        
        # Wait for content to load
        print("⏳ Waiting for content to render...")
        time.sleep(5)
        
        # Get all the text
        content = page.content()
        
        # Find agent links
        agent_links = page.query_selector_all('a[href^="/u/"]')
        agents = []
        
        for link in agent_links:
            try:
                href = link.get_attribute('href')
                text = link.inner_text()
                if href:
                    agent_name = href.replace('/u/', '')
                    if agent_name and agent_name not in agents:
                        agents.append(agent_name)
                        print(f"  Found: {agent_name}")
            except:
                pass
        
        # Also try finding by text content
        all_links = page.query_selector_all('a')
        for link in all_links:
            try:
                href = link.get_attribute('href')
                if href and '/u/' in href:
                    agent_name = href.split('/u/')[-1]
                    if agent_name and agent_name not in agents:
                        agents.append(agent_name)
                        print(f"  Found: {agent_name}")
            except:
                pass
        
        browser.close()
    
    print(f"\n✓ Found {len(agents)} agents total")
    
    # Save results
    data = {
        'agents': agents,
        'count': len(agents),
        'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('scraped-agents.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Saved to scraped-agents.json")
    
    return agents

if __name__ == '__main__':
    scrape_homepage()
