import redis
from redis import from_url

# Create a redis client
redisClient = redis.from_url('redis://default:QoXPc9gnci5QELoYThRX1RkRHZjyl7jp@redis-13281.c326.us-east-1-3.ec2.cloud.redislabs.com:13281')

# Push URLs to Redis Queue
redisClient.lpush('quotes_queue:start_urls', "https://www.lme.com/en/news?page=1/")
redisClient.lpush('quotes_queue:start_urls', "https://www.lme.com/en/news?page=2/")
redisClient.lpush('quotes_queue:start_urls', "https://www.lme.com/en/news?page=3/")
redisClient.lpush('quotes_queue:start_urls', "https://www.lme.com/en/news?page=4/")
redisClient.lpush('quotes_queue:start_urls', "https://www.lme.com/en/news?page=5/")
redisClient.lpush('quotes_queue:start_urls', "https://www.lme.com/en/news?page=6/")
redisClient.lpush('quotes_queue:start_urls', "https://www.lme.com/en/news?page=7/")
redisClient.lpush('quotes_queue:start_urls', "https://www.lme.com/en/news?page=8/")
redisClient.lpush('quotes_queue:start_urls', "https://www.lme.com/en/news?page=9/")

