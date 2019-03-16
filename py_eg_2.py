# 猫眼电影新闻资讯爬取
from selenium import webdriver
from pyquery import PyQuery as pq
import pymongo
import time
# 利用selenium进入网站,启用chrome无框模式
url='https://maoyan.com/news?showTab=2'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
# 之上部分也可以改为 browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)利用该无框浏览器抓取
browser.get(url)
# 抓取网页
def index_page(page):
    print('正在爬取第',page,'页')
    if page>1:
        node=browser.find_element_by_css_selector('.page_'+str(page))
        node.click()
    html=browser.page_source
    parse_one_page(html)


# 解析网页抓取图片与内容
def parse_one_page(html):     # 解析一张网页
    # pq初始化html
    doc=pq(html)
    # 解析网页，抓取数据
    items=doc('.news-box ').items()
    for item in items:
         information={
            'image':item.find('.news-img img').attr('src'),
            'title': item.find('h4').find('a').text(),
            'partial_content': item.find('.latestNews-text').text(),
            'source': item.find('.news-source').text(),
            'data': item.find('.news-date').text(),
            }
         print(information)
         save_to_mongo(information)


# 初始化MongoDB 保存数据
def save_to_mongo(result):
    """
    保存至MongoDB
    :param result: 结果
    """
    MONGO_URL = 'localhost'
    MONGO_DB = 'maoyanzixun'
    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    MONGO_COLLECTION = 'content'
    try:
        if db[MONGO_COLLECTION].insert_one(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')

PAGE=7              # 通过修改该变量来控制爬取数量
def main():
    for i in range(1,PAGE+1):
        index_page(i)
        time.sleep(1)
    browser.close()

if __name__ == '__main__':
    main()