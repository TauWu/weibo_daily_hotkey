# -*- coding: utf-8 -*-

from redis import Redis as RawRedis
from redis import ConnectionPool
import json

from util.configcenter.config_center import ConfigCenter

def equal(object1, object2):
    return True if object1 == object2 else False

class Redis(object):

    def __init__(self, db):
        self.conf = ConfigCenter.RedisConfig()

        host = self.conf['host']
        port = self.conf['port']
        passwd = self.conf['passwd']

        self.db = db
        self.__pool = ConnectionPool(host=host, port=port, db=self.db, password=passwd)
        self.__conn = RawRedis(connection_pool=self.__pool)
        
        print("*** Connect to redis-server succeed.")

    def rset(self, k, v):
        rval = self.rget(k)
        if rval is not None:
            try:
                rval = json.loads(rval)
            except Exception:
                pass
        
        if equal(v, rval):
            print("db{}:set【{} => <=】".format(self.db, k))
            return

        elif rval is None:
            print("db{}:set【{} () => {}】".format(self.db, k, v))
        else:
            print("db{}:set【{} {} => {}】".format(self.db, k, rval, v))

        if isinstance(v, (dict, list)):
            v = json.dumps(v)

        self.__conn.set(k, v)
        return

    def rget(self, k):
        try:
            res = self.__conn.get(k)
            return None if res is None else res.decode('utf-8')
        
        except Exception as e:
            print("*** Get value from redis failed.", k, e)
            return None

    def delete(self, k):
        self.__conn.delete(k)
        print("*** db%s:删除【%s】的缓存"%(self.db, k))

    @property
    def dbsize(self):
        return self.__conn.dbsize()

    def pipeset(self, lists):

        pipe = self.__conn.pipeline(transaction=True)

        for list_detail in lists:
            k = list(list_detail.keys())[0]
            v = list_detail[key]
            self.rset(k, v)

        pipe.execute()

    @property
    def scan_iter(self):
        ''' Scan Redis db to iterator.
        '''
        for k in self.__conn.keys():
            yield k.decode('utf-8'), self.rget(k)

    def __update_dict_to_redis__(self, k, v):
        ''' __update_dict_to_redis__
        Merge dict rather than replace it.
        '''
        if self.rget(k) is not None:
            bf_val = self.rget(k)
            try:
                bf_val = json.loads(bf_val)
                bf_val = dict(bf_val, **v)
                self.rset(k, bf_val)
            except Exception as e:
                print("__update_dict_to_redis__ failed.", e)
                pass
        else:
            self.rset(k, v)
