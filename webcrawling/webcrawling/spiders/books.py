from pathlib import Path
from pymongo import MongoClient
import scrapy
import datetime


def inserttodb(page, title, rating, image, price, inStock):
        collection = db[page]
        doc = {
                "Title": title,
                "Image": image,
                "Ratings": rating,
                "Price": price,
                "Instock": inStock,
                "date": datetime.datetime.now(tz=datetime.timezone.utc),
              }
        inserted = collection.insert_one(doc)
        return inserted.inserted_id

client = MongoClient("mongodb+srv://test:test123@scrapped.alfiwcn.mongodb.net/")
db = client.scrapy



class BooksSpider(scrapy.Spider):
        name = "books"
        allowed_domains = ["books.toscrape.com"]
        start_urls = ["https://books.toscrape.com"]

        def start_requests(self):
            urls = [
                "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
                "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
            ]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

        def parse(self, response):
            page = response.url.split("/")[-2]
            filename = f"books-{page}.html"
            #Path(filename).write_bytes(response.body)
            self.log(f"Saved file {filename}")
            cards = response.css(".product_pod")
            for card in cards:
             title = card.css("h3>a::text").get()
             image = card.css(".image_container img")
             image = image.attrib["src"]   

             rating = card.css(".star-rating").attrib["class"].split(" ")[1]
             price = card.css(".price_color::text").get()
             available = card.css(".instock availability")
             if len(available.css(".icon-ok")) > 0:
                 inStock = True
             else:
                 inStock = False
             inserttodb(page, title, rating, image, price, inStock)
