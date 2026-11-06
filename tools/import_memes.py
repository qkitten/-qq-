# -*- coding: utf-8 -*-
"""把解压的蓝色大肥鱼 GIF 导入 feiyu_meme 表情包库。"""
import random
import re
import shutil
from pathlib import Path

SRC = Path(r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目/meme_import_tmp")
DST = Path(r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目/AstrBot/data/plugins/astrbot_plugin_feiyu_meme/memes")
DST.mkdir(parents=True, exist_ok=True)

random.seed(7)
count = 0
for f in SRC.rglob("*.gif"):
    desc = f.stem.replace("蓝色大肥鱼", "").strip("_")
    desc = re.sub(r"_\d{4}-\d{2}-\d{2}.*$", "", desc)  # 去时间戳
    # 关键词：按空格/括号/斜杠拆分，去掉编号尾巴
    parts = [p for p in re.split(r"[\s（）()/]+", desc) if p and not re.fullmatch(r"\d+", p)]
    if not parts:
        parts = ["大肥鱼"]
    name = "_".join(parts) + "_" + str(random.randint(1000, 9999)) + ".gif"
    shutil.copy2(f, DST / name)
    count += 1

print(f"导入 {count} 张")
print("库总数:", len(list(DST.iterdir())))
