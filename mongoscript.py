from pymongo import MongoClient
import datetime

client = MongoClient("mongodb+srv://test:test123@scrapped.alfiwcn.mongodb.net/")


db = client.scrapy

collection = db.books

doc = post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
}

post_id = collection.insert_one(post).inserted_id

print(post_id)

