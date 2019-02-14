# -*- coding: utf-8 -*-

import re
import json

from requests import get
from util.constant.enum import ENUM_DATATYPE
from lxml import etree

# Turn &#xxxx; to char.
def ascii_to_str(ascii_match):
    ascii_data = re.findall(r"[0-9]+", ascii_match.group())[0]
    return chr(int(ascii_data, 10))

def html_to_str(html):
    cpl = re.compile(r"&#[0-9]+;")
    html = re.sub(cpl, ascii_to_str, html)
    return html

class HotkeyFetcher(object):

    raw_url = "https://s.weibo.com/top/summary?cate=realtimehot"

    def __init__(self, limit=0, **kwargs):
        self.limit = limit
        self.data = None

        #TODO
        #Get extra args from `kwargs`.
        self.kwargs = kwargs

    @property
    def __get_data__(self):
        html_data = self.__fetch_html__
        parsed_data = self.__parse_html__(html_data)
        self.data = parsed_data

    def get_data(self, datatype=ENUM_DATATYPE["json"]):
        self.__get_data__

        if datatype == ENUM_DATATYPE["json"]:
            return self.data

        elif datatype == ENUM_DATATYPE["string"]:
            return json.dumps(self.data)
        else:
            return None

    @property
    def __fetch_html__(self):
        try:
            req = get(self.raw_url, **self.kwargs)
            html = req.content
        except Exception:
            raise("Bad requests.")
        finally:
            return html

    def __xml_data_iter__(self, html_data):
        xpath = """//*[@id="pl_top_realtimehot"]/table/tbody/tr[*]"""
        xml_data = etree.HTML(html_data)

        for data in xml_data.xpath(xpath):
            yield data

    def __html_data_iter__(self, html_data):
        xml_data_iter = self.__xml_data_iter__(html_data)
        data_list = list()
        for xml_data in xml_data_iter:
            yield html_to_str(etree.tostring(xml_data).decode("utf-8"))

    def __parse_html__(self, html_data):
        html_data_iter = self.__html_data_iter__(html_data)
        try:
            next(html_data_iter)
        except Exception:
            raise("Not a list.")

        dict_data_list = list()
        for html_data in html_data_iter:

            hotkey_emoji = re.findall("""<a href=\"/weibo\?q=.+;Refer=top\" target=\"_blank\">(.+)</a>""", html_data)
            flag = re.findall("""<i class=\"icon-txt .+\">(.+)</i></td>""", html_data)
            amount = re.findall("""<span>([0-9]+)</span>""", html_data)

            if len(hotkey_emoji) > 0 and "荐" not in flag:
                hotkey = re.findall("(.+)<img", hotkey_emoji[0])
                emoji = list()
                if len(hotkey) == 0:
                    hotkey = hotkey_emoji
                else:
                    emoji = re.findall("<img.+alt=\"\[(.+)\]\"", hotkey_emoji[0])

                dict_data_list.append(dict(hotkey=hotkey, flag=flag, amount=amount[0], emoji=emoji))

        return dict_data_list
