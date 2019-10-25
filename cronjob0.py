# -*- coding: utf-8 -*-
# Cronjob for Weibo's hotkey upload system.

from cronjob.crawler.hotkey_fetcher import HotkeyFetcher
from cronjob.datacenter.cache.cache_controller import CacheController

from util.constant.enum import *
from util.base.time import Time

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

    cacheController = CacheController()
    cacheController.insert_cache(now, data)
