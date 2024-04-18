import scrapy

class QuotesSpider(scrapy.Spider):
    name = "static_spider"
    start_urls = [
        "http://quotes.toscrape.com",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        elements = response.css('.quote')

        for element in elements:
            yield {
                'quote': element.find_element(By.CSS_SELECTOR, 'span.text').text,
                'author': element.find_element(By.CSS_SELECTOR,'small.author').text,
                'tags': element.find_element(By.CSS_SELECTOR,'div.tags').text
            }
