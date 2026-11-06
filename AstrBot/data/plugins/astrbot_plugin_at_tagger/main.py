"""@人插件：让大肥鱼在回复里用 @昵称 真正艾特群友。

原理：发送前扫描消息链里的纯文本，把 "@昵称" 替换成真正的 At 组件。
昵称解析用群成员列表（群名片 + 昵称，双缓存 10 分钟）。
"""

import re
import time

from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.message_components import At, Plain
from astrbot.api.star import Context, Star

AT_PATTERN = re.compile(r"(@[^\s@，。！？,!?~～]{1,24})")
CACHE_TTL = 600


class Main(Star):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        self._members_cache: dict[int, tuple[float, dict[str, str]]] = {}

    async def _member_map(self, event: AstrMessageEvent, group_id: int) -> dict[str, str]:
        cached = self._members_cache.get(group_id)
        now = time.time()
        if cached and now - cached[0] < CACHE_TTL:
            return cached[1]
        mapping: dict[str, str] = {}
        try:
            bot = getattr(event, "bot", None)
            if bot is None:
                return mapping
            members = await bot.api.call_action(
                "get_group_member_list", group_id=int(group_id)
            )
            for m in members or []:
                uid = str(m.get("user_id", "")).strip()
                if not uid:
                    continue
                for name in (m.get("card") or "", m.get("nickname") or ""):
                    name = name.strip()
                    if name:
                        mapping[name.lower()] = uid
        except Exception:
            logger.debug("at_tagger 获取群成员列表失败", exc_info=True)
        if mapping:
            self._members_cache[group_id] = (now, mapping)
        return mapping

    @filter.on_decorating_result()
    async def replace_at_text(self, event: AstrMessageEvent) -> None:
        result = event.get_result()
        if result is None or not result.chain:
            return
        group_id = getattr(event.message_obj, "group_id", None)
        if not group_id:
            return  # 私聊没有 @ 人一说

        mapping = await self._member_map(event, int(group_id))
        if not mapping:
            return

        new_chain = []
        changed = False
        for seg in result.chain:
            if not isinstance(seg, Plain):
                new_chain.append(seg)
                continue
            parts = AT_PATTERN.split(seg.text or "")
            if len(parts) <= 1:
                new_chain.append(seg)
                continue
            changed = True
            for part in parts:
                if not part:
                    continue
                if part.startswith("@"):
                    uid = mapping.get(part[1:].strip().lower())
                    if uid:
                        new_chain.append(At(qq=uid, name=part[1:].strip()))
                    else:
                        new_chain.append(Plain(part))  # 找不到人就原样输出
                else:
                    new_chain.append(Plain(part))
        if changed:
            result.chain = new_chain
