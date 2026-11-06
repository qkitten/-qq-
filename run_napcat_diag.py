# -*- coding: utf-8 -*-
"""前台启动 NapCat 并打印完整输出，用于诊断 Cannot find module。"""
import os
import subprocess
import sys
import time

shell_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NapCat.Shell")
qq = r"C:\Program Files (x86)\Tencent\QQNT\QQ.exe"

env = os.environ.copy()
env.update({
    "NAPCAT_PATCH_PACKAGE": os.path.join(shell_dir, "qqnt.json"),
    "NAPCAT_LOAD_PATH": os.path.join(shell_dir, "loadNapCat.js"),
    "NAPCAT_INJECT_PATH": os.path.join(shell_dir, "NapCatWinBootHook.dll"),
    "NAPCAT_LAUNCHER_PATH": os.path.join(shell_dir, "NapCatWinBootMain.exe"),
    "NAPCAT_MAIN_PATH": os.path.join(shell_dir, "napcat.mjs"),
})

p = subprocess.Popen(
    [os.path.join(shell_dir, "NapCatWinBootMain.exe"), qq, os.path.join(shell_dir, "NapCatWinBootHook.dll")],
    cwd=shell_dir,
    env=env,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
start = time.time()
while time.time() - start < 40:
    line = p.stdout.readline()
    if not line:
        break
    sys.stdout.write(line.decode("utf-8", "ignore"))
    sys.stdout.flush()

if p.poll() is None:
    print("\n[diag] NapCat 仍在运行（未退出），pid=", p.pid)
    time.sleep(3)
else:
    print("\n[diag] 进程已退出，返回码 =", p.returncode)
