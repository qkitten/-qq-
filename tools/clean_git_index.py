# -*- coding: utf-8 -*-
"""清理 git 暂存区：移除内嵌仓库跟踪、NapCat 分发文件，删除 AstrBot/.git 让内容入库。"""
import shutil
import subprocess
from pathlib import Path

ROOT = Path(r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目")

def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")

# 1) AstrBot 内嵌仓库改为普通目录（删除其 .git，重新加入跟踪）
r = git("rm", "--cached", "-f", "AstrBot")
print("unstage AstrBot:", r.returncode == 0)
inner = ROOT / "AstrBot/.git"
if inner.exists():
    shutil.rmtree(inner)
    print("已删除 AstrBot/.git")

# 2) NapCat.Shell 整目录排除
r = git("rm", "--cached", "-r", "-f", "NapCat.Shell", "-q")
print("unstage NapCat.Shell:", r.returncode == 0)

# 3) 更新 .gitignore 追加规则
gi = ROOT / ".gitignore"
t = gi.read_text(encoding="utf-8")
extra = "\n# ===== 内嵌仓库与协议端分发 =====\nAstrBot/.git/\nNapCat.Shell/\nbootmain/\nconfig/\npersona/\n"
if "NapCat.Shell/" not in t:
    t += extra
    gi.write_text(t, encoding="utf-8")
    print(".gitignore 已更新")

# 4) 重新暂存
git("add", ".")
r = git("diff", "--cached", "--name-only")
files = r.stdout.splitlines()
print("暂存文件数:", len(files))
bad = [f for f in files if any(k in f for k in ("cmd_config", "OneKey/", "NapCat.Shell/", ".log", "ffmpeg-9"))]
print("残留敏感/大文件:", bad if bad else "无")
print("AstrBot 是否入库:", any(f.startswith("AstrBot/") for f in files))
print("README/gitignore/LICENSE:", [f for f in files if f in ("README.md", ".gitignore", "LICENSE")])
