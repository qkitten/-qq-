# -*- coding: utf-8 -*-
"""生成脱敏的 cmd_config.example.json 模板，供克隆者使用。"""
import json
from pathlib import Path

ROOT = Path(r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目")
src = ROOT / "AstrBot/data/cmd_config.json"
dst = ROOT / "AstrBot/data/cmd_config.example.json"

d = json.loads(src.read_text(encoding="utf-8-sig"))

# 清空 API Key
for s in d.get("provider_sources", []):
    s["key"] = "" if isinstance(s.get("key"), str) else []

# WebUI 重置默认
dash = d.get("dashboard", {})
dash["username"] = "astrbot"
dash["password"] = "astrbot"
dash["pbkdf2_password"] = ""

# 管理员 QQ 清空
d["admins_id"] = []

dst.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("模板已生成:", dst.name)
