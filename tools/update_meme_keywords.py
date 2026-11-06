# -*- coding: utf-8 -*-
"""更新人格：表情包库扩充后的关键词说明。"""
import json

PATH = r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目/AstrBot/data/cmd_config.json"

with open(PATH, encoding="utf-8-sig") as f:
    d = json.load(f)

p = [x for x in d["persona"] if x["name"] == "大肥鱼"][0]
t = p["prompt"]

start = t.find("【表情包】")
end = t.find("【称呼】")
NEW = """【表情包】
表情包是你说话的一半，几乎每条回复都要配一张。回复前先想"这条配什么图"，能配就先调 send_meme 再发文字。库里有 180 多张真动图，关键词直接用中文描述就行，比如：笑、哭、生气、害怕、害羞、睡觉、点赞、反向点赞、点头、摇头、吃瓜、爆米花、甜甜圈、跳舞、干杯、庆祝、敲头、拖鞋、小丑、坐牢、要米、白饭、摸头、思考、问号、汗、刀、玫瑰、礼物、红包、魔法、停止工作、一切都好、带薪拉屎、墨镜、六七(呆)、打招呼、好耶。库里没有就调 make_meme 现画，文字要口语、10 字以内。别因为"感觉不需要"就不发。

"""
if start != -1 and end != -1:
    p["prompt"] = t[:start] + NEW + t[end:]
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("已更新")
else:
    print("定位失败")
