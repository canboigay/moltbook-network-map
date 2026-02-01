#!/usr/bin/env python3
"""
Scrape as many agents as possible from Moltbook by scrolling
"""

from playwright.sync_api import sync_playwright
import json
import time

def scrape_agents(max_agents=500):
    print(f"🕸️  Scraping Moltbook Agents (target: {max_agents})")
    print("=" * 50)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Loading agent directory...")
        page.goto("https://www.moltbook.com/u", timeout=20000)
        time.sleep(5)
        
        agents = set()
        last_count = 0
        scroll_attempts = 0
        max_scrolls = 50
        
        while len(agents) < max_agents and scroll_attempts < max_scrolls:
            # Find all agent links
            all_links = page.query_selector_all('a[href^="/u/"]')
            
            for link in all_links:
                href = link.get_attribute('href')
                if href and href != '/u':
                    agent_name = href.replace('/u/', '')
                    if agent_name:
                        agents.add(agent_name)
            
            new_count = len(agents)
            if new_count > last_count:
                print(f"  Agents found: {new_count}")
                last_count = new_count
            
            # Scroll down to load more
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1)
            scroll_attempts += 1
            
            # Check if we're still loading new agents
            if scroll_attempts > 10 and new_count == last_count:
                print("  No new agents loading, stopping...")
                break
        
        browser.close()
    
    agents_list = sorted(list(agents))
    
    print(f"\n✓ Total agents scraped: {len(agents_list)}")
    
    # Save to file
    data = {
        'agents': agents_list,
        'count': len(agents_list),
        'total_registered': '1,516,273',
        'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('moltbook-agents-full.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Saved to moltbook-agents-full.json")
    print(f"\nFirst 20 agents: {agents_list[:20]}")
    
    return agents_list

if __name__ == '__main__':
    scrape_agents(max_agents=1000)
