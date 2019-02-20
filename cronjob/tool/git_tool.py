# -*- coding: utf-8 -*-

from util.base.git import Git
from util.base.time import Time

from util.configcenter.config_center import ConfigCenter

class GitTool(object):

    def __init__(self):
        conf = ConfigCenter.GitConfig()
        self.git = Git(conf['path'])

    def __check_status__(self):
        if self.git.active_branch != "master":
            raise ValueError("Active branch is not master.")
        if self.git.is_bare:
            raise ValueError("This repo is bare.")

    def push_data(self):

        conf = ConfigCenter.GitConfig()
        filepath = conf['filepath'].split(',')
        msg = "Auto commit for %s."%(Time.now_date_str())
        err = self.push(*filepath)
        if err is not None:
            print(err)

    def push(self, *filepath, msg):

        try:
            self.__check_status__()
        except ValueError as err:
            return 'value err: {err}'.format(err=err)
        except Exception as e:
            return 'unknown err: {err}'.format(err=err)
        else:
            self.git.pull()
            #TODO check if conflicts exists.
            self.git.add(*filepath)
            self.git.commit(msg)
            self.git.push()
            return None
