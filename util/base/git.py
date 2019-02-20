from git import Repo

class Git(object):

    def __init__(self, path):
        self.__repo     = Repo(path)
        self.__index    = self.__repo.index
        self.__remote   = self.__repo.remote()

    @property
    def is_bare(self):
        return self.__repo.bare

    @property
    def is_dirty(self):
        return self.__repo.is_dirty()
    
    @property
    def active_branch(self):
        return "{branch}".format(branch=self.__repo.active_branch)

    def add(self, *path):
        self.__index.add(path)
    
    def remove(self, *path):
        self.__index.remove(path)

    def commit(self, msg):
        self.__index.commit(msg)

    def pull(self):
        self.__remote.pull()

    def push(self):
        self.__remote.push()
