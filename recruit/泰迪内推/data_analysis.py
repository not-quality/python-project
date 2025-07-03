import pandas as pd
import matplotlib.pyplot as plt
import re

info = pd.read_csv('information.csv', header=None)

# 列名称
colNames = [
    'positionNames', 'minimumWages', 'maximumWages','payMethods',
    'detailedAddresses', 'educationalRequirements', 'exps', 'counts',
    'shortNames', 'personScopes', 'industrys', 'econKinds', 'jobDes'
]

info.columns = colNames    # 为数据框指定列名称

# 薪资数据处理
info['salary'] = info.loc[:, ['minimumWages', 'maximumWages']].mean(axis=1)

# 人员规模数据处理
mid = info['personScopes'].str.findall('\d+')    # 获取数值内容
personScopes = mid.apply(lambda x: sum(list(map(float, x)))/len(list(map(float, x))))   # 得到明确人员规模数字
info['personScopes'] = personScopes.astype('str')     # 将数据转为字符串类型

# 招聘要求的学历分布
a = info['educationalRequirements'].value_counts()    # 统计不同学历要求的频次
plt.rcParams['font.sans-serif'] = 'SimHei'            # 设置绘图字体
plt.subplots_adjust(bottom=0.15)                      # 设置图形的底边距
plt.bar(a.index, a)             # 绘制条形图
plt.xticks(rotation=45)         # 坐标刻度旋转
plt.title('学历要求分布')
plt.show()

# 各行业的招聘需求数量
industrys = ' '.join(info['industrys'].tolist())    # 将对应列元素拼接成一个长字符串
industrys = re.sub('["\]\[\,]', ' ', industrys)     # 将字符串中的多余符号去除
b = pd.Series(industrys.split()).value_counts()    # 统计各行业的出现频次
plt.rcParams['font.sans-serif'] = 'SimHei'        # 设置绘图字体
plt.subplots_adjust(bottom=0.15)
plt.bar(b.index, b)
plt.xticks(rotation=45)
plt.title('各行业的招聘需求数量')
plt.show()

# 不同类型公司的招聘需求
a = info['econKinds'].value_counts()              # 统计不同类型公司的各招聘数量
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.subplots_adjust(bottom=0.15)
plt.bar(a.index, a)
plt.xticks(rotation=45)
plt.title('不同类型公司的招聘需求')
plt.show()

# 不同类型公司的薪资待遇
disSalarys = info[['econKinds', 'salary']].groupby('econKinds').agg('mean')['salary']    # 通过分组聚合操作求出不同类型公司的平均薪资
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.subplots_adjust(bottom=0.15)
plt.bar(disSalarys.index, disSalarys)
plt.xticks(rotation=45)
plt.title('不同类型公司的薪资待遇对比')
plt.show()

# 不同人员规模公司的薪资待遇对比
disSalarys = info[['personScopes', 'salary']].groupby('personScopes').agg('mean')['salary']  # 计算不同人员规模公司的平均薪资
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.subplots_adjust(bottom=0.15)
plt.bar(disSalarys.index, disSalarys.values)
plt.xticks(rotation=45)
plt.title('不同人员规模公司的薪资待遇对比')
plt.show()
