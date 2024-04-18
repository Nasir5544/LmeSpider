import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By

class QuotesSpider(scrapy.Spider):
    name = "dynamic_spider"
    start_urls = [
        "http://quotes.toscrape.com/js/",
    ]

    def start_requests(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=chrome_options)

        for url in self.start_urls:
            driver.get(url)
            yield scrapy.Request(url, self.parse, meta={"driver": driver})

    def parse(self, response):
        driver = response.meta["driver"]
        elements = driver.find_elements(By.CSS_SELECTOR, '.quote')

        for element in elements:
            yield {
                'quote': element.find_element(By.CSS_SELECTOR, 'span.text').text,
                'author': element.find_element(By.CSS_SELECTOR,'small.author').text,
                'tags': element.find_element(By.CSS_SELECTOR,'div.tags').text
            }
