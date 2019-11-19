# -*- coding: utf-8 -*-
# Cronjob for Weibo's hotkey upload system.

from cronjob.crawler.hotkey_fetcher import HotkeyFetcher
from cronjob.datacenter.cache.cache_controller import CacheController
from cronjob.datacenter.cache.cache_monitor import CacheMonitor
from util.configcenter.config_center import ConfigCenter
from cronjob.tool.qywx import QYWX, MSG_TYPE_MARKDOWN

from util.constant.enum import *
from util.base.time import Time, TimeTranslator

import base64

if __name__ == "__main__":

    now = Time.now_timestamp()
    fetcher = HotkeyFetcher(headers={
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "Upgrade-Insecure-Requests": "1"
        })

    data = fetcher.get_data(ENUM_DATATYPE_JSON, limit=10)

    cfg = ConfigCenter.MonitorConfig()
    sender = QYWX()

    cacheController = CacheController()
    cacheController.insert_cache(now, data)

    robotmsg = "## 微博热搜实时监控\n"
    cacheMonitor = CacheMonitor()
    for idx, d in enumerate(data):
        hkey = d["hotkey"]
        bs64hkey = base64.b64encode(hkey.encode("utf-8")).decode("utf-8")

        # 检查是否有监控词
        for mkey in cfg["keys"]:
            if hkey.find(mkey) == -1:
                continue

            #满足 key 存在且 idx 没有上升，不发送消息
            if cacheMonitor.has_key("hint", bs64hkey):
                raw_idx = int(cacheMonitor.get_hotkey("hint", bs64hkey, "idx"))
                if raw_idx <= idx + 1:
                    continue

            cacheMonitor.set_hotkey("hint", bs64hkey, idx=idx+1, amount=int(d["amount"]), tm=d["time"], expire=24*3600)
            robotmsg += f'### 命中监控词！{mkey} \n NO.{idx+1}| {hkey} \n 热度: {d["amount"]} 时间: {TimeTranslator.timestamp2datetime(d["time"])}\n'

        # 检查是否有超高热度的话题
        if int(d["amount"]) < int(cfg["hot_count"]):
            continue

        # 超高热度话题每 1000W 热度推送一次
        if cacheMonitor.has_key("hot", bs64hkey):
            raw_amount = cacheMonitor.get_hotkey("hot", bs64hkey, "amount")
            if raw_amount >= int(d["amount"]) - int(cfg["hot_count"]):
                continue

            robotmsg += f'### 爆！NO.{idx+1}| {hkey} \n 热度: {d["amount"]} 时间: {TimeTranslator.timestamp2datetime(d["time"])}\n'

    if len(robotmsg) > 20:
        sender.send_msg(msg_type=MSG_TYPE_MARKDOWN, content=robotmsg)
