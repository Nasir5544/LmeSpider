import scrapy

class ChocolateProduct(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    
class QuoteItem(scrapy.Item):
    quote = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

class LmeNewsItem(scrapy.Item):
    title = scrapy.Field()
    file = scrapy.Field()
    published = scrapy.Field()
    scraped = scrapy.Field()
    exchange = scrapy.Field()

class LmeItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    file = scrapy.Field()
    scraped = scrapy.Field()
    exchange = scrapy.Field()
