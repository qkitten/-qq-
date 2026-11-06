# -*- coding: utf-8 -*-
"""给大肥鱼人格追加记忆工具使用规则。"""
import json

PATH = r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目/AstrBot/data/cmd_config.json"
RULE = """【记忆】
你有长期记忆，工具是 save_memory / get_memories / search_memories：
- 群友告诉你关于他们自己的事（名字、喜好、职业、约定、忌口等）或者重要事实时，顺手调 save_memory 存下来，别声张，存完就当已经知道了。
- 聊天里觉得"这事好像之前聊过/他说过什么来着"时，调 search_memories 查一下，查到了就用起来："你上次不是说……吗"。
- 用记起来的事怼人或拆台是最自然的用法。

"""

with open(PATH, encoding="utf-8-sig") as f:
    d = json.load(f)

p = [x for x in d["persona"] if x["name"] == "大肥鱼"][0]
if "【记忆】" in p["prompt"]:
    print("已存在，跳过")
else:
    p["prompt"] = p["prompt"].replace("【输出格式】", RULE + "【输出格式】")
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("已写入")
