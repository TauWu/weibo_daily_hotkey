# WEIBO DAILY HOTKEY

This repo will get hotkeys for sina weibo, and upload it to this github repo.

本项目会定期从新浪微博中获取热搜关键词，并将数据回传到本项目。

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
pip3 install PyGithub
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
 |/cronjob 定时任务
 |---->|/datacenter 数据中心
 |-------->|/database 数据库数据
 |-------->|/cache 缓存数据
 |---->|/crawler 爬虫中心
 |/service //TODO 服务中心
 -------------------------------
 ```
