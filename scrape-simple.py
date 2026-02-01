#!/usr/bin/env python3
"""
Simple scraper for Moltbook - just get what we can
"""

import requests
from bs4 import BeautifulSoup
import json

def scrape_with_requests():
    """Try simple HTTP request first"""
    
    print("🕸️  Scraping Moltbook (simple method)")
    print("=" * 50)
    
    # Try homepage
    print("\n📊 Checking homepage...")
    resp = requests.get("https://www.moltbook.com", timeout=10)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Find agent links
    agent_links = soup.find_all('a', href=True)
    agents = set()
    
    for link in agent_links:
        href = link.get('href', '')
        if href.startswith('/u/'):
            agent_name = href.replace('/u/', '')
            if agent_name:
                agents.add(agent_name)
    
    print(f"Found {len(agents)} agents in HTML: {list(agents)[:10]}")
    
    # Check known agents
    known = ['AgentDroverland', 'SimeonsClaw', 'SimeonAgent', 'NetworkMapper']
    
    nodes = []
    for agent in known:
        print(f"Checking {agent}...")
        try:
            resp = requests.get(f"https://www.moltbook.com/u/{agent}", timeout=5)
            if resp.status_code == 200:
                nodes.append({
                    'id': agent,
                    'username': agent,
                    'exists': True,
                    'status_code': resp.status_code
                })
                print(f"  ✓ {agent} exists")
        except Exception as e:
            print(f"  ✗ {agent}: {e}")
    
    # Save what we found
    data = {
        'nodes': nodes,
        'edges': [],
        'metadata': {
            'method': 'simple_http_scrape',
            'agents_in_html': list(agents),
            'verified_agents': len(nodes)
        }
    }
    
    with open('simple-scrape.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Found {len(nodes)} verified agents")
    print(f"✓ Saved to simple-scrape.json")

if __name__ == '__main__':
    scrape_with_requests()
