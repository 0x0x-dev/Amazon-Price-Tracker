import requests
from bs4 import BeautifulSoup
import re

def get_amazon_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Try multiple price selectors
    price_selectors = [
        '.a-price-whole',
        '.a-price .a-offscreen',
        '#priceblock_dealprice',
        '#priceblock_ourprice',
        '.a-price-range'
    ]
    
    price = None
    for selector in price_selectors:
        price = soup.select_one(selector)
        if price:
            break
    
    title = soup.select_one('#productTitle')
    
    def clean_price(price_text):
        if not price_text:
            return None
        
        # Remove Arabic text, Unicode markers, and common currency symbols
        cleaned = re.sub(r'[^\d.,]', '', price_text)  # Keep only digits, dots, and commas
        cleaned = cleaned.replace(',', '')  # Remove commas
        
        try:
            return float(cleaned)
        except ValueError:
            return None
    
    return {
        'title': title.text.strip() if title else 'Unknown Product',
        'price': clean_price(price.text) if price else None
    }
