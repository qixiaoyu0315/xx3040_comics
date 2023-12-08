import pymongo

mongo_db_client = pymongo.MongoClient("mongodb://localhost:27017/")
x3040_db_mydb = mongo_db_client["comics_db"]
comics_x3040_db = x3040_db_mydb["comics_x3040"]

headers = {
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "User-Agent": 'Mozilla/5.0 (Linux; Android 11; Redmi K30 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 Mobile Safari/537.36 EdgA/45.09.4.5079',
    'Referer': 'https://www.san499.com/'
}

proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}

url = 'https://www.san499.com/meinv'


comics_url = 'https://www.san499.com/'

loc_path_c = r'C:\Users\23909\Desktop\xx3040\xx3040'
