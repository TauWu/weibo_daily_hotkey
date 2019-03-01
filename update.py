# -*- coding: utf-8 -*-
# Update Weibo's hotkey list daily.

# 1. Get cache data where key is '0'
# 2. Clean cache where key is '0'
# 3. Update the data to this repo.

from cronjob.datacenter.file.file import FileController
from cronjob.datacenter.cache.cache_controller import CacheController
from cronjob.tool.git_tool import GitTool

if __name__ == '__main__':
    cache_controller = CacheController(0)
    today_cache = cache_controller.get_today_cache()

    # save cache.
    file_controller = FileController()
    file_controller.write_data_md(today_cache)
    
    # # clear cache.
    # cache_controller.clear_today_cache()

    # # update data.
    # git_tool = GitTool()
    # git_tool.push_data()
    