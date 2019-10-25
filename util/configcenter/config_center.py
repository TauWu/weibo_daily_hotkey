# -*- coding: utf-8 -*-

from util.base.config import ConfigReader

class ConfigCenter(object):

    @staticmethod
    def RedisConfig():
        k = ['host', 'port', 'passwd']
        return ConfigReader.read_section_key('conf', 'base.cfg', 'redis', *k)

    @staticmethod
    def DatabaseConfig():
        k = ['host', 'port', 'user', 'passwd']
        return ConfigReader.read_section_key('conf', 'base.cfg', 'database', *k)

    @staticmethod
    def FileConfig():
        k = ['path']
        return ConfigReader.read_section_key('conf', 'base.cfg', 'file', *k)
        
    @staticmethod
    def GitConfig():
        k = ['path', 'filepath']
        return ConfigReader.read_section_key('conf', 'base.cfg', 'git', *k)

    @staticmethod
    def QYWXConfig():
        k = ['tokens']
        return ConfigReader.read_section_key('conf', 'base.cfg', 'qywx', *k).split(",")

    @staticmethod
    def MonitorConfig():
        k = ['keys', 'hot_count']
        cfg = ConfigReader.read_section_key('conf', 'base.cfg', 'monitor', *k)
        cfg["keys"] = cfg["keys"].split(",")
        return cfg
