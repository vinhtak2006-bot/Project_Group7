import json
from pymongo import MongoClient

json_file_path = "../3.Data_Integration/Final_Data.json"

with open(json_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

client = MongoClient("mongodb+srv://AnhKhoa123:12345@cluster0.ql2vkbs.mongodb.net/?appName=Cluster0")

db = client["homeoffice_db"]
collection = db["products"]

collection.delete_many({})

collection.insert_many(data)

client.close()