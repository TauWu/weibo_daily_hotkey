# -*- coding: utf-8 -*-
# 监控机器人，当出现爆炸新闻或者出现监控词的时候会自动推送到群内。

from cronjob.crawler.hotkey_fetcher import HotkeyFetcher
from cronjob.datacenter.cache.cache_controller import CacheController
from util.configcenter.config_center import ConfigCenter
from cronjob.tool.qywx import QYWX, MSG_TYPE_MARKDOWN


from util.constant.enum import *
from util.base.time import Time

if __name__ == "__main__":
    now = Time.now_timestamp()

    fetcher = HotkeyFetcher()
    data = fetcher.get_data(ENUM_DATATYPE_JSON, limit=10)

    # cacheController = CacheController()
    # cacheController.insert_cache(now, data)
    print(now, data)
