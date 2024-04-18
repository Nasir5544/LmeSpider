# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo
import boto3
from pymongo import MongoClient

from botocore.exceptions import NoCredentialsError
import os

class ScrapTestsPipeline:
    def process_item(self, item, spider):
        return item

# price to usd
class PriceToUSDPipeline:
    gbpToUsdRate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if adapter.get('price'):
            floatPrice = float(adapter['price'])
            adapter['price'] = round(floatPrice * self.gbpToUsdRate, 2)
            return item
        
        else:
            raise DropItem(f"Missing Price in {item}")


# remove dublicates
class DuplicatesPipeline:

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if(adapter['name'] in self.names_seen):
            raise DropItem(f"duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['name'])
            return item


# mongodb
class MongoDBPipeline:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://mongo:PNJg1god7O4VAMMr@cluster0.p6vsysp.mongodb.net/?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)
        self.db = self.client["scrapper"]
        self.collection = self.db["lme"]
        
        # Create a unique index on the "title" field
        self.collection.create_index("title", unique=True)
        
    def process_item(self, item, spider):
        try:
            # Attempt to insert the item into MongoDB
            self.collection.insert_one(dict(item))
        except pymongo.errors.DuplicateKeyError as e:
            # Handle duplicate key error (e.g., log the error and skip insertion)
            print(f"Duplicate key error: {e}")
            pass
        
        return item

    



# aws s3
class S3Pipeline:
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region_name, aws_s3_bucket_name):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region_name = aws_region_name
        self.aws_s3_bucket_name = aws_s3_bucket_name

    @classmethod
    def from_crawler(cls, crawler):

        return cls(
            aws_access_key_id = os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key = os.getenv('AWS_SECRET_KEY'),
            aws_region_name = os.getenv('AWS_REGION'),
            aws_s3_bucket_name = os.getenv('AWS_BUCKET')
        )

    def open_spider(self, spider):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key,
            region_name = self.aws_region_name
        )

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        try:
            # Replace 'your_key_prefix' with the desired prefix for S3 object keys
            object_key = f'your_key_prefix/{item["unique_id"]}.json'
            content = item.get_json_data()  # Implement a method to convert item to JSON data

            self.s3_client.put_object(
                Bucket=self.aws_s3_bucket_name,
                Key=object_key,
                Body=content,
                ContentType='application/json'
            )
            return item
        
        except NoCredentialsError:
            spider.log("AWS credentials not found. Unable to upload to S3.")
            return item