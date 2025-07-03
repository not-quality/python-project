import pandas as pd
import os
# _flatten():用于展平嵌套列表
# from tkinter import _flatten
import jieba
import re
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
import warnings
warnings.filterwarnings('ignore')


os.chdir('./data_pretreatment')
job_information = pd.read_csv('job_information.csv')
# 查看数据
print(job_information)
# 查看数据标签信息
print(job_information.info())


# 去除“岗位名称”中括号里的内容
job_information['岗位名称'] = [re.sub(r'[\（|\()|【].*?[\）|\)|】]','',job_information['岗位名称'][i]) for i in range(job_information.shape[0])]
print(job_information['岗位名称'])
# 统计薪资待遇为 面议的数量(True等价于1)
print((job_information['薪资待遇']=='面议').sum())
# 删除为面议的信息(loc:数据筛选；reset_index:索引重置)
job_information = job_information.loc[job_information['薪资待遇']!='面议'].reset_index(drop=True)
# 将薪资单位转化为“元/天”，并求区间的均值，
for i in range(job_information.shape[0]):
    salary = job_information['薪资待遇'][i]
    ls = re.findall('\d+',salary)
    # 计算平均日薪资（四舍五入，保留两位小数）
    if salary[-3:] == 'K/月':
        job_information['薪资待遇'][i] = round((int(ls[0])+int(ls[1]))*1000/30/2,2)
    else:
        job_information['薪资待遇'][i] = round((int(ls[0])+int(ls[1]))/2,2)
# 统一为保留两位小数的浮点数
job_information['薪资待遇'] = job_information['薪资待遇'].astype(float)
print(job_information['薪资待遇'])


# 发布时间只保留日期（按照指定的格式 '%Y/%m/%d %H:%M:%S' 解析字符串，将日期时间字符串转换为 Pandas 的 DateTime 对象）
job_information['发布时间'] = pd.to_datetime(job_information['发布时间'],format='%Y-%m-%d %H:%M')
job_information['发布日期'] = job_information['发布时间'].dt.date
# 提取年
job_information['年'] = job_information['发布时间'].dt.year


# 中国共计34个省级行政区，包括23个省、5个自治区、4个直辖市、2个特别行政区。
# 23个省分别为:河北省、山西省、辽宁省、吉林省、黑龙江省、江苏省、浙江省、安徽省、福建省、江西省、山东省、河南省、湖北省、湖南省、广东省、海南省、四川省、贵州省、云南省、陕西省、甘肃省、青海省、台湾省。
# 5个自治区分别为:内蒙古自治区、广西壮族自治区、西藏自治区、宁夏回族自治区、新疆维吾尔自治区。
# 4个直辖市分别为:北京市、天津市、上海市、重庆市。
# 2个特别行政区分别为:香港特别行政区、澳门特别行政区。
# tolist():转为列表；set():转为数组(去重)
for i in set(job_information['工作地点'].tolist()):
    # 筛选包含'工作地点'数据的'工作地点'标签内容进行处理
    if i =='北京' or i =='上海' or i =='重庆' or i =='天津':
        job_information.loc[job_information['工作地点'] == i, '工作地点'] = i + '市'
    elif i == '广西':
        job_information.loc[job_information['工作地点'] == i, '工作地点'] = i + '壮族自治区'
    elif i =='内蒙古' or i =='西藏':
        job_information.loc[job_information['工作地点'] == i, '工作地点'] = i + '自治区'
    elif i == '宁夏':
        job_information.loc[job_information['工作地点'] == i, '工作地点'] = i + '回族自治区'
    elif i == '新疆':
        job_information.loc[job_information['工作地点'] == i, '工作地点'] = i + '维吾尔自治区'
    elif i == '全国':
        job_information.loc[job_information['工作地点'] == i, '工作地点'] = i 
    else:
        job_information.loc[job_information['工作地点'] == i, '工作地点'] = i + '省'
        
# 处理“全国”
ls = list(set(job_information['工作地点']))
df1 = job_information.loc[job_information['工作地点']=='全国']
df2 = df1.copy()
for i in ls:
    df2['工作地点']=i
    df1 = pd.concat([df1, df2])
job_information = pd.concat([job_information,df1])
job_information = job_information.loc[job_information['工作地点']!='全国'].reset_index(drop=True)
print(job_information['工作地点'])


"""数据清理"""
# 缺失值(isnull():创建一个DataFrame缺失值位置为 True，非缺失值为 False)
print(job_information.isnull().sum())

# 重复值
job_information.drop_duplicates(inplace=True)
job_information.reset_index(drop=True,inplace=True)
print(job_information)

# 差异值
job_information.boxplot(column='薪资待遇',figsize=(12,8))
plt.show()

# 删除异常值
job_information = job_information.loc[(job_information['薪资待遇']>50)&(job_information['薪资待遇']<250)].reset_index(drop=True)
print(job_information)

# 分词、去停用词
with open('stoplist.txt', encoding='utf-8') as f:
    stopWords = f.read()
stopWords += '\【】\\t\\r\\n\\xa0\-\•'
f.close()

for i in range(job_information.shape[0]):
    # jieba.lcut()：使用 jieba 库的精确模式分词，返回词语列表
    words = jieba.lcut(job_information['工作描述'][i])
    words = [i for i in words if i not in stopWords]   # 去除停用词
    job_information['工作描述'][i] = words
print(job_information['工作描述'])

job_information.to_csv('data_pre.csv',index=False,encoding='utf-8-sig')