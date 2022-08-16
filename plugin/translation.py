import json
import os
import requests
import random
import re
from hashlib import md5
from flowlauncher import FlowLauncher
import pyperclip
import webbrowser


class Translation(FlowLauncher):
    __config_file = "config.json"
    appid = None
    appkey = None

    def __init__(self):
        with open(self.__config_file, 'r', encoding="utf-8") as f:
            content = f.read()
        dt = json.loads(content)
        self.appid = dt.get("appid", None)
        self.appkey = dt.get("appkey", None)
        super().__init__()


    def make_md5(self, s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()


    def query(self, translate):
        if not self.appid or not self.appkey:
            return self.nullConfig()
        if translate.strip():
            # 英文->中文 由英文翻译成中文
            from_lang = 'en'
            to_lang = 'zh'
            if re.findall("[\u4e00-\u9fa5]+", translate):
                from_lang, to_lang = to_lang, from_lang
            endpoint = 'https://api.fanyi.baidu.com'  # 固定内容,百度翻译开发者平台
            path = '/api/trans/vip/translate'  # 固定格式
            url = endpoint + path  # 拼接, 拼接后是网站的api接口(也是个网址,最好自行访问下感受感受)
            salt = random.randint(32768, 65536)  # 默认,官方要求的必填值
            sign = self.make_md5(self.appid + str(translate) + str(salt) + self.appkey)  # 同上
            # Build request
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            payload = {'appid': self.appid, 'q': translate, 'from': from_lang, 'to': to_lang, 'salt': salt,
                       'sign': sign}
            # Send request  发送请求获取数据
            r = requests.post(url, params=payload, headers=headers)
            result = r.json()  # 解析获得的 json 数据
            data = result['trans_result'][0]['dst']
            return [
                {
                    "title": data,
                    "subTitle": "点击复制到剪切板",
                    "icoPath": "assets/translate.png",
                    "jsonRPCAction": {
                        "method": "copy",
                        "parameters": [result['trans_result'][0]['dst']]
                    },
                    "score": 0
                }
            ]
        else:
            return self.context_menu(None)

    def context_menu(self, data):
        return [
            {
                "title": "直接输入内容可以翻译",
                "subTitle": "会自动识别输入语言，进行英汉互译",
                "icoPath": "assets/translate.png",  # related path to the image
                "jsonRPCAction": {
                    "method": "open_url",
                    "parameters": ["https://github.com/yifishyu/Flow.Launcher.Plugin.BaiDuTranslate"]
                },
                "score": 0
            }
        ]

    def nullConfig(self):
        return [
            {
                "title": "没有配置appid信息",
                "subTitle": "点击编辑配置，同时打开百度开放平台，查看信息",
                "icoPath": "assets/translate.png",  # related path to the image
                "jsonRPCAction": {
                    "method": "open_file",
                    "parameters": ["https://api.fanyi.baidu.com/manage/developer"]
                },
                "score": 0
            }
        ]

    def open_url(self, url):
        webbrowser.open(url)

    def open_file(self, url):
        os.startfile(self.__config_file)
        self.open_url(url)

    def copy(self, data):
        pyperclip.copy(data)


if __name__ == '__main__':
    # 手动录入翻译内容，q存放
    source = "please input the word you want to translate:"
    # source = "理解不到"
    t = Translation()
    q = t.query(source)
    print("原句:" + source)
    print(q)
