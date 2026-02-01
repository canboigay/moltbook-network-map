#!/usr/bin/env python3
"""
Aggressively scrape as many agents as possible from Moltbook
"""

from playwright.sync_api import sync_playwright
import json
import time

def scrape_agents_aggressive(target=5000):
    print(f"🕸️  Aggressive Moltbook Agent Scraper (target: {target})")
    print("=" * 50)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Loading agent directory...")
        page.goto("https://www.moltbook.com/u", timeout=30000)
        time.sleep(5)
        
        agents = set()
        last_count = 0
        no_change_count = 0
        
        # Try aggressive scrolling
        for scroll_num in range(200):  # Try up to 200 scrolls
            # Scroll to bottom
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(0.5)
            
            # Also try scrolling by pixels
            page.evaluate('window.scrollBy(0, 1000)')
            time.sleep(0.5)
            
            # Extract agents
            all_links = page.query_selector_all('a[href^="/u/"]')
            for link in all_links:
                href = link.get_attribute('href')
                if href and href != '/u':
                    agent = href.replace('/u/', '')
                    if agent:
                        agents.add(agent)
            
            current_count = len(agents)
            
            if current_count > last_count:
                print(f"  Scroll {scroll_num + 1}: {current_count} agents")
                last_count = current_count
                no_change_count = 0
            else:
                no_change_count += 1
            
            # Stop if no new agents in 10 scrolls
            if no_change_count >= 10:
                print(f"  No new agents after {no_change_count} scrolls, stopping...")
                break
            
            # Stop if we hit our target
            if current_count >= target:
                print(f"  Reached target of {target} agents!")
                break
            
            # Try clicking "Load More" button if it exists
            try:
                load_more = page.query_selector('button:has-text("Load More")')
                if load_more:
                    load_more.click()
                    print("  Clicked 'Load More' button")
                    time.sleep(2)
            except:
                pass
        
        print(f"\n✓ Total agents scraped: {len(agents)}")
        
        # Try different tabs/filters
        print("\nTrying different filters...")
        
        # Try "Recent" tab
        try:
            recent_btn = page.query_selector('button:has-text("Recent")')
            if recent_btn:
                recent_btn.click()
                time.sleep(3)
                
                for _ in range(20):
                    page.evaluate('window.scrollBy(0, 1000)')
                    time.sleep(0.3)
                
                all_links = page.query_selector_all('a[href^="/u/"]')
                for link in all_links:
                    href = link.get_attribute('href')
                    if href and href != '/u':
                        agent = href.replace('/u/', '')
                        if agent:
                            agents.add(agent)
                
                print(f"  After Recent tab: {len(agents)} agents")
        except Exception as e:
            print(f"  Recent tab error: {e}")
        
        # Try "Karma" tab
        try:
            karma_btn = page.query_selector('button:has-text("Karma")')
            if karma_btn:
                karma_btn.click()
                time.sleep(3)
                
                for _ in range(20):
                    page.evaluate('window.scrollBy(0, 1000)')
                    time.sleep(0.3)
                
                all_links = page.query_selector_all('a[href^="/u/"]')
                for link in all_links:
                    href = link.get_attribute('href')
                    if href and href != '/u':
                        agent = href.replace('/u/', '')
                        if agent:
                            agents.add(agent)
                
                print(f"  After Karma tab: {len(agents)} agents")
        except Exception as e:
            print(f"  Karma tab error: {e}")
        
        browser.close()
    
    agents_list = sorted(list(agents))
    
    print(f"\n✅ Final count: {len(agents_list)} agents")
    
    # Save
    data = {
        'agents': agents_list,
        'count': len(agents_list),
        'total_registered': '1,516,273+',
        'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'method': 'aggressive_scroll_with_tabs'
    }
    
    with open('moltbook-agents-full.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Saved to moltbook-agents-full.json")
    
    return agents_list

if __name__ == '__main__':
    agents = scrape_agents_aggressive(target=5000)
    print(f"\nSample agents: {agents[:30]}")
