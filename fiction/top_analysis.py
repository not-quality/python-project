# %%
import requests
from lxml import etree
import time
import random
import re
import pandas as pd
from pathlib import Path

"""
爬取《笔趣阁》中小说排行榜内容并进行数据分析
"""

# 主页地址
url_head = 'https://www.997b84a6.sbs'
# 假设排行榜页面路径
rank_path = '/top/'  # 实际排行榜页面路径
rank_url = f"{url_head}{rank_path}"

# 请求头伪装
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'
}

# 随机延迟
delay = random.uniform(0.5, 1)
time.sleep(delay)

# 获取排行榜页面
response = requests.get(rank_url, headers=headers)
response.encoding = 'utf-8'
if response.status_code != 200:
    print(f"请求失败，状态码: {response.status_code}")
    exit()
else:
    print(f"成功获取页面内容，状态码: {response.status_code}")

html = etree.HTML(response.text)
print(f"成功获取页面内容，{len(response.text)}")

# %%
# 提取所有排行榜标题和内容
rank = html.xpath('//h2/text()')
title = html.xpath('//li/a/text()')[10:]
author = html.xpath('//li/text()')

# %%
# 清洗榜单
# 移除榜单类型中的'排行榜'后缀
rank = [re.sub(r'排行榜$', '', item.strip()) for item in rank]
# 清洗标题/清洗标题中的各类括号及其内容
pattern = r'\([^)]*\)|\[[^]]*\]|\{[^}]*\}|<[^>]*>|【[^】]*】|（[^）]*）'
title = [re.sub(pattern, '', item).strip() for item in title]
# 作者名
# 清洗作者名中的特殊字符（斜杠、换行符等）
author = [re.sub(r'[\\/\n]', '', item.strip()) for item in author if item.strip()]

# %%
# 数据整理
# 确保rank有8个类型，每个类型对应50个条目
if len(rank) == 8 and len(title) == 400 and len(author) == 400:
    # 重复每个rank类型50次，以匹配title和content的数量
    expanded_rank = []
    for r in rank:
        expanded_rank.extend([r] * 50)
    
    # 创建DataFrame
    df = pd.DataFrame({
        '榜单': expanded_rank,
        '书名': title,
        '作者': author
    })
    
df

# %%
# 频率分析
df.describe()

# %%
# 保存为CSV文件
output_path = Path(__file__).parent / 'rank_data.csv'
df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"数据已成功保存至{output_path}")
