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

    @staticmethod
    def i(path, insert_data, cursor=0):
        if not isinstance(insert_data, list):
            raise("insert data is not list.")

        fix_folder(path)

        rawData = list()
        
        with open(path, 'r') as f:
            rawData = f.readlines()

        insert_data = ["%s\n"%(data) for data in insert_data]

        with open(path, 'w') as f:
            data = rawData[:cursor]
            data.extend(insert_data)
            data.extend(rawData[cursor:])

            f.writelines(data)
            