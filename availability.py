import pymongo
from database import *

def order_books_by_availability():
    return books.find({}, {'_id': 0}).sort("Status",pymongo.ASCENDING)
