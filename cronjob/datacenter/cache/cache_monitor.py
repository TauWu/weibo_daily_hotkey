# -*- coding: utf-8 -*-

from util.base.redis import Redis
import json

class CacheMonitor(object):

    def __init__(self, db=0):
        self.cache = Redis(db)
    
    def has_key(self, prefix="", hotkey=""):
        has = self.cache.exists(prefix+":"+hotkey)
        if has is None:
            return False
        if has == 0:
            return False
        return True
    
    def set_hotkey(self, prefix="", hotkey="", idx=0, amount=0, tm=0, expire=0):
        k = prefix+":"+hotkey
        self.cache.hset(k, "idx", idx)
        self.cache.hset(k, "amount", amount)
        self.cache.hset(k, "timestamp", tm)
        if expire > 0:
            self.cache.expire(k, expire)

    def get_hotkey(self, prefix="", hotkey="", key=""):
        k = prefix+":"+hotkey
        if not self.has_key(prefix, hotkey):
            return None
        return self.cache.hget(k, key)
