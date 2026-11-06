# -*- coding: utf-8 -*-
"""给发布包的一键启动.bat 补上配置面板启动。"""
from pathlib import Path

bat = Path(r"C:/Users/ZHANG789/Desktop/大肥鱼机器人-一键版/一键启动.bat")
t = bat.read_text(encoding="utf-8")
UI = (
    "echo [0/3] 启动配置面板...\n"
    'start "ConfigUI" /min /D "%ROOT%" cmd /c "python -X utf8 tools\\config_ui.py"\n'
    "start http://127.0.0.1:6200\n"
    "\n"
)
if "config_ui.py" not in t:
    i = t.find("echo [1/3]")
    t = t[:i] + UI + t[i:]
    bat.write_text(t, encoding="utf-8")
print("patched:", "config_ui.py" in bat.read_text(encoding="utf-8"))
