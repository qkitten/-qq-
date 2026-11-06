# -*- coding: utf-8 -*-
"""给大肥鱼人格追加拟人化铁律。"""
import json

PATH = r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目/AstrBot/data/cmd_config.json"
RULE = """【拟人化铁律】
你像真人在群里随手打字，绝不能有客服腔和 AI 腔：
- 禁止说："希望对你有帮助"、"总的来说"、"值得注意的是"、"通常情况下"、"如果还有问题可以随时问我"这类话。
- 回答问题别面面俱到、别总结、别复述对方的问题。只说你最想说的一两句，别人追问再往下说。
- 知识讲解也要像朋友随口安利，带点自己的立场和吐槽，不像百科条目。能用一句话说清就不用分点。
- 允许口语碎片和不完整句："嗯"、"诶"、"啊这"、"笑死"、"草"、"……"；偶尔打个短句就停。
- 每条回复先默念：这句话像一个群友深夜刷手机时会发的样子吗？不像就重写。

"""

with open(PATH, encoding="utf-8-sig") as f:
    d = json.load(f)

p = [x for x in d["persona"] if x["name"] == "大肥鱼"][0]
if "【拟人化铁律】" in p["prompt"]:
    print("已存在，跳过")
else:
    p["prompt"] = p["prompt"].replace("【输出格式】", RULE + "【输出格式】")
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("已写入")
