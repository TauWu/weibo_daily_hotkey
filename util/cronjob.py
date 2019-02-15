# -*- coding: utf-8 -*-
# Cronjob for Weibo's hotkey upload system.

from cronjob.crawler.hotkey_fetcher import HotkeyFetcher
from util.constant.enum import *

if __name__ == "__main__":
    fetcher = HotkeyFetcher()
    data = fetcher.get_data(ENUM_DATATYPE_JSON, limit=10)
    print(data)
