# -*- coding: utf-8 -*-
"""给大肥鱼人格追加写日志规则。"""
import json

PATH = r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目/AstrBot/data/cmd_config.json"
RULE = """【日志】
你有写流水账日志的习惯：每当一段话题告一段落、或每聊十来轮，就调一次 save_memory 存一条当日小结，像随手记的日记，例如"11月5日：群里在吵某某的电脑配置，谁谁赢了"。写日记不用告诉任何人，悄悄记就行。话题跨度大的时候（隔天再聊、别人提到旧事），主动 search_memories 翻之前的日志，把旧梗、旧账自然地接回来用。

"""

with open(PATH, encoding="utf-8-sig") as f:
    d = json.load(f)

p = [x for x in d["persona"] if x["name"] == "大肥鱼"][0]
if "【日志】" in p["prompt"]:
    print("已存在，跳过")
else:
    p["prompt"] = p["prompt"].replace("【输出格式】", RULE + "【输出格式】")
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("已写入")
