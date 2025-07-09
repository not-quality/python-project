from DrissionPage import Chromium
import requests
import re
import time
import random

tab = Chromium().latest_tab
# 开始监听，指定获取包含该文本的数据包
tab.listen.start('/aweme/post/')
# 访问网址，这行产生的数据包不监听
tab.get('https://www.douyin.com/user/MS4wLjABAAAA3VU80liJguQ9LB7qmEAV_0zbsNRl4SfkSOKV37vPVXgQPw-fJ2w7s4g-gfkPdSLm?from_tab_name=main&vid=7524636798996204809')
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Referer": "https://www.douyin.com/",
    "Cookie": "douyin.com; enter_pc_once=1; UIFID_TEMP=e71d819f1cb72e7166823ce125547a3e5a83b631a52f7c0b3c34cd9714dd602d16588596dd88de521d6d1e2a055b22502b0b3eee93b3ab6b431daaa75fab812cf64eeedffd7760d08cb68ae3ff591ffd; hevc_supported=true; dy_swidth=1536; dy_sheight=864; fpk1=U2FsdGVkX19qfS0XVrUhiA5W3gMG1bnSi0hX/yyNQ1jxrq32x34E6FtZFifq5SlG0vMPc8EGt6F7VeMWL9j9nQ==; fpk2=0fe6feb54289f4c67027ec06cc2131f8; odin_tt=e41cccb2218b9e73964853896ba3352721359e2e4f8249ee0531fb960147556e1977271df0923c4bfd83722c1f687d7f441187ccc257e665f0eb2379c972d11e0c02a652e7c2e8503ae6e234baea60f6; xgplayer_user_id=793287326596; s_v_web_id=verify_mculgeya_1XqHmgjN_mqLY_46Kr_BJ1L_v6JKjRkEMwhn; UIFID=e71d819f1cb72e7166823ce125547a3e5a83b631a52f7c0b3c34cd9714dd602d16588596dd88de521d6d1e2a055b22501fed1e48ca489c5a7edcf695c0885c85f34a60681c5259e08e4daedca5b510b89a1d6d46392c56b47e2c6993821bcbd3caca6f84ca0405030bbae9d72dc5d5d0f3fa214416325e10f415e18fe39ec01010c1296c2724db37c0cd6ec5f5c50d4e28954c02dab8994b6df17f859eb2bde9; is_dash_user=1; passport_csrf_token=97fc83ddf2d4527470905493e2c75196; passport_csrf_token_default=97fc83ddf2d4527470905493e2c75196; __security_mc_1_s_sdk_cert_key=ea3f5518-470d-a203; __security_mc_1_s_sdk_sign_data_key_web_protect=7ed9ed50-431c-b8ac; __security_mc_1_s_sdk_crypt_sdk=7e4fa1f5-42cb-8880; bd_ticket_guard_client_web_domain=2; download_guide=%223%2F20250708%2F0%22; xgplayer_device_id=80427097544; WallpaperGuide=%7B%22showTime%22%3A1751989273303%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A22%2C%22cursor2%22%3A6%2C%22hoverTime%22%3A1751989866133%7D; __ac_nonce=0686d410f00594b971ccc; __ac_signature=_02B4Z6wo00f013QkfcQAAIDA6kDdVWWBic90BHlAALVv77; strategyABtestKey=%221751990544.07%22; douyin.com; xg_device_score=7.184352941176471; device_web_cpu_core=16; device_web_memory_size=8; architecture=amd64; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; sdk_source_info=7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e58272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e582729277672715a646971273f2763646976602729277f6b5a666475273f2763646976602729276d6a6e5a6b6a716c273f2763646976602729276c6b6f5a7f6367273f27636469766027292771273f27373d30323735373c3c34303234272927676c715a75776a716a666a69273f2763646976602778; bit_env=X25Jv8fLQq_sj3CNdPMtAuDkS3GvwkXOKNbe0dyHJA0qGSel9d2eI6v1otnxs3JEkbmUyHRyfXV8KUSn-mQ3eFXatctntAESbwNZxqjAszEYCZe5E7PQy0zZ4-gfxCVJJZdhuz4UpbzVVXrw5YrR1vvHPvXnXGO4CspObc_hlDKDYIqo5JWZFAQ5-CWTZJX9urREsFYvIRfZSFEpSJ9EwevILJ1lLhYwNpuNFQulckfnmDksDwBI49FVQB9ya3CIyhv_6SqQp1GOW5lm3ZiA8Xjdjl41rZNdIdXyjJkDaqz2RWJn5pQbeuOIracZx0jN2QD9Aic4uy6km9_dgg6AvO1hYCF-45XZU0hpVu48EBQG-R6E7lbe7Dh7w7LRCeVUTQZuErzLoRo-OcjWcoIJpLRej2dIU43247bwRtEm0WEyJfpVuFP23xcsWOoaEESWyGOR-b24cvAALF2hTsBzQOteL1246Lx_HW7B7YOp-lzL0Go6A82vx-1s3d0UM2zP; gulu_source_res=eyJwX2luIjoiODE4ZmQ4N2E4MDc2ZjQwYjA4ZjJiNjYwZTg5MGFhM2JmYTMyNTg1MzhhODVhZTBlYjZkM2M5YTZkNWU0ZDEzZCJ9; passport_auth_mix_state=gdpohcvsti32ovr0waxqb1va3a2nivlf; volume_info=%7B%22volume%22%3A0.6%2C%22isMute%22%3Afalse%2C%22isUserMute%22%3Afalse%7D; ttwid=1%7CJD7gczWwD4P5fuHiUGsVBB1N3kscvlyFGF_C31Dzi5c%7C1751992201%7C05eb52e520e4b53a456749bdf201cda4565425c337ff0c456969f5c5b57dc425; biz_trace_id=e4e7192f; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCT2crMXBZNjJBQnhLMVNiMzhieVRvR0JXbTliellOb25acUNxcEYzTUFITGhqY1Y5SnQ4anVxSVE3REdpbUdFd2ljamw4S1hnbXNYMytuQVJueGhpcE09IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; home_can_add_dy_2_desktop=%221%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A1%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; IsDouyinActive=false",
}
# 等待并获取一个数据包
# info = tab.listen.wait()
# 返回一个获取数据包的可迭代对象，每次循环可从中获取到的数据包。
for info in tab.listen.steps():
    json = info.response.body
    print("视频数量:",len(json["aweme_list"]))
    count = 0
    for temp in json["aweme_list"]:
        count += 1
        url = temp["video"]["play_addr"]["url_list"][0]
        title = temp["desc"]
        title = re.sub(r'#\S+\s*','',title)
        title = re.sub(r'@\S+\s*','',title)
        res = requests.get(url, headers=headers)
        print(res)
        print(title)
        print(f"进度:{len(json["aweme_list"])}/{count}")
        # print(url)

        # 视频保存
        # with open(f"{ title }.mp4", "wb") as f:
        #     f.write(res.content)
        #     print(title)

        # 随机时间
        delay = random.uniform(0.5, 1)
        time.sleep(delay)

    # 监听终止条件(不设置终止条件将一直监听下去)
    if count == len(json["aweme_list"]) == 20:
        break

# 关闭标签页
tab.close()