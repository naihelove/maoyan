#   猫眼电影新闻资讯爬取
import requests
from pyquery import PyQuery as pq
from requests.exceptions import RequestException
import pymongo
import time

# 获取网页源代码
def get_one_page(url):
    try:

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36'
                          + ' (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


# 解析网页抓取图片与内容
def parse_one_page(html,page):
    print('正在爬取第',page,'页')
    doc=pq(html)    # pq初始化html
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


# 初始化MongoDB，保存数据
def save_to_mongo(result):
    """
    保存至MongoDB:param result: 结果
    """
    MONGO_URL = 'localhost'   # 地址
    MONGO_DB = 'maoyanzixun'  # 指定操作数据库
    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    MONGO_COLLECTION = 'content'
    try:
        if db[MONGO_COLLECTION].insert_one(result):  # 声明一个collection对象
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


# 编写运行主函数
def main(offset):
    url = 'https://maoyan.com/news?showTab=2&offset=' + str(offset)
    page=int(offset/10+1)
    html = get_one_page(url)
    parse_one_page(html,page)

if __name__== '__main__':
    for i in range(1):      #   此处括号内可以根据情况在一定范围内任意取值
        main(offset=i * 10)
        time.sleep(1)

