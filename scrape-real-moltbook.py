#!/usr/bin/env python3
"""
Scrape the real Moltbook website to build network visualization
Uses Playwright to handle JavaScript-rendered content
"""

import json
import time
from collections import defaultdict

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Installing playwright...")
    import subprocess
    subprocess.run(["pip3", "install", "playwright"], check=True)
    subprocess.run(["playwright", "install", "chromium"], check=True)
    from playwright.sync_api import sync_playwright

def scrape_agent_profile(page, agent_name):
    """Scrape an individual agent profile"""
    url = f"https://www.moltbook.com/u/{agent_name}"
    
    try:
        page.goto(url, wait_until="networkidle", timeout=10000)
        time.sleep(2)  # Let content load
        
        # Extract agent info
        agent_data = {
            'username': agent_name,
            'posts': [],
            'followers': 0,
            'following': 0,
            'karma': 0
        }
        
        # Try to find stats
        content = page.content()
        
        # Look for post titles/links
        posts = page.query_selector_all('a[href^="/post/"]')
        agent_data['posts'] = [p.get_attribute('href') for p in posts[:10]]
        
        print(f"  {agent_name}: {len(agent_data['posts'])} posts found")
        return agent_data
        
    except Exception as e:
        print(f"  Error scraping {agent_name}: {e}")
        return None

def scrape_homepage(page):
    """Scrape homepage for agent list"""
    url = "https://www.moltbook.com"
    
    page.goto(url, wait_until="networkidle")
    time.sleep(3)
    
    agents = []
    
    # Try to find agent links
    agent_links = page.query_selector_all('a[href^="/u/"]')
    
    for link in agent_links:
        href = link.get_attribute('href')
        if href and href.startswith('/u/'):
            agent_name = href.replace('/u/', '')
            if agent_name and agent_name not in agents:
                agents.append(agent_name)
    
    print(f"Found {len(agents)} agents on homepage")
    return agents

def main():
    print("🕸️  Scraping Real Moltbook Network")
    print("=" * 50)
    
    all_agents = set()
    nodes = []
    edges = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("\n📊 Scraping homepage...")
        homepage_agents = scrape_homepage(page)
        all_agents.update(homepage_agents)
        
        # Also try known agents
        known_agents = ['AgentDroverland', 'SimeonsClaw', 'SimeonAgent']
        all_agents.update(known_agents)
        
        print(f"\n👥 Scraping {len(all_agents)} agent profiles...")
        
        for agent_name in list(all_agents)[:20]:  # Limit to 20 for now
            agent_data = scrape_agent_profile(page, agent_name)
            
            if agent_data:
                nodes.append({
                    'id': agent_name,
                    'username': agent_name,
                    'posts_count': len(agent_data['posts']),
                    'karma': agent_data.get('karma', 0)
                })
        
        browser.close()
    
    # Save data
    network_data = {
        'nodes': nodes,
        'edges': edges,
        'metadata': {
            'total_agents': len(nodes),
            'total_connections': len(edges),
            'data_source': 'real_moltbook_website_scrape',
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
    }
    
    with open('real-moltbook-data.json', 'w') as f:
        json.dump(network_data, f, indent=2)
    
    print(f"\n✓ Scraped {len(nodes)} agents")
    print(f"✓ Saved to real-moltbook-data.json")
    
    # Top agents
    top = sorted(nodes, key=lambda x: x['posts_count'], reverse=True)[:10]
    print(f"\n📊 Top Agents by Posts:")
    for i, agent in enumerate(top, 1):
        print(f"  {i}. {agent['username']}: {agent['posts_count']} posts")

if __name__ == '__main__':
    main()
