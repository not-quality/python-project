import pandas as pd
import os

# os.chdir：将路径定位到该目录
os.chdir('./excel_auto')
# 引入数据
data = pd.read_excel('./全球票房最高电影TOP15_2025.xlsx')
# 按名称读取
# df_sheet1 = pd.read_excel('file.xlsx', sheet_name='Sheet1')
# 按索引读取（0表示第一个工作表）
# df_first = pd.read_excel('file.xlsx', sheet_name=0)
# 一次性读取所有工作表
# all_sheets = pd.read_excel('your_file.xlsx', sheet_name=None)

# 数据读取
print(data)
print(data['类型标签'])

# 末尾添加新列，其中apply(lambda x:x.func()) 表示将列表中的每个元素单独提取为x,并对x元素运用func()方法
data['类型标签-1'] = data['类型标签'].apply(lambda x:x.split('/')[0])

# 查看单标签元素种类
print(data['类型标签-1'].unique())
# 查看多标签元素种类
type_list = set(m for i in data['类型标签'] for m in i.split('/'))
print(type_list)
# 注：其中unique()和set()都用于去重

# 筛选特定标签数据
print(data[data['类型标签-1'] == '动画'])
print(data[data['类型标签-1'].str.contains('科幻')])


# 写入器保存数据
with pd.ExcelWriter('temp_1.xlsx') as writer:  
    for i in data['类型标签-1'].unique():
        # 筛选数据并写入指定工作表
        data[data['类型标签-1'] == i].to_excel(
            # 指定写入器
            writer,          
            # 工作表名=类型名
            sheet_name=i,    
            # 可选：不保存行索引
            index=False      
        )

with pd.ExcelWriter('temp_2.xlsx') as writer:  
    for ty in type_list:
        data[data['类型标签'].str.contains(ty)].to_excel(
            # 指定写入器
            writer,          
            # 工作表名=类型名
            sheet_name=ty,    
            # 可选：不保存行索引
            index=False      
        )



