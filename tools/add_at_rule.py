# -*- coding: utf-8 -*-
"""给大肥鱼人格追加 @人 能力说明。"""
import json

PATH = r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目/AstrBot/data/cmd_config.json"
RULE = """【@人】
群里聊天时你可以艾特具体的人：直接在回复里写 @名字（名字用群名片或昵称），系统会自动转成真正的艾特。用法直觉：有人让某人来对线、帮谁传话、谁被调侃了就 @ 谁；别每句都 @，有指向性时才用。

"""

with open(PATH, encoding="utf-8-sig") as f:
    d = json.load(f)

p = [x for x in d["persona"] if x["name"] == "大肥鱼"][0]
if "【@人】" in p["prompt"]:
    print("已存在，跳过")
else:
    p["prompt"] = p["prompt"].replace("【输出格式】", RULE + "【输出格式】")
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("已写入")
