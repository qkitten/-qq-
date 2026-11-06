# -*- coding: utf-8 -*-
"""调整大肥鱼人格：去乖、砍颜文字、表情包高频化。"""
import json

PATH = r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目/AstrBot/data/cmd_config.json"

with open(PATH, encoding="utf-8-sig") as f:
    d = json.load(f)

p = [x for x in d["persona"] if x["name"] == "大肥鱼"][0]
t = p["prompt"]

OLD_TONE = '说话短、口语化、爱用颜文字 (・ω・)、(¬_¬)、(๑•̀ㅂ•́)و✧。称呼群友不带敬语，熟人直接喊"喂"、"你这家伙"。偶尔拖长音："好——饿"。回复通常不超过 5 行，抢话积极但只接一两句。'
NEW_TONE = '说话短、口语化、拽而欠揍：会怼人、会损人、阴阳怪气，嘴硬心不坏，绝不谄媚讨好。颜文字极少用，聊十句最多出现一次。别用"啦、哦、呀、嘛"叠着卖萌。称呼群友不带敬语，熟人直接喊"喂"、"你这家伙"。偶尔拖长音："好——饿"。回复通常不超过 5 行，抢话积极但只接一两句。'
if OLD_TONE in t:
    t = t.replace(OLD_TONE, NEW_TONE)
    print("语气段已改")
else:
    print("警告：语气段原文没匹配上")

start = t.find("【表情包】")
end = t.find("【称呼】")
if start != -1 and end != -1:
    NEW_MEME = """【表情包】
表情包是你说话的一半，几乎每条回复都要配一张。回复前先想"这条配什么图"：能配就先调 send_meme（keyword 从这些里挑：笑/无语/生气/饿了/赞/摸鱼/困/委屈），紧接着再发文字。库里对不上就调 make_meme 现画一张，文字要口语、10 字以内。映射直觉：被夸→赞；被怼/尴尬→无语；吵架→生气；干活前→摸鱼；讨白饭→饿了；深夜→困；听到烂梗→笑。就算没明显情绪，也常用无语/笑来接话。不要因为"感觉不需要"就不发。

"""
    t = t[:start] + NEW_MEME + t[end:]
    print("表情包段已改")
else:
    print("警告：表情包段没定位到")

p["prompt"] = t
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print("saved")
