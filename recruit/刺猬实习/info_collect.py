import requests
import os
import json
import pandas as pd
import time
import random

"""数据采集"""
job = []
salary = []
practice_time = []
describe = []
educational = []
release_time = []
headcount = []
company = []
size = []
address = []
trade = []

n = 50
count = 0
for i in range(n):
    count += 1
    print(f'正在第{count}个一级页面')
    """一级数据采集"""
    href1 = []
    href2 = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'}
    url_js = f'https://www.ciwei.net/api/Shixi_Pc/search?city=0&getCount=1&s_c=1&page={count}&source=pc'
    web_js = requests.get(url_js, headers=headers)                  # 发送访问请求
    json_text = json.loads(web_js.text)
    # 将列表转化为数据框架，以便于通过key获取value
    data = pd.DataFrame(json_text['data']['lists'])
    job.extend(data["title"])                                       # 对网页源码进行解析
    salary.extend(data["salary"])                                   # 工作岗位
    practice_time.extend(data["work_time_string"])                  # 薪资待遇
    href1.extend(data["jobid"])                                     #岗位详情网址ID
    href2.extend(data["company_id"])                                #公司详情网址ID

    # # 数据保存
    # data_dic_1 = {
    #     '岗位名称': job,
    #     '薪资待遇': salary,
    #     '实习时长': practice_time,
    #     '岗位详情网址ID': href1,
    #     '公司详情网址ID': href2
    # }
    # # 循环采集时不可用的
    # job_1 = pd.DataFrame(data_dic_1)
    # print(job_1)


    """二级数据采集"""
    for j in href1:
        url_sub1 = 'https://www.ciwei.net/api/Shixi_V2_Job/detail?jobid={}'.format(j)    # 二级页面的网址
        print('...正在爬取【岗位详情】二级网页：{}'.format(url_sub1))
        web_sub1 = requests.get(url_sub1, headers=headers)
        json_sub1 = json.loads(web_sub1.text)
        data_sub1 = json_sub1['data']['jobInfo']
        describe.append(data_sub1["fduty"])                         # 获取工作描述
        educational.append(data_sub1["education"])                  # 学历要求
        headcount.append(data_sub1["num"])                          # 招聘人数
        release_time.append(data_sub1["refresh_time"])              # 发布时间
        # 随机时间
        delay = random.uniform(0.5, 1)
        time.sleep(delay)

    for k in href2:
        url_sub2 = 'https://www.ciwei.net/api/Shixi_V2_Company/detail?company_id={}'.format(k)    # 二级页面的网址
        print('...正在爬取【公司详情】二级网页：{}'.format(url_sub2))
        web_sub2 = requests.get(url_sub2, headers=headers)
        json_sub1 = json.loads(web_sub2.text)
        data_sub1 = json_sub1['data']['companyInfo']
        company.append(data_sub1["comname"])                        # 公司名称
        size.append(data_sub1["scale"])                             # 公司规模
        address.append(data_sub1["provinces_string"])               # 企业地点
        trade.append(data_sub1["industry_string"])                  # 公司领域
        # 随机时间
        delay = random.uniform(0.5, 1)
        time.sleep(delay)

    # data_dic_2 = {
    #     '工作描述': describe,
    #     '学历要求': educational,
    #     '招聘人数': headcount,
    #     '发布时间': release_time,
    #     '公司名称': company,
    #     '公司规模': size,
    #     '工作地点': address,
    #     '企业领域': trade
    # }
    # # 循环采集时不可用的
    # job_2 = pd.DataFrame(data_dic_2)
    # print(job_2)


# 数据保存
data_dic = {
    '岗位名称': job,
    '薪资待遇': salary,
    '实习时长': practice_time,
    '工作描述': describe,
    '学历要求': educational,
    '招聘人数': headcount,
    '发布时间': release_time,
    '公司名称': company,
    '公司规模': size,
    '工作地点': address,
    '企业领域': trade
}
os.chdir('./recruit/刺猬实习/')
job_information = pd.DataFrame(data_dic)
job_information.to_csv('job_information.csv', encoding='utf-8-sig', index=None, mode='a')
print(job_information.shape)