# -*- coding: utf-8 -*-

from util.base.redis import Redis

import json

class CacheController(object):

    def __init__(self, db=0):
        self.cache = Redis(db)

    def insert_cache(self, timestamp, new_hotkey_json):
        '''insert_cache
        1. 最近一条数据存入当前时间戳为 key 的 json 中
        2. 一一比对将较大的热度数值对应的热词更新，取大不取小，存在 key = 0 的 json 中
        '''
        self.cache.rset(timestamp, new_hotkey_json)

        hotkeys_set = self.cache.rget(0)

        if hotkeys_set is None:
            self.cache.rset(0, new_hotkey_json)
        else:
            self.__update_cache__(new_hotkey_json)

    def __update_cache__(self, new_hotkey_json):
        today_hotkey_json = self.get_today_cache()

        today_hotkey_dict = dict()

        for hotkey in today_hotkey_json:
            today_hotkey_dict[hotkey['hotkey']] = hotkey

        for new_hotkey in new_hotkey_json:

            if new_hotkey['hotkey'] in today_hotkey_dict.keys():
                if int(new_hotkey['amount']) > int(today_hotkey_dict[new_hotkey['hotkey']]['amount']):
                    today_hotkey_dict[new_hotkey['hotkey']] = new_hotkey
            else:
                today_hotkey_dict[new_hotkey['hotkey']] = new_hotkey

        self.cache.rset(0, list(today_hotkey_dict.values()))

    def clear_today_cache(self):
        self.cache.delete(0)
        
    def get_today_cache(self):
        return self.get_cache(0)

    def get_cache(self, timestamp):
        return json.loads(self.cache.rget(timestamp))
        