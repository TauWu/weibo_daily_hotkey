# -*- coding: utf-8 -*-

from cronjob.tool.git_tool import GitTool

if __name__ == "__main__":
    git_tool = GitTool()
    git_tool.push(".", "test push code.")
