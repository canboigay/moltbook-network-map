#!/usr/bin/env python3
"""
Debug what's actually on the Moltbook homepage
"""

from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    print("Loading page...")
    page.goto("https://www.moltbook.com", timeout=20000)
    
    print("Waiting 10 seconds for content...")
    time.sleep(10)
    
    # Take screenshot
    page.screenshot(path="moltbook-homepage.png")
    print("Screenshot saved to moltbook-homepage.png")
    
    # Get all text
    text = page.inner_text('body')
    print(f"\nPage text preview:")
    print(text[:500])
    
    # Find all links
    all_links = page.query_selector_all('a')
    print(f"\nFound {len(all_links)} links")
    
    hrefs = []
    for link in all_links[:20]:
        href = link.get_attribute('href')
        if href:
            hrefs.append(href)
    
    print("First 20 hrefs:", hrefs)
    
    browser.close()
    print("\nDone!")
