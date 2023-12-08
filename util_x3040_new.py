import json
import time
import requests
import os

from rich import print
from bs4 import BeautifulSoup
from setting import proxies, headers ,loc_path_c, comics_x3040_db


# 获取html的soup
def get_html_soup(url):  # 获取 soup
    html_doc = ''
    count = 0
    while 1:
        try:
            html_doc = requests.get(url, headers=headers,proxies=proxies)
            break
        except Exception as e:
            print(e)
            count = count + 1
            print("************将在0.3秒钟后重试...**********")
            time.sleep(0.3)
            if count == 10:  # 重试两次 防止无限重试
                break
            continue
    soup = BeautifulSoup(html_doc.content, 'lxml')
    return soup

# 获取写真的所有页面的url
def get_page_list(soup):
    pages = soup.find_all(name='a', attrs={'class': 'post-page-numbers'})
    num = int(len(pages) / 2 - 1)
    lists = []
    for x in pages[0:num]:
        lists.append(x.get('href'))
    return lists


def get_comics_info(html_url:str):
    soup = get_html_soup(html_url)

    uid = html_url.split('/')[-1].split('.')[0].strip()
    tittle = soup.find_all(name='a', attrs={'href': html_url})[0].string[1::].strip()

    page_list = [html_url.replace('.html', '/page-1.html')]
    page_list += get_page_list(soup)
    page_item = {}
    for page in page_list:
        index = page.split('page-')[-1].replace('.html', '').strip()
        page_item.update({index.strip(): {'page': page.strip(),'down':0,'analysis':0,'img_list':[]}})
    comics_info = {'uid':uid,'tittle':tittle,'page_item':page_item,'html_url':html_url,}
    print(comics_info)
    return comics_info


# 获取一页中的img
def get_page_img_list(page_url):
    soup = get_html_soup(page_url)
    img_list = soup.find_all('img')  # 找出所有的img 剔除前三个无用 img
    img_list.pop(0)
    img_list.pop(0)
    img_list.pop(0)
    lists = []
    for i in img_list:
        lists.append(i.get('src'))
    return lists


def down_file_to_rpc(loc_path,uid,page,img_url,head):
    x_url = f"{loc_path}/static/{uid}/{page}"
    json_req = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "aria2.addUri",
            "params": [
                [
                    img_url,
                ],
                {
                    "dir": x_url,
                    "out": f"{img_url.split('/')[-1]}",
                    "header": [
                        f"Referer: {head}"
                    ]
                }
            ]
        })
    rep = requests.post('http://localhost:16800/jsonrpc', json_req)
    print(rep.text)


# 解析每页
def get_page_img_list_to_dict(uid,analysis:str):
    for comics in comics_x3040_db.find({'uid': uid}):
        analysis_info = comics['page_item'].get(analysis,{})
        if analysis_info:
            if analysis_info['analysis'] == 0:
                img_list = get_page_img_list(analysis_info['page'])
                comics_x3040_db.update_one(
                    {'uid': uid, f'page_item.{analysis}': {'$exists': True}},
                    {'$set': {f'page_item.{analysis}.analysis': 1,f'page_item.{analysis}.img_list': img_list}}
                )
            return True
    return False

# 下载单个漫画
def down_comics_img_for_page(uid,down:str):
    flag = False
    for comics in comics_x3040_db.find({'uid': uid}):
        analysis_info = comics['page_item'].get(down, {})
        if analysis_info:
            if analysis_info['down'] == 0 and analysis_info['analysis'] == 1:
                head = analysis_info['page']
                for img in analysis_info['img_list']:
                    down_file_to_rpc(loc_path_c, uid, down, img ,head)
                comics_x3040_db.update_one(
                    {'uid': uid, f'page_item.{down}': {'$exists': True}},
                    {'$set': {f'page_item.{down}.down': 1}}
                )
                flag = True
    return flag

# 添加订阅
def add_comics_rss(html_str: str) -> bool:
    # 获取最基础的信息
    comics_update = get_comics_info(html_str.strip())
    # 信息写入数据库
    comics_x3040_db.update_one({'uid': comics_update['uid'], }, {'$setOnInsert': comics_update}, upsert=True)
    # 新订阅内容 默认解析 第一页
    get_page_img_list_to_dict(comics_update['uid'],'1')
    # 新订阅内容 默认下载 第一页
    down_comics_img_for_page(comics_update['uid'],'1')
    return True


# 主页显示所有漫画
def view_all_comics():
    comics_list = []
    for comics in comics_x3040_db.find():
        comics_list.append({'uid': comics['uid'], 'tittle': comics['tittle'], 'look_url': f"/comics/{comics['uid']}/1", 'down_url': f"/down_rss/{comics['uid']}", })
    return comics_list


def look_comics(uid,page):
    page_img_list = []
    for comics in comics_x3040_db.find({'uid':uid}):
        page_item = comics['page_item'].get(page, {})
        if page_item:
            page_img_list = [ f'/static/{uid}/{page}/' + i.split('/')[-1] for i in page_item['img_list']]
    return page_img_list

def check_pig_ex(img_list):
    print(img_list)
    no_img_list = []
    for img in img_list:
        print([img,os.path.exists(f".{img}")])
        if not os.path.exists(f".{img}"):
            no_img_list.append(img)
    print(no_img_list)
    if no_img_list:
        img_info = no_img_list[0].split("/")
        tittle = '/'.join(no_img_list[0].split("/")[:-1])
        print('tittle',tittle)
        uid = img_info[-3]
        page = img_info[-2]
        comics_info = comics_x3040_db.find_one({'uid': uid})['page_item'][page]
        all_img_list = comics_info['img_list']
        head = comics_info['page']
        print('all_img_list',all_img_list)
        print('no_img_list', no_img_list)
        for no_img in all_img_list:
            print([f'{tittle}/{no_img.split("/")[-1]}'])

            if f'{tittle}/{no_img.split("/")[-1]}' in no_img_list:
                down_file_to_rpc(loc_path_c, uid, page, no_img ,head)
                print(f'down:{img}')

if __name__ == "__main__":
    pass

