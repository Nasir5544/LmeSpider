import os
import scrapy
from datetime import datetime
from scrap_tests.items import LmeItem, QuoteItem

class LmeJSSpider(scrapy.Spider):
    name = "lme_js"

    # override global settings for this spider
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": False,
            "timeout": 20 * 1000,  # 20 seconds
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
    }

    start_urls = [
        "https://www.lme.com/en/news"
    ]

    # download_directory = os.path.join(os.getcwd(), 'spiders', 'downloads')

    def start_requests(self):
        # for url in self.start_urls:
            # driver.get(url)
        url = "https://quotes.toscrape.com/js/"
        yield scrapy.Request(url, self.parse, meta={"playwright": True})
    
    def parse(self, response):
        for quote in response.css('div.quote'):
            print('Quote: %s' % quote.css('span.text::text').get())