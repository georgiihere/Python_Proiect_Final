import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Proiect_Final"]
books = db['Books']