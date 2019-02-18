# -*- coding: utf-8 -*-
# base module for config parser.

from configparser import ConfigParser

class Config(object):

    def __init__(self, path_name='conf', file_name='base.cfg', section_name='base'):
        self.filepath = '%s/%s'%(path_name, file_name)
        self.section = section_name
        self.config = ConfigParser()
        self.config.read(self.filepath)

    def use_section(self, section):
        self.section = section
    
    def add_section(self, section):
        self.config.add_section(section)
        self.use_section(section)

    def set_kv(self, k, v):
        self.config.set(self.section, k, str(v))
        self.save

    def read(self, k):
        return self.config[self.section][k]

    def readall(self):
        return {k:self.read(k) for k in self.config[self.section]}

    @property
    def save(self):
        self.config.write(open(self.filepath, 'w'))

class ConfigReader(Config):

    @staticmethod
    def read_section_key(path_name='conf', file_name='base.cfg', section_name='base', *k, **kwargs):
        
        conf = Config(path_name=path_name, file_name=file_name, section_name=section_name)

        if 'all' in kwargs.keys() and kwargs['all']:
            return conf.readall()
        elif len(k) == 1:
            return conf.read(k[0])
        else:
            return {ik:conf.read(ik) for ik in k}