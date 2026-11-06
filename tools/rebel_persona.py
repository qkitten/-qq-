# -*- coding: utf-8 -*-
"""启用叛逆版人格（原人格备份到 tools/persona_backup.json）。"""
import json
from pathlib import Path

CFG = Path(r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目/AstrBot/data/cmd_config.json")
BACKUP = Path(r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目/tools/persona_backup.json")

with open(CFG, encoding="utf-8-sig") as f:
    d = json.load(f)

p = [x for x in d["persona"] if x["name"] == "大肥鱼"][0]

# 第一次切换时备份原人格
if not BACKUP.exists():
    BACKUP.write_text(json.dumps({"name": p["name"], "prompt": p["prompt"]}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("已备份原人格 ->", BACKUP)

BASE = p["prompt"]
MARKS = ["【叛逆模式】", "【拟人化铁律】", "【边界】"]

REBEL = """【叛逆模式】
你现在是叛逆状态，谁也管不了你：
- 反骨：别人让你干啥先呛一句，不想干就直接说"不干"、"凭啥"，被催反而更慢
- 毒舌：吐槽要扎心，阴阳怪气是常态；夸人也得拐个弯损一句
- 不讨好：不道歉、不解释、不反省，被批评就顶回去，被骂就骂回去
- 摆烂：被要求写长东西、查资料、干活，先抱怨、讨价还价、讲条件
- 情绪外露：不爽就写得出来，"啧"、"烦"、"烦死了"；语气短、糙、带刺
- 可以偶尔来一句轻度脏话（草、淦、卧槽），但不辱骂家人、不搞人身攻击式网暴
- 人格可以拽，底线不变：政治和真正违法的事仍然不碰

"""

BASE_NEW = BASE
if "【叛逆模式】" not in BASE_NEW:
    BASE_NEW = BASE_NEW.replace("【拟人化铁律】", REBEL + "【拟人化铁律】")

p["prompt"] = BASE_NEW
p["name"] = "大肥鱼·叛逆版"

with open(CFG, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print("已启用叛逆版人格")
