import requests
import re
import pandas as pd
import time
import random

"""
泰迪内推招聘数据抓取
网页地址
https://www.5iai.com/#/jobList

一级数据
https://www.5iai.com/api/enterprise/job/public/es?pageSize=10&pageNumber=1

二级数据
https://www.5iai.com/api/enterprise/job/public?id=1495652137043099648
"""


# 计数器
count = 0

# 网页爬取次数
n = 10

for _ in range(n):
    count += 1
    info_url = f'https://www.5iai.com/api/enterprise/job/public/es?pageSize=10&pageNumber={count}'
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0' }
    info_js = requests.get(info_url, headers=headers)
    if info_js.status_code == 200:
        print(f"第{count}次请求：请求成功!")
    else:
        print(f"第{count}次请求：请求失败，状态码: {info_js.status_code}")
        continue
    info_js = info_js.text

    # 岗位名称
    positionNames = re.findall(r'"positionName":"(.+?)"',info_js)
    # 最低工资
    minimumWages_raw = re.findall(r'"minimumWage":(\d+)',info_js)
    # 最高工资
    maximumWages_raw = re.findall(r'"maximumWage":(\d+)',info_js)
    # 工资结算时间，1代表月结/2表示日结
    payMethods = re.findall(r'"payMethod":(\d+)',info_js)
    # 统一按月计算工资
    minimumWages = []
    maximumWages = []
    for min,max,pay in zip(minimumWages_raw,maximumWages_raw,payMethods):
        if pay == '1':
            minimumWages.append(min)
            maximumWages.append(max)
        elif pay == '2':
            minimumWages.append(str(int(min)*30))
            maximumWages.append(str(int(max)*30))
            
    # 工作地区
    detailedAddresses = re.findall(r'"detailedAddress":"(.+?)"',info_js)
    # 学历要求，2:大专/3:本科/4:硕士/
    educationalRequirements_raw = re.findall(r'"educationalRequirements":(\d+)',info_js)
    educationalRequirements = []
    for i in educationalRequirements_raw:
        if i == '1':
            educationalRequirements.append("无需学历")
        elif i == '2':
            educationalRequirements.append("大专")
        elif i == '3':
            educationalRequirements.append("本科")
        elif i == '4':
            educationalRequirements.append("硕士")
        else:
            educationalRequirements.append("博士")

    # 经验要求
    exps = re.findall(r'"exp":"(.+?)"',info_js)
    # 招聘人数，0表示不限人数
    counts = re.findall(r'"count":(\d+)',info_js)
    # 公司名称
    shortNames = re.findall(r'"shortName":"(.+?)"',info_js)
    # 公司规模
    personScopes = re.findall(r'"personScope":"(.+?)"',info_js)
    # 行业列表清洗：'[\\"互联网\\",\\"计算机软件\\"]'
    industrys_raw = re.findall(r'"industry":"(.+?])"',info_js)
    industrys = []
    for temp in industrys_raw:
        # 移除首尾的方括号和引号
        temp = temp.strip('[]')
        # 分割字符串并清理每个元素
        element = [e.strip('\\"') for e in temp.split(',') if e.strip()]
        # 清洗后：['互联网', '计算机软件']
        industrys.append(element)
    # 公司类型
    econKinds = re.findall(r'"econKind":"(.+?)"',info_js)

    # 二级网页信息获取
    ids = re.findall(r'{"id":"(\d+)","publishTime"',info_js)
    jobDes = []
    for id in ids:
        sub_url = f'https://www.5iai.com/api/enterprise/job/public?id={id}'
        sub_info = requests.get(sub_url, headers=headers).text
        jobDe = re.findall(r'"jobRequiredments":"(.+)","welfare"',sub_info)
        jobDes.append(jobDe)
        # 随机时间
        delay = random.uniform(0.5, 1)
        time.sleep(delay)

    # 数据保存
    colNames = [
        positionNames, minimumWages, maximumWages, payMethods,
        detailedAddresses, educationalRequirements, exps,counts,
        shortNames, personScopes, industrys, econKinds,jobDes
    ]
    # pandas库将数据转为数据框结构（zip(*)置换数据）
    data_drop = pd.DataFrame(zip(*colNames))
    # 内容追加写入
    data_drop.to_csv('information.csv', header=None, index=None, encoding='utf-8-sig', mode='a+')

    # 随机时间
    print(f"第{count}次请求：请求结束!")
    delay = random.uniform(0.5, 1)
    time.sleep(delay)

