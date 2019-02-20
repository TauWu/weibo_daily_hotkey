# -*- coding: utf-8 -*-

from util.base.config import ConfigReader

class ConfigCenter(object):

    @staticmethod
    def RedisConfig():
        k = ['host', 'port']
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
