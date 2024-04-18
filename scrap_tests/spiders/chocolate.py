import scrapy
from selenium import webdriver
from scrap_tests.items import ChocolateProduct
from scrap_tests.loaders import ChocolateProductLoader
from dotenv import load_dotenv
import os

load_dotenv()

class ChocolateSpider(scrapy.Spider):
    # override global settings for this spider
    custom_settings = {
        "MONGO_URI": f"mongodb+srv://ewarenet_user:{os.getenv('MONGO_PASS')}@cluster0.marvopk.mongodb.net/?retryWrites=true&w=majority",
        "MONGO_DB": "ewarenet",
        "ITEM_PIPELINES": {
            'scrap_tests.pipelines.PriceToUSDPipeline': 100,
            'scrap_tests.pipelines.DuplicatesPipeline': 200,
            'scrap_tests.pipelines.MongoDBPipeline': 300
        }
    }
    
    name = "choco_spider"
    start_urls = [
        "https://www.chocolate.co.uk/collections/all",
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


    # product details
    def parse_product_details(self, response):
        chocolate = response.meta['chocolate']
        description = response.css('div.product-form__description p::text').get()
        chocolate.add_value('description', description)
        yield chocolate.load_item()

    def parse(self, response):
        driver = response.meta["driver"]
        products = response.css('product-item')
        
        for product in products:
            chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector=product)
            chocolate.add_css('name', 'a.product-item-meta__title::text')
            chocolate.add_css('price', 'span.price', re="<span class=\"price\">\n              <span class=\"visually-hidden\">Sale price</span>(.*)</span>")
            chocolate.add_css('url', 'div.product-item-meta a::attr(href)')

            # Follow the link to the product details page
            product_details_url = 'https://www.chocolate.co.uk' + product.css('div.product-item__image-wrapper a::attr(href)').get()
            yield response.follow(product_details_url, self.parse_product_details, meta={'chocolate': chocolate})

        next_page = response.css('[rel="next"] ::attr(href)').get()
        if next_page is not None:
           next_page_url = 'https://www.chocolate.co.uk' + next_page
           yield response.follow(next_page_url, callback=self.parse, meta={"driver": driver})