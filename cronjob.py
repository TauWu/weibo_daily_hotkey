# -*- coding: utf-8 -*-
# Cronjob for Weibo's hotkey upload system.

from cronjob.crawler.hotkey_fetcher import HotkeyFetcher
from cronjob.datacenter.cache.cache_controller import CacheController

from util.constant.enum import *
from util.base.time import Time

if __name__ == "__main__":
    now = Time.now_timestamp()

    fetcher = HotkeyFetcher()
    data = fetcher.get_data(ENUM_DATATYPE_JSON, limit=10)

    cacheController = CacheController()
    cacheController.insert_cache(now, data)
