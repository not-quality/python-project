import requests
from pathlib import Path
import re
import time
import random

"""
游戏图片爬取
以《英雄联盟》皮肤为例。
"""

#获取全英雄名称 
all_hero_js_url = 'https://lol.qq.com/biz/hero/champion.js'
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0' }
all_hero_js = requests.get(all_hero_js_url, headers=headers).text
all_hero_names = re.findall(r'"\d+?":"(\w+?)"',all_hero_js)

for n in all_hero_names:
    # 获取英雄对应的皮肤id和名称
    hero_info_url = f'https://lol.qq.com/biz/hero/{n}.js'
    hero_info = requests.get(hero_info_url, headers=headers).text
    hero_ids = re.findall(r'"id":("\d+?")',hero_info)
    hero_names = re.findall(r'"name":"(.+?)".+?"chromas"',hero_info)
        

    for id,name in zip(hero_ids,hero_names):

        # 由于英雄联盟皮肤地址id使用了hash加密，暂时使用安妮图片地址演示
        # img_url =f'https://game.gtimg.cn/images/lol/act/img/skin/big_{id}.jpg'
        img_url =f'https://game.gtimg.cn/images/lol/act/img/skin/big_0b95894e-0df2-470e-b282-6c5f5cf41955.jpg'

        img_res = requests.get(img_url,headers=headers)
        # 清洗皮肤名称（K\\/DA系列皮肤中的/会在写入时被识别为创建文件夹）
        name = name.encode().decode('unicode_escape').replace('/','').replace('\\','')

        # 创建文件夹并写入方式
        file_path = Path(f"英雄联盟（皮肤）/{n}/{name}.jpg")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # 'wb' 二进制模式写入
            with file_path.open('wb') as f:
                # 写入二进制图片数据  
                f.write(img_res.content)  
            print(f"文件已成功写入到: {file_path}")
        except Exception as e:
            print(f"写入文件时出错: {e}")
        
        # 随机时间
        delay = random.uniform(0.5, 1)
        time.sleep(delay)






