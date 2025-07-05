# 微信消息监控与CSV记录工具
# 功能：监控指定微信群聊，提取包含关键词的消息并写入CSV文件
# 实现机制：通过UI自动化获取微信消息，使用缓冲区机制处理高频消息写入
import os
import re
import subprocess
import time
import csv
import uiautomation as auto
from wxauto import *
from datetime import datetime  

# 配置参数区域 - 可根据实际需求修改以下参数
# 文件夹名称
FILE_FOLDER = '微信信息'

# 文件名工作簿
FILE_NAME = '接收数据.csv'

USERNAME='用户名'
TEXT='内容'
TIME='时间'

# 获取当前文件所在目录的绝对路径
current_dir = os.path.abspath(os.path.dirname(__file__))

# 文件夹的绝对路径
file_dir = os.path.join(current_dir, FILE_FOLDER)

# 文件名的绝对路径
file_path = os.path.join(file_dir, FILE_NAME)

# 检查文件是否存在并创建CSV文件
if not os.path.exists(file_path):
    # 创建新的CSV文件并写入标题行
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow([USERNAME, TEXT, TIME])

# 设置要搜索需要监控的用户ID、群号（备注）
WHO = "监控用户名"

# 设置要检查的关键词列表（包含任何一个关键词即匹配）
KEYWORD = ["关键词1", "关键词2", "关键词3"]

# 指定微信应用程序路径
APP_PATH = r"F:\Apply\common\WeChat\WeChat.exe"

# 打开微信应用程序
subprocess.Popen(APP_PATH)

# 创建 WeChat 实例
wx = WeChat()

# 在微信客户端中搜索指定关键词的聊天记录表
wx.B_Search.Click()
auto.SendKeys(WHO)
auto.SendKeys("{ENTER}")

# 绑定微信主窗口
wz = auto.WindowControl(serchDepth=1,className='WeChatMainWndForPC',Name='微信')

# 绑定会话控件
hh = wz.ListControl(Name='会话')

# 绑定“我的群”
hl=hh.ListItemControl(Name=WHO)

# 时间文本
wf = hl.TextControl(searchDepth=4)
# 消息数字文本
wt = hl.TextControl(searchDepth=2)
# 查找多个关键词
def check_keywords(text, keywords):
    """
    检查文本中是否包含指定关键词列表中的任何关键词
    :param text: 待检查的文本字符串
    :param keywords: 关键词列表（区分大小写）
    :return: 如果包含任何关键词则返回True，否则返回False
    """
    text_lower = text.lower()
    for keyword in keywords:
        pattern = re.compile(keyword, re.IGNORECASE)
        match = re.search(pattern, text_lower)
        if match:
            return True
    return False

# 移除空格保留换行符
def remove_extra_spaces_in_list(lst):
    """
    移除列表中字符串元素的多余空格，保留换行符
    :param lst: 包含字符串的列表
    :return: 清理后的字符串列表
    """
    cleaned_list = []
    for item in lst:
        cleaned_item = re.sub(r' +', ' ', item)
        cleaned_list.append(cleaned_item)
    return cleaned_list

def process_buffer(buffer, file_path):
    """
    处理消息缓冲区，将累积的消息批量写入CSV文件
    :param buffer: 消息缓冲区列表，每个元素为[name, text, time]格式
    :param file_path: CSV文件路径
    :return: 清空后的缓冲区（空列表）
    """
    if buffer:
        with open(file_path, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(buffer)
        print(f'已完成{len(buffer)}条信息写入!')
        return []
    return buffer

# 打印最后一条消息
def print_last_message():
    """
    主监控函数：持续监控微信群消息，提取符合条件的消息并写入CSV
    实现逻辑：
    1. 初始化微信客户端并定位目标群聊
    2. 循环监控未读消息提示或群聊消息列表
    3. 对新消息进行关键词检查和数据清洗
    4. 通过缓冲区机制批量写入CSV文件
    """
    last_msg = None
    isnotext=True
    message_buffer = []  # 消息缓冲区
    # 立即获取内容控件的最后一个消息
    msgs = wx.GetAllMessage()
    if not msgs:
        print("No messages found.")
        return
    msgsname = msgs[-1][0]
    msgstext = msgs[-1][1]
    while True:
        if wt.Exists(0):
            # 查找文本控件
            while not wt.Exists(0):  # 忽略超时出错中断，一直执行空语句
                pass
            # 检查是否存在未读消息
            if wt.Name:
                # 获取消息列表
                msg_list = wz.ListControl(Name='消息').GetChildren()
                # 获取最后一条消息
                new_msg = msg_list[-1].Name
                if new_msg != last_msg:
                    # 检查最后一条消息是否包含指定关键词
                    istrue = check_keywords(new_msg, KEYWORD)
                    if istrue:
                        # 将匹配到的消息添加到列表
                        msgs = wx.GetAllMessage()
                        msgsname = msgs[-1][0]
                        msgstext = msgs[-1][1]
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        # 处理单条新消息
                        cleaned_name = remove_extra_spaces_in_list([msgsname])[0]
                        cleaned_text = remove_extra_spaces_in_list([msgstext])[0]

                        # 过滤NaN值并添加到缓冲区
                        if str(cleaned_name) != 'nan' and str(cleaned_text) != 'nan':
                            message_buffer.append([cleaned_name, cleaned_text, current_time])
                        last_msg = new_msg
                    else:
                        print('信息中无匹配的关键词')
                else:
                    print('信息等待中...')
            else:
                print('未找到未读消息')

            # 处理缓冲区消息
            message_buffer = process_buffer(message_buffer, file_path)
            # 当没有未读消息时，等待新消息到达
            time.sleep(1)
            # 检查是否有新消息到达，如果没有，则继续等待新消息
            while wt.Name == last_msg:
                time.sleep(1)
        else:
            while not wf.Exists(0):  # 忽略超时出错
                pass
            # 检查是否存在我的群的文本列表
            if wf.Name:
                msg_list = wz.ListControl(Name='消息').GetChildren()
                # 获取最后一条消息
                new_msg = msg_list[-1].Name
                if new_msg != last_msg:
                    # 检查最后一条消息是否包含指定关键词
                    istrue = check_keywords(new_msg, KEYWORD)
                    if istrue:
                        msgs = wx.GetAllMessage()
                        msgsname = msgs[-1][0]
                        msgstext = msgs[-1][1]
                        # 将匹配到的消息添加到列表
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        # 处理单条新消息
                        cleaned_name = remove_extra_spaces_in_list([msgsname])[0]
                        cleaned_text = remove_extra_spaces_in_list([msgstext])[0]

                        # 过滤NaN值并添加到缓冲区
                        if str(cleaned_name) != 'nan' and str(cleaned_text) != 'nan':
                            message_buffer.append([cleaned_name, cleaned_text, current_time])
                        last_msg = new_msg
                    else:
                        # 不管找不找到匹配关键词的内容都执行一次写入操作后续就不在写入，写入的内容排在列表第一位
                        if isnotext:
                            # 处理并写入单条初始消息
                            cleaned_name = remove_extra_spaces_in_list([msgsname])[0]
                            cleaned_text = remove_extra_spaces_in_list([msgstext])[0]
                            if str(cleaned_name) != 'nan' and str(cleaned_text) != 'nan':
                                message_buffer.append([cleaned_name, cleaned_text, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                            isnotext=False
                        print('信息中无匹配的关键词')
                else:
                    print('信息等待中...')
            else:
                print('找不到{wf.Name}会话窗口')
            # 处理缓冲区消息
            message_buffer = process_buffer(message_buffer, file_path)
            time.sleep(1)
            # 检查是否有新消息到达，如果没有，则继续等待新消息
            while wf.Name == last_msg:
                time.sleep(1)

# 调用函数开始打印最后一条消息
print_last_message()