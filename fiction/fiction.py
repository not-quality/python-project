import requests
from lxml import html
from pathlib import Path
import re
import time
import random
et = html.etree


"""
笔趣阁小说爬取
以《凡人修仙传》为例
"""

# 主页地址
url_head = 'https://www.3fs232349823.xyz'

# 目录地址(终止地址)
url_content = '/html/45942/'

# 第一章地址
url = 'https://www.3fs232349823.xyz/html/45942/1.html'

# 请求头伪装
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'
}

# 初始化计算器
count = 0

# 全部下载
# while True:

# 部分下载
for _ in range(1):

    # 计数器
    count += 1

    # 随机时间
    delay = random.uniform(0.5, 2)
    time.sleep(delay)

    # 获取网页数据
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'


    # xpath筛选网页数据
    e = et.HTML(res.text)


    title = e.xpath('//div/div/h1/text()')[0]
    content = e.xpath('//div[@id="chaptercontent"]/text()')
    url_next = e.xpath('//*[@id="pb_next"]/@href')[0]
    
    # 更新url
    url = f"{url_head}{url_next}"


    ls = []
    # 排除广告文本
    for i in content[0:-2]:
        # 删除所有空白字符
        text = re.sub(r'\s', '', i) 
        ls.append(text)


    # 创建文件夹并写入方式
    file_path = Path(f"凡人修仙传（小说）/{count}.{title}.txt")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n\n".join(ls)
    try:
        file_path.write_text(text, encoding='utf-8')
        print(f"文件已成功写入到: {file_path}")
    except Exception as e:
        print(f"写入文件时出错: {e}")


    # 判断-跳出循环(最后一章)
    if url_next == url_content:
        break







