# WEIBO DAILY HOTKEY

This repo will get hotkeys for sina weibo, and upload it to this github repo.

本项目会定期从新浪微博中获取热搜关键词，并将数据回传到本项目。


## NOTICE

本项目预期会在 [WeiboDaily](https://github.com/trim-troop/weibo_daily) 进行重构，施工中🚧

## DATA

[Click Here](./data/data.md) to read daily hotkey data.

[点击这里](./data/data.md)阅读每日微博热搜词数据。

## Requirements

### Softwares

```sh
apt-get install python3
apt-get install python3-pip
apt-get install redis-server
```

### Python Modules
```sh
pip3 install requests
pip3 install GitPython
pip3 install lxml
pip3 install redis
```

## Crawler Info

### Base URL

https://s.weibo.com/top/summary?cate=realtimehot

*Shouldn't login.*

### Parser

lxml module for python and regexp tools.

### Database

Redis for daily data and MySQL for API data(//TODO).

## Project Menu Tree

```
--
 |/conf 配置文件
 |/data 爬取数据
 |/util 工具函数
 |---->|/base 基础库
 |---->|/configcenter 配置中心
 |---->|/constant 常量
 |/cronjob 定时任务
 |---->|/datacenter 数据中心
 |-------->|/database 数据库数据
 |-------->|/cache 缓存数据
 |---->|/crawler 爬虫中心
 |---->|/tool 定时工具
 |/service //TODO 服务中心
 |cronjob.py 定时抓取、数据比对脚本
 |update.py 定时更新 repo 脚本
 |update_code.py 手动更新 github 代码脚本 //FIXME (git add . 的实现有 bug)
 -------------------------------
 ```
