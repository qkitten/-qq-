# -*- coding: utf-8 -*-
"""更新发布包说明书：加入 Python 环境准备步骤。"""
from pathlib import Path

f = Path(r"C:/Users/ZHANG789/Desktop/大肥鱼机器人-一键版/使用说明书.txt")
t = f.read_text(encoding="utf-8")

OLD = """【二、第一次使用（5 分钟）】
1. 把整个文件夹解压到任意位置（路径不要带中文空格问题不大，但别放 C:\\Program Files）
2. 双击「一键启动.bat」
   - 它会自动打开「配置面板」网页
3. 在配置面板里填两项："""

NEW = """【二、第一次使用（10 分钟）】
0. 环境准备（只需一次）：
   - 安装 Python 3.10 或更高版本：https://www.python.org/downloads/
     （安装时务必勾选 "Add python.exe to PATH"）
   - 双击「安装依赖.bat」，等它装完（需联网，约 2-5 分钟）
1. 把整个文件夹解压到任意位置（路径不要带中文空格问题不大，但别放 C:\\Program Files）
2. 双击「一键启动.bat」
   - 它会自动打开「配置面板」网页
3. 在配置面板里填两项："""

if "0. 环境准备" not in t:
    t = t.replace(OLD, NEW)
    f.write_text(t, encoding="utf-8")
print("说明书已更新:", "0. 环境准备" in t)
