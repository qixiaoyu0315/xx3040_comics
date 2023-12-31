import uvicorn

from rich import print
from fastapi import Request
from fastapi import FastAPI, applications
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi.openapi.docs import get_swagger_ui_html
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from util_video import get_video_info, get_photo_analysis, get_down_video
from util_x3040 import add_comics_rss, view_all_comics, get_page_img_list_to_dict, down_comics_img_for_page, \
    look_comics, check_pig_ex, update_all_comics, update_comics_one


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui-bundle.js',
        swagger_css_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui.css'
    )


applications.get_swagger_ui_html = swagger_monkey_patch

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")
template = Jinja2Templates(directory='templates')

scheduler = AsyncIOScheduler()


# @scheduler.scheduled_job('cron', hour=9, minute=00)
@scheduler.scheduled_job("interval", seconds=1805)
def update_many():
    # update_all_comics()
    pass


# 开始定时任务
@app.on_event("startup")
async def startup_event():
    scheduler.start()


# 结束定时任务
@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


# 主页面显示
@app.get("/")
def comics_root(request: Request):
    comics_list = view_all_comics()
    return template.TemplateResponse('index.html', {'request': request, 'comics_list': comics_list, 'home_active':'active'})


# 添加订阅功能
@app.get("/add_rss/")
def comics_add_rss(request: Request, uid_url: str, ):
    flag = add_comics_rss(uid_url)
    if flag:
        msg_text = '订阅成功'
    else:
        msg_text = '订阅失败'
    comics_list = view_all_comics()
    return template.TemplateResponse('index.html',
                                     {'request': request, 'comics_list': comics_list, 'msg_text': msg_text, 'home_active':'active'})


# 内容页面跳转
@app.get("/comics/{uid}/{page}")
def comics_to_page(request: Request, uid: str, page: str):
    # 新订阅内容 默认解析 第一页
    get_page_img_list_to_dict(uid, page)
    # 新订阅内容 默认下载 第一页
    flag = down_comics_img_for_page(uid, page)
    print([flag])
    if flag:
        comics_list = view_all_comics()
        return template.TemplateResponse('index.html', {'request': request, 'comics_list': comics_list,
                                                       'msg_text': '下载图片中，刷新即可', 'home_active':'active'})

    page_img_list = look_comics(uid, page)

    check_pig_ex(page_img_list)
    # 新订阅内容 默认解析 第一页
    get_page_img_list_to_dict(uid, str(int(page) + 1))
    # 新订阅内容 默认下载 第一页
    down_comics_img_for_page(uid, str(int(page) + 1))

    if page_img_list:
        return template.TemplateResponse('comics_page.html', {'request': request, 'page_img_list': page_img_list, 'home_active':'active'})
    else:
        return '404'


# 更新全部订阅功能
@app.get("/update_rss/{uid}")
def comics_update_rss_all(request: Request, uid: str):
    update_comics_one(uid)
    comics_list = view_all_comics()
    return template.TemplateResponse('index.html',
                                     {'request': request, 'comics_list': comics_list, 'msg_text': '全部更新成功', 'home_active':'active'})


# 更新全部订阅功能
@app.get("/update_rss_all/")
def comics_update_rss_all(request: Request):
    update_all_comics()
    comics_list = view_all_comics()
    return template.TemplateResponse('index.html',
                                     {'request': request, 'comics_list': comics_list, 'msg_text': '全部更新成功', 'home_active':'active'})


# 解析网页
@app.get("/get_video_info_api")
def get_video_info_api(request: Request, start: str, end: str):
    get_video_info(int(start.strip()),int(end.strip()))
    return template.TemplateResponse('index.html',
                                     {'request': request, 'msg_text': '解析完成', 'ios_active':'active'})

# 解析图片
@app.get("/get_photo_analysis_api")
def get_photo_analysis_api(request: Request):
    get_photo_analysis()
    return template.TemplateResponse('index.html',
                                     {'request': request, 'msg_text': '解析完成', 'ios_active':'active'})

# 解析图片
@app.get("/down_video_api")
def get_photo_analysis_api(request: Request, video_num):
    get_down_video(video_num)
    return template.TemplateResponse('index.html',
                                     {'request': request, 'msg_text': '下载完成', 'ios_active':'active'})


if __name__ == "__main__":
    uvicorn.run(app='main:app', host="0.0.0.0", port=5555, reload=True)
