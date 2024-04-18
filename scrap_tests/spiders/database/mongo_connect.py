import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

# cluster uri
cluster_uri = f"mongodb+srv://muhammadnasir1991:{os.getenv('JvfQB6BCmHsVBkdG')}@cluster0.p6vsysp.mongodb.net/?retryWrites=true&w=majority"

# Create a MongoDB client
client = pymongo.MongoClient(cluster_uri)