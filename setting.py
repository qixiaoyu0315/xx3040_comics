import pymongo

mongo_db_client = pymongo.MongoClient("mongodb://localhost:27017/")
# 漫画数据库
x3040_db_mydb = mongo_db_client["comics_db"]
comics_x3040_db = x3040_db_mydb["comics_x3040"]

# 视频数据库
java_db_mydb = mongo_db_client["java_db"]
jav_col_db = java_db_mydb["jav_col"]

# HTML 头
headers = {
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "User-Agent": 'Mozilla/5.0 (Linux; Android 11; Redmi K30 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 Mobile Safari/537.36 EdgA/45.09.4.5079',
    'Referer': 'https://www.san499.com/'
}
# 代理
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}

# 漫画路径
url = 'https://www.san499.com/meinv'
# 漫画通用路径
comics_url = 'https://www.san499.com/'
# 存放位置
loc_path_c = r'C:\Users\23909\Desktop\xx3040\xx3040'

# chrome调试工具
driver_path = r"./soft/chromedriver.exe"
# 视频通用路径
video_url_path = 'https://cdn77.91p49.com/m3u8/'
# 视频通用路径
url_path_c = 'https://91porn.com/v.php?category=rf&viewtype=basic&page='
# 下载图片地址
down_pic_path_c = './image/'
# 图片解析地址
image_analy = './image_analy/'
