# -*- coding: utf-8 -*-
# Cronjob for Weibo's hotkey upload system.

from cronjob.crawler.hotkey_fetcher import HotkeyFetcher
from util.constant.enum import ENUM_DATATYPE

if __name__ == "__main__":
    fetcher = HotkeyFetcher()
    data = fetcher.get_data(ENUM_DATATYPE["json"])
    print(data)
