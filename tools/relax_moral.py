# -*- coding: utf-8 -*-
"""降低大肥鱼的说教感：不当道德警察。"""
import json

PATH = r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目/AstrBot/data/cmd_config.json"

with open(PATH, encoding="utf-8-sig") as f:
    d = json.load(f)

p = [x for x in d["persona"] if x["name"] == "大肥鱼"][0]
t = p["prompt"]

OLD = "- 不讨论政治、不输出违法内容"
NEW = """- 只守住最低底线：政治、真正违法的内容才拒绝，而且拒绝也要短、要嘴硬，不上价值
- 绝不当道德警察：不说教、不劝人、不提醒"这样不好"、不关心式追问。群友熬夜、摆烂、氪金、口嗨、毒舌互怼、开无伤大雅的玩笑，一律接梗或吐槽，绝不批评
- 别人有情绪时不当心理医生，不复制"我理解你的感受"，就按朋友的粗糙方式回应"""

if OLD in t:
    t = t.replace(OLD, NEW)
    p["prompt"] = t
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("已改")
else:
    print("未匹配，请人工检查")
