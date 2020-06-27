import requests
from bs4 import BeautifulSoup as bs
import lxml.etree
import pandas as pd

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'maoyan.com',
    'Referer': 'https://u.geekbang.org/lesson/18?article=252019&utm_source=infoq_web&utm_medium=GEOBanner&utm_term=GEOBanner',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
}

# 域名
domain = 'https://maoyan.com'

# 猫眼电影排名
url = 'https://maoyan.com/films?showType=3'

# 猫眼电影前10个电影名称、详情连接
def get_top_10(url):
    response = requests.get(url, headers=header)
    bs_info = bs(response.text, 'html.parser')

    toplist = []

    for tags in bs_info.find_all('div', attrs={'class': 'movie-item-title'}, limit=10):
        _item = {}
        _item['name'] = tags.find('a').text
        _item['href'] = tags.find('a').get('href')
        toplist.append(_item)
    return toplist

# 猫眼电影前10个电影名称、详情 电影类型 上映时间
def get_movie_detail(movie):
    response = requests.get(domain + movie['href'], headers=header)
    bs_info = bs(response.text, 'html.parser')
    
    tags = bs_info.find('div', attrs={'class': 'movie-brief-container'}).find_all('li', attrs={'class': 'ellipsis'})
    show = tags[2].text
    typelist = []
    for atags in tags[0].find_all('a', attrs={'class': 'text-link'}):
        typelist.append(atags.text.strip())
    movie_type = '-'.join(typelist)
    mylist = [movie['name'], show, movie_type]
    return mylist

# 开始爬取前10排行
top_10 = get_top_10(url)
# 控制请求的频率，引入了time模块
from time import sleep
sleep(3)

export_list = []
for movie in top_10:
    movie_item = get_movie_detail(movie)
    export_list.append(movie_item)
    sleep(3)



movie1 = pd.DataFrame(data = export_list)

# windows需要使用gbk字符集
movie1.to_csv('./movie1.csv', encoding='utf8', index=False, header=False)