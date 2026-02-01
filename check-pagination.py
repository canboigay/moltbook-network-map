#!/usr/bin/env python3
"""
Check if Moltbook has pagination
"""

from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.goto("https://www.moltbook.com/u", timeout=20000)
    time.sleep(8)
    
    # Take screenshot
    page.screenshot(path="pagination-check.png", full_page=True)
    print("Screenshot saved to pagination-check.png")
    
    # Look for pagination elements
    pagination_keywords = ['next', 'previous', 'page', 'more', 'load']
    
    all_buttons = page.query_selector_all('button')
    print(f"\nFound {len(all_buttons)} buttons:")
    for btn in all_buttons:
        text = btn.inner_text().lower()
        if any(kw in text for kw in pagination_keywords):
            print(f"  - Button: '{text}'")
    
    # Check for numbered pagination
    page_numbers = page.query_selector_all('a[href*="page="], button[href*="page="]')
    if page_numbers:
        print(f"\nFound {len(page_numbers)} page number links")
    
    # Check URL params
    url = page.url
    print(f"\nCurrent URL: {url}")
    
    # Look for "Load More" or similar
    html = page.content()
    if 'load' in html.lower():
        print("\n'Load' found in HTML")
    if 'next' in html.lower():
        print("'Next' found in HTML")
    if 'page' in html.lower():
        print("'Page' found in HTML")
    
    browser.close()
