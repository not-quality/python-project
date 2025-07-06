# %%
import requests
import json
import re
from moviepy import VideoFileClip, AudioFileClip

# B站视频链接（凡人修仙传-128）
url = "https://www.bilibili.com/bangumi/play/ep1231536?from_spmid=666.25.episode.0"
headers = {
    "referer": "https://www.bilibili.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
}
res = requests.get(url, headers=headers)
print(res)
html_data = res.text

# %%
playinfo_match = re.findall(r"console.log\('responseData',(.*)", html_data)[0][:-1]
# print(playinfo_match)

# %%
json_data = json.loads(playinfo_match)
# vip试看地址
# print(json_data["data"]["result"]["video_info"]["durl"][0]["url"])
# print(json_data["data"]["result"]["video_info"]["dash"]["video"][0]["base_url"])
# print(json_data["data"]["result"]["video_info"]["dash"]["audio"][0]["base_url"])

# %%
# vip试看爬取
# res = requests.get(json_data["data"]["result"]["video_info"]["durl"][0]["url"], headers=headers)
# 非vip视频爬取
res_video = requests.get(json_data["data"]["result"]["video_info"]["dash"]["video"][0]["base_url"], headers=headers)
res_audio = requests.get(json_data["data"]["result"]["video_info"]["dash"]["audio"][0]["base_url"], headers=headers)
# 完整链接下载vip视频（凡人修仙传-150）
# res_video = requests.get('https://cn-zjhz-cm-01-07.bilivideo.com/upgcxcode/63/53/30857235363/30857235363_sr1-1-100035.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&mid=400892715&deadline=1751774276&oi=1974965948&platform=pc&trid=0000b7283793458b4db1b286cb12c3b0b97p&nbs=1&gen=playurlv3&os=bcache&og=hw&upsig=aa8e899e9e1fea279b0199012f1dc7eb&uparams=e,uipk,mid,deadline,oi,platform,trid,nbs,gen,os,og&cdnid=4065&bvc=vod&nettype=0&bw=16526028&build=0&dl=0&f=p_0_0&agrr=1&buvid=54F9AD58-0B07-7C9A-3769-35CF1E08325B03144infoc&orderid=0,4', headers=headers)
# res_audio = requests.get('https://xy42x4x57x133xy.mcdn.bilivideo.cn:4483/upgcxcode/63/53/30857235363/30857235363-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&platform=pc&gen=playurlv3&og=cos&trid=0000b7283793458b4db1b286cb12c3b0b97p&os=mcdn&mid=400892715&deadline=1751774276&oi=1974965948&nbs=1&upsig=c423cebb9a37493b4f5cc42f7b0f2430&uparams=e,uipk,platform,gen,og,trid,os,mid,deadline,oi,nbs&mcdnid=50026545&bvc=vod&nettype=0&bw=213065&build=0&dl=0&f=p_0_0&agrr=1&buvid=54F9AD58-0B07-7C9A-3769-35CF1E08325B03144infoc&orderid=0,4', headers=headers)

# print(res_video)
# print(res_audio)

with open("1.mp4", "wb") as f:
    f.write(res_video.content)
with open("1.mp3", "wb") as f:
    f.write(res_audio.content)

# %%
# 加载视频文件
video_clip = VideoFileClip("1.mp4")
# 加载音频文件
audio_clip = AudioFileClip("1.mp3")
# 将音频合并到视频轨道
final_clip = video_clip.with_audio(audio_clip)
# 保存合并后的完整视频（使用H.264编码确保兼容性）
final_clip.write_videofile("完整视频.mp4", codec="libx264", audio_codec="aac")
print("视频和音频合并完成，输出文件：完整视频.mp4")
