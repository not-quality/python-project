# 微信消息数据分析工具
# 功能：导入微信消息CSV文件，进行消息统计和关键词分析，并生成可视化图表
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 配置中文显示字体（Windows系统）
CHINESE_FONT = FontProperties(family='Microsoft YaHei')
from collections import Counter
import re
import os

def load_wechat_data(file_path):
    """
    加载微信消息CSV数据
    :param file_path: CSV文件路径
    :return: 包含消息数据的DataFrame或None（加载失败时）
    """
    try:
        # 使用utf-8-sig编码读取，支持包含BOM的CSV文件
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        print(f"成功加载数据：{len(df)} 条消息")
        return df
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 不存在")
        return None
    except Exception as e:
        print(f"加载数据时出错：{str(e)}")
        return None

def analyze_message_frequency(df):
    """
    分析消息发送频率和用户活跃度
    :param df: 包含微信消息的DataFrame
    """
    if df is None or df.empty:
        print("没有数据可供分析")
        return

    # 1. 总体统计
    total_messages = len(df)
    earliest_time = df['时间'].min()
    latest_time = df['时间'].max()
    print(f"\n=== 总体消息统计 ===")
    print(f"总消息数：{total_messages}")
    print(f"时间范围：{earliest_time} 至 {latest_time}")

    # 2. 用户活跃度统计
    user_counts = df['用户名'].value_counts()
    print(f"\n=== 用户活跃度排名 ===")
    print(user_counts.to_string())

    # 3. 生成用户活跃度柱状图
    plt.figure(figsize=(10, 6))
    user_counts.plot(kind='bar', color='skyblue')
    plt.title('用户消息数量统计', fontproperties=CHINESE_FONT)
    plt.xlabel('用户名', fontproperties=CHINESE_FONT)
    plt.ylabel('消息数', fontproperties=CHINESE_FONT)
    plt.xticks(rotation=45, ha='right', fontproperties=CHINESE_FONT)
    plt.tight_layout()
    
    # 保存图表
    output_dir = os.path.dirname(os.path.abspath(__file__))
    user_chart_path = os.path.join(output_dir, '用户活跃度统计.png')
    plt.savefig(user_chart_path)
    print(f"\n用户活跃度图表已保存至：{user_chart_path}")
    plt.close()

def analyze_keywords(df, target_keywords=None):
    """
    分析消息内容中的关键词出现频率
    :param df: 包含微信消息的DataFrame
    :param target_keywords: 要分析的关键词列表，默认为None（分析所有包含'关键词'的内容）
    """
    if df is None or df.empty:
        print("没有数据可供分析")
        return

    # 1. 准备关键词列表
    if target_keywords is None:
        # 从wechat_get.py中获取关键词（这里使用默认关键词）
        target_keywords = ["关键词"]
    print(f"\n=== 关键词分析 ({', '.join(target_keywords)}) ===")

    # 2. 统计关键词出现次数
    # 明确指定需要统计的三个关键词
    target_keywords = ["关键词1", "关键词2", "关键词3"]
    # 初始化关键词计数器，确保所有目标关键词都被包含（即使计数为0）
    keyword_counter = Counter({kw: 0 for kw in target_keywords})
    content_series = df['内容'].dropna()
    
    for content in content_series:
        # 对每条消息检查所有关键词
        for keyword in target_keywords:
            # 使用正则表达式进行不区分大小写的匹配
            matches = re.findall(re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE), str(content))
            keyword_counter[keyword] += len(matches)

    # 3. 输出关键词统计结果
    for keyword, count in keyword_counter.items():
        print(f"{keyword}: {count} 次出现")

    # 4. 生成关键词频率饼图
    if keyword_counter.total() > 0:
        plt.figure(figsize=(8, 8))
        # 按固定顺序排序关键词，确保颜色与关键词对应
        sorted_items = sorted(keyword_counter.items(), key=lambda x: target_keywords.index(x[0]))
        labels = [item[0] for item in sorted_items]
        sizes = [item[1] for item in sorted_items]
        
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['lightgreen', 'lightblue', 'orange'], textprops={'fontproperties': CHINESE_FONT})
        plt.title('关键词出现频率分布', fontproperties=CHINESE_FONT)
        
        # 保存图表
        output_dir = os.path.dirname(os.path.abspath(__file__))
        keyword_chart_path = os.path.join(output_dir, '关键词频率统计.png')
        plt.savefig(keyword_chart_path)
        print(f"关键词频率图表已保存至：{keyword_chart_path}")
        plt.close()
    else:
        print("未找到任何关键词出现记录")

def analyze_time_pattern(df):
    """
    分析消息发送的时间模式
    :param df: 包含微信消息的DataFrame
    """
    if df is None or df.empty:
        print("没有数据可供分析")
        return

    # 1. 转换时间列为datetime格式
    df['时间'] = pd.to_datetime(df['时间'], format='%Y-%m-%d %H:%M:%S')
    
    # 2. 提取小时信息并统计
    df['小时'] = df['时间'].dt.hour
    hourly_counts = df['小时'].value_counts().sort_index()
    
    # 3. 生成小时分布柱状图
    plt.figure(figsize=(12, 6))
    hourly_counts.plot(kind='bar', color='salmon')
    plt.title('消息发送时间分布（小时）', fontproperties=CHINESE_FONT)
    plt.xlabel('小时', fontproperties=CHINESE_FONT)
    plt.ylabel('消息数', fontproperties=CHINESE_FONT)
    plt.xticks(range(24))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # 保存图表
    output_dir = os.path.dirname(os.path.abspath(__file__))
    time_chart_path = os.path.join(output_dir, '消息时间分布.png')
    plt.savefig(time_chart_path)
    print(f"消息时间分布图表已保存至：{time_chart_path}")
    plt.close()

def main():
    # 1. 配置文件路径（与wechat_get.py保持一致）
    current_dir = os.path.abspath(os.path.dirname(__file__))
    file_dir = os.path.join(current_dir, '微信信息')
    csv_file = os.path.join(file_dir, '接收数据.csv')
    
    # 2. 加载数据
    print(f"正在从 {csv_file} 导入数据...")
    df = load_wechat_data(csv_file)
    
    # 3. 执行各项分析
    if df is not None and not df.empty:
        analyze_message_frequency(df)
        analyze_keywords(df)
        analyze_time_pattern(df)
        print("\n=== 数据分析完成 ===")
    else:
        print("无法进行数据分析，数据加载失败或数据为空")

if __name__ == "__main__":
    main()