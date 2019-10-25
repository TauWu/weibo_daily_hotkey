# -*- coding: utf-8 -*-
import requests
import json

from util.configcenter.config_center import ConfigCenter

BASE_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}"

MSG_TYPE_DICT = {
    1: "text",
    2: "markdown",
    3: "image",
    4: "news",
}

MSG_TYPE_TEXT = 1
MSG_TYPE_MARKDOWN = 2
MSG_TYPE_IMAGE = 3
MSG_TYPE_NEWS = 4

class QYWXNews(object):

    def __init__(self, title = "", desc = "", url = "", picurl = ""):
        self.data = {
            "title": title,
            "description": desc,
            "url": url,
            "picurl": picurl,
        }


class QYWX(object):

    def __init__(self):
        conf = ConfigCenter.QYWXConfig()
        self._tokens = conf

    def __create_content__(self,
        msg_type = MSG_TYPE_TEXT,
        content = "", mentioned_mobile_list = [],
        image_md5 = "", image_base64 = "",
        newsObjects = [QYWXNews],
    ):

        self._data = dict()
        self._data["msgtype"] = MSG_TYPE_DICT[msg_type]

        if msg_type == MSG_TYPE_TEXT:
            self._data["text"] = dict()
            self._data["text"]["content"] = content
            self._data["text"]["mentioned_mobile_list"] = mentioned_mobile_list

        elif msg_type == MSG_TYPE_MARKDOWN:
            self._data["markdown"] = dict()
            self._data["markdown"]["content"] = content

        elif msg_type == MSG_TYPE_IMAGE:
            self._data["image"] = dict()
            self._data["image"]["base64"] = image_base64
            self._data["image"]["md5"] = image_md5

        elif msg_type == MSG_TYPE_NEWS:
            self._data["news"] = dict()
            articles = list()
            for d in newsObjects:
                articles.append(d.data)
            self._data["news"]["articles"] = articles

        else:
            pass

    def send_msg(self, *,
        msg_type = MSG_TYPE_TEXT,
        content = "", mentioned_mobile_list = [],
        image_md5 = "", image_base64 = "",
        newsObjects = [QYWXNews]):
        
        self.__create_content__(msg_type, content, mentioned_mobile_list, image_md5, image_base64, newsObjects)
        
        for token in self._tokens:
            resp = requests.post(
                BASE_URL.format(token),
                json=self._data,
            )
            print(f"request qywx succeed, resp => {resp.content}")
