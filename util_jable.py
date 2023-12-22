from bs4 import BeautifulSoup
from selenium import webdriver
from setting import driver_path
from selenium.webdriver.chrome.options import Options

def get_video_info_add_db(page_url):
    img_lists = []
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1")
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    # driver = webdriver.Chrome(executable_path=driver_path)

    driver.get(page_url)
    html = driver.page_source
    # print(html)
    soup = BeautifulSoup(html, "lxml")

    lists = soup.find_all('div', attrs={'class': "video-img-box mb-e-20"})
    for i in lists:

        print(i)
        ja_href = i.a['href']
        print(ja_href)
        ja_src = i.img['src']
        print(ja_src)
        ja_data_src = i.img['data-src']
        print(ja_data_src)
        ja_data_preview = i.img['data-preview']
        print(ja_data_preview)
        tittle_soup = i.find('div', attrs={'class': 'detail'})
        print([tittle_soup])
        x = tittle_soup.a.text
        print(x)
        break
        # vid = photo.split('/')[-1].split('.')[0]
        # time = i.span.text
        # title = i.find_next('span', attrs={'class': 'video-title title-truncate m-t-5'}).text
        #
        # down_url = f'{video_url_path}{vid}/{vid}.m3u8'
        #
        # video_msg = {'vid': vid, 'photo': photo, 'title': title, 'time': time, 'down_url': down_url, 'use': 1}
        # print(video_msg)
        #
        # jav_col_db.update_one(filter={'vid': vid}, update={'$setOnInsert': video_msg}, upsert=True)
        #
        # img_lists.append(video_msg)

    return img_lists

get_video_info_add_db('https://jable.tv/categories/chinese-subtitle/')