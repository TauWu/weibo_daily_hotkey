# -*- coding: utf-8 -*-

from datetime import datetime
import time

from cronjob.tool.qywx import QYWX, MSG_TYPE_MARKDOWN
from cronjob.datacenter.cache.cache_controller import CacheController
from cronjob.datacenter.file.file import sort_hotkey_order_by_amount
from util.base.time import TimeTranslator, DateTime, Time

if __name__ == "__main__":
    cache_controller = CacheController(0)
    cache = cache_controller.get_today_cache()
    ordered_cache = sort_hotkey_order_by_amount(cache)

    idx = 1
    today = DateTime(DateTime.str_to_datetime(Time.ISO_datetime_str()))

    robot_string = f'## {today.date_str} 热搜TOP5\n\n'
    for data in ordered_cache:
        # TOP5
        if idx > 5:
            break
        flag = '' if len(data['flag']) == 0 else data['flag'][0]
        emoji = '' if len(data['emoji']) == 0 else data['emoji'][0]
        dt = "{}".format(TimeTranslator.timestamp2datetime(data['time']))

        robot_string += f"### {idx} | {data['hotkey']}\n"
        robot_string += f"{dt[10:]} → 热度：{data['amount']}\t {flag} {emoji}\n"
        idx += 1

    # 结合 cronjob，每日 8 点推送
    time.sleep(3600 * 8)

    sender = QYWX()
    sender.send_msg(msg_type = MSG_TYPE_MARKDOWN, content = robot_string)
