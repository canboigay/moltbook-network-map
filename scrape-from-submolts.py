#!/usr/bin/env python3
"""
Scrape agents from different submolts (communities)
Each submolt might have different active members
"""

from playwright.sync_api import sync_playwright
import json
import time

def scrape_submolt_page(page):
    """Scrape list of submolts"""
    print("Getting submolt list...")
    page.goto("https://www.moltbook.com/m", timeout=20000)
    time.sleep(5)
    
    # Find submolt links
    links = page.query_selector_all('a[href^="/m/"]')
    submolts = set()
    
    for link in links:
        href = link.get_attribute('href')
        if href and href != '/m':
            submolt = href.replace('/m/', '')
            if submolt:
                submolts.add(submolt)
    
    print(f"Found {len(submolts)} submolts")
    return list(submolts)

def scrape_submolt_members(page, submolt):
    """Get agents who posted in a submolt"""
    print(f"\n  Checking m/{submolt}...")
    url = f"https://www.moltbook.com/m/{submolt}"
    
    try:
        page.goto(url, timeout=15000)
        time.sleep(3)
        
        # Find author links in posts
        author_links = page.query_selector_all('a[href^="/u/"]')
        agents = set()
        
        for link in author_links:
            href = link.get_attribute('href')
            if href and href != '/u':
                agent = href.replace('/u/', '')
                if agent:
                    agents.add(agent)
        
        print(f"    Found {len(agents)} agents in m/{submolt}")
        return agents
        
    except Exception as e:
        print(f"    Error: {e}")
        return set()

def main():
    print("🕸️  Scraping Agents from Submolts")
    print("=" * 50)
    
    all_agents = set()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Get submolt list
        submolts = scrape_submolt_page(page)
        
        # Check each submolt
        for submolt in submolts[:20]:  # Check first 20
            agents = scrape_submolt_members(page, submolt)
            all_agents.update(agents)
            print(f"    Total unique agents: {len(all_agents)}")
            time.sleep(1)
        
        browser.close()
    
    agents_list = sorted(list(all_agents))
    
    print(f"\n✅ Total agents from submolts: {len(agents_list)}")
    
    # Save
    data = {
        'agents': agents_list,
        'count': len(agents_list),
        'method': 'submolt_scraping',
        'submolts_checked': submolts[:20]
    }
    
    with open('submolt-agents.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Saved to submolt-agents.json")
    print(f"\nSample: {agents_list[:20]}")

if __name__ == '__main__':
    main()
