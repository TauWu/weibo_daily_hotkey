# -*- coding: utf-8 -*-
import os

def get_folder_iter(path):
    last_folder = '.'
    folder_list = path.split('/')[:-1]
    for folder in folder_list:
        last_folder = "%s/%s"%(last_folder, folder)
        yield last_folder

    
def fix_folder(path):
    folder_iter = get_folder_iter(path)
    for folder in folder_iter:
        if not os.access(folder, 0x000):
            os.mkdir(folder)

class File(object):

    @staticmethod
    def w(path, string):
        fix_folder(path)
        with open(path, 'w') as f:
            f.write("%s\n"%string)

    @staticmethod
    def a(path, string):
        fix_folder(path)
        with open(path, 'a') as f:
            f.write("%s\n"%string)

    @staticmethod
    def r(path):
        with open(path, 'r') as f:
            return f.readlines()
