import os
import glob
import requests

from rich import print
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from setting import driver_path, video_url_path, url_path_c, down_pic_path_c, image_analy, jav_col_db

def image_download(video):
    vid = video['vid']
    title = video['title']
    title = ''.join(filter(str.isalnum, title))
    down_path = f'{down_pic_path_c}{vid}-{title}.jpg'
    print(down_path)

    r = requests.get(video['photo'], stream=True)
    while True:
        try:
            with open(down_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=32):
                    f.write(chunk)
            break
        except Exception as e:
            print(e)


def video_download(video):
    down_url = video['down_url']
    title = video['title']
    command = f'./soft/N_m3u8DL-RE "{down_url}" --header "Referer:https://91porn.com/"  --save-name "{title}" --save-dir "./video/"'
    print(command)
    os.system(command)


# 获取需要解析的url
def get_page_url(start, end):
    url_list = []
    for i in range(start, end + 1):
        url_list.append(f'{url_path_c}{i}')
    return url_list


# 1.获取url
def get_video_info(start,end):
    # 通过输入 获取到需要解析的链接
    url_list = get_page_url(start, end)
    # 解析数据 存入数据库
    for url in url_list:
        print([url])
        img_list = get_video_info_add_db(url)
        for i in img_list:
            print(i)
            image_download(i)


# 获取页面中的信息 存入数据库
def get_video_info_add_db(page_url):
    img_lists = []
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument(
    #     "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1")
    # driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    driver = webdriver.Chrome(executable_path=driver_path)

    driver.get(page_url)
    html = driver.page_source
    print(html)
    soup = BeautifulSoup(html, "lxml")

    lists = soup.find_all('div', attrs={'class': "col-xs-12 col-sm-4 col-md-3 col-lg-3"})
    for i in lists:
        photo = i.img['src']
        vid = photo.split('/')[-1].split('.')[0]
        time = i.span.text
        title = i.find_next('span', attrs={'class': 'video-title title-truncate m-t-5'}).text

        down_url = f'{video_url_path}{vid}/{vid}.m3u8'

        video_msg = {'vid': vid, 'photo': photo, 'title': title, 'time': time, 'down_url': down_url, 'use': 1}
        print(video_msg)

        jav_col_db.update_one(filter={'vid': vid}, update={'$setOnInsert': video_msg}, upsert=True)

        img_lists.append(video_msg)
    return img_lists


# 3.
def get_photo_analysis():
    photo_name_list = glob.glob(f'{image_analy}*.jpg')
    print(photo_name_list)
    for photo_name in photo_name_list:
        vid = photo_name.split('/')[-1].split('-')[0]
        jav_col_db.update_one(filter={'vid': vid}, update={'$set': {'use': 2}})


# 4.
def get_down_video(video_num):
    for video in jav_col_db.find({'use': 2}).limit(video_num):
        print(video)
        video_download(video)
        jav_col_db.update_one(filter={'vid': video['vid']}, update={'$set': {'use': 3}})


if __name__ == '__main__':
    pass
#     sel_num = int(input('1.获取页数\n2.解析图片\n3.下载视频\n'))
#     if sel_num == 1:
#         get_video_info()
#     elif sel_num == 2:
#         get_photo_analysis()
#     elif sel_num == 3:
#         down_num = int(input('输入下载视频个数\n'))
#         get_down_video(down_num)
