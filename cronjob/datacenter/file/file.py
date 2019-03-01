# -*- coding: utf-8 -*-

from util.base.file import File
from util.base.time import TimeTranslator, Time
from util.configcenter.config_center import ConfigCenter

def sort_hotkey_order_by_amount(hotkey_cache):
    hotkey_cache.sort(key=lambda hotkey: int(hotkey['amount']), reverse=True)
    return hotkey_cache

class FileController(object):

    def __init__(self):
        conf = ConfigCenter.FileConfig()

        self.__path = conf
        self.year, self.month, day = Time.now_ymd()
        self.lasty, self.lastm, _ = Time.lastday_ymd()

        if day == "01":
            self._new_month_do_()

    def _new_month_do_(self):
        self.file = File(self.__path)
        self.year_dir = "./data/%s"%(self.year)
        
        if self.month == "1" or not File.access(self.year_dir):
            File.mkdir(self.year_dir)

        self.file.move(self.year_dir, "data.%s%s.md"%(self.lasty, self.lastm))
        self.__init_new_markdown__()

    def __init_new_markdown__(self):
        File.w(self.__path, "Date | Time | Hotkey | Amount | Flag & Emoji \n--- | --- | --- | --- | ---\n")
    
    def write_data_md(self, today_cache):
        ordered_cache = sort_hotkey_order_by_amount(today_cache)

        cursor = 2

        insert_data = list()

        insert_data.append('--- | --- | --- | --- | ---')

        for data in ordered_cache[0:5]:

            datetime = TimeTranslator.timestamp2datetime(data['time'])

            insert_data.append( '{date}|{time}|{hotkey}|{amount}|{flag} {emoji}'.format(
                hotkey=data['hotkey'], date=datetime.date(), time=datetime.time(),
                amount=data['amount'], flag='' if len(data['flag']) == 0 else data['flag'][0], 
                emoji='' if len(data['emoji']) == 0 else data['emoji'][0],
            ))

        File.i(self.__path, insert_data, cursor)
