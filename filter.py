# filter.py
from html.parser import HTMLParser
import re

class HTMLCleaner(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
        
    def handle_data(self, data):
        self.fed.append(data)
        
    def get_data(self):
        return ''.join(self.fed)

def clean_html(html):
    # Remove CSS
    css_pattern = re.compile(r'<style.*?>.*?</style>', re.DOTALL)
    html = re.sub(css_pattern, '', html)

    # Remove script
    script_pattern = re.compile(r'<script.*?>.*?</script>', re.DOTALL)
    html = re.sub(script_pattern, '', html)
    
    # Remove images
    img_pattern = re.compile(r'<img.*?>', re.DOTALL)
    html = re.sub(img_pattern, '', html)
    
    # Remove the subject line explicitly, if it exists in the message body
    subject_pattern = re.compile(r'Subject:\s*.*?\n', re.IGNORECASE)
    html = re.sub(subject_pattern, '', html)

    # Strip other HTML tags
    cleaner = HTMLCleaner()
    cleaner.feed(html)
    clean_text = cleaner.get_data()

    # Highlight verification codes after the word "code" or "code:", e.g., "verification code: tkv5z-tjd6f"
    pattern = re.compile(r'(code:\s*[\w-]+)', re.IGNORECASE)
    clean_text = re.sub(pattern, lambda match: f"<strong>{match.group(0)}</strong>", clean_text)

    # Highlight OTP (One-Time Password) codes
    otp_pattern = re.compile(r'\b\d{6}\b')  # assuming OTP is a 6-digit number
    clean_text = re.sub(otp_pattern, lambda match: f"<strong>{match.group(0)}</strong>", clean_text)

    # Remove multiple spaces and newlines
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    return clean_text