import re
import scrapy
from pathlib import Path


class MailSpider(scrapy.Spider):
    name = 'mail_spider'

    def __init__(self, domain=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = domain
        self.emails = []
        self.start_urls = ['http://www.' + self.domain] if self.domain else []
        self.social_media_domains = [
            'facebook.com', 'linkedin.com', 'instagram.com', 'youtube.com',
            'twitter.com', 'pinterest.com', 'plus.google.com', 'blogspot.com',
            'telegram.me', 'whatsapp.com']
        self.garbage_extensions = [
            'pdf', 'doc', 'jpg', 'jpeg', 'docx',
            'xlsx', 'png', 'gif', 'mp3', 'mp4',
            'avi', 'mov', 'ppt', 'pptx', 'exe',
            'zip', 'rar', '7z', 'gz', 'tar',
            'iso', 'dmg'
        ]

    def is_link_valid(self, link):
        if not link.startswith("http"):
            return False
        if any(domain in link for domain in self.social_media_domains):
            return False
        if  any(extension in link for extension in self.garbage_extensions):
            return False
        if not self.domain in link:
            return False
        return True

    def parse(self, response):
        # Extract email addresses using regular expression
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text)

        # Yield each email address as a separate item
        for email in set(emails):
            # Check if email address is unique
            if email not in self.emails:
                self.emails.append(email)
                yield {'email': email, 'reference': response.url}

        # Follow all links on the page and call the parse method recursively
        for link in response.css('a::attr(href)').getall():
            if self.is_link_valid(link):
                yield response.follow(link, callback=self.parse)

