# Flow.Launcher.Translation

## 描述

一款使用在Flow Launcher中的翻译插件(当前只支持百度翻译中英互译)

## 使用方法

## 安放位置

将下载得到的 zip 文件解压后得到的文件放在 %AppData%/FlowLauncher/Plugins 目录下，之后重启Flow Launcher，最后在插件选项中开启该插件

### 注册

在[百度翻译开放平台]([百度翻译开放平台](https://fanyi-api.baidu.com/product/11))中注册成为使用者，获取百度翻译的 appid 和 key

### 配置

在插件的目录下的 `config.js` 文件中填写你的 appid 和 key，如果没有配置，第一次也会弹出配置文件，可以进行编辑

![config](https://i.postimg.cc/JhT1kVhy/config.png)

### 使用

中译英，`fy 苹果`

![中译英](https://i.postimg.cc/Kzy10y20/zhToEn.png)

英译中， `fy apple`

![英译中](https://i.postimg.cc/tgn6r5V4/entozh.png)

目前只支持中英互译， 且只能翻译单个词或单个句子
