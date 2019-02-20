# -*- coding: utf-8 -*-

from sys import argv
from cronjob.datacenter.cache.cache_controller import CacheController
from cronjob.datacenter.file.file import sort_hotkey_order_by_amount
from util.base.time import TimeTranslator

if __name__ == "__main__":
    cache_controller = CacheController(0)
    cache = cache_controller.get_today_cache()
    ordered_cache = sort_hotkey_order_by_amount(cache)

    for data in ordered_cache:

        datetime = TimeTranslator.timestamp2datetime(data['time'])

        print("{}|{}|{}|{}|{}".format(
            datetime.time(), data['hotkey'], data['amount'], 
            '' if len(data['flag']) == 0 else data['flag'][0], 
            '' if len(data['emoji']) == 0 else data['emoji'][0])
        )