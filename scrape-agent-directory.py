#!/usr/bin/env python3
"""
Scrape the /u (agent directory) page on Moltbook
"""

from playwright.sync_api import sync_playwright
import json
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    print("Loading agent directory...")
    page.goto("https://www.moltbook.com/u", timeout=20000)
    
    print("Waiting for agents to load...")
    time.sleep(10)
    
    # Take screenshot
    page.screenshot(path="agent-directory.png")
    
    # Get page text
    text = page.inner_text('body')
    print(f"\nPage content preview:")
    print(text[:1000])
    
    # Find agent links
    agent_links = []
    all_links = page.query_selector_all('a')
    
    for link in all_links:
        href = link.get_attribute('href')
        if href and '/u/' in href and href != '/u':
            agent_name = href.replace('/u/', '')
            if agent_name and agent_name not in agent_links:
                agent_links.append(agent_name)
    
    print(f"\n✓ Found {len(agent_links)} agents")
    print(f"Agents: {agent_links[:20]}")
    
    # Save
    with open('agent-directory.json', 'w') as f:
        json.dump({'agents': agent_links, 'count': len(agent_links)}, f, indent=2)
    
    browser.close()
    print("\nSaved to agent-directory.json")
