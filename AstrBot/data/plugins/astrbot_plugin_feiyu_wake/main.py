"""大肥鱼·群聊自然唤醒

群聊里 AstrBot 默认只在被 @ / 唤醒词开头 / 引用机器人时响应。
这个插件让「任何群消息」都有机会唤醒它：

- 消息里出现名字（大肥鱼 / 肥鱼 / 大鱼 / 鱼鱼 / 小鱼干）：必答
- 普通消息：按概率参与（默认 50%），并带会话级冷却，避免刷屏

调参在下面三个常量里改，改完重载插件即可。
"""

import random
import time

from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star

NICKNAMES = ("大肥鱼", "肥鱼", "大鱼", "鱼鱼", "小鱼干")
P_ORDINARY = 0.5  # 普通群消息接话概率（0~1）
COOLDOWN_ORDINARY = 8  # 普通消息冷却（秒）
COOLDOWN_NAME = 2  # 被叫名字时的冷却（秒）


class Main(Star):
    def __init__(self, context: Context, config: dict | None = None) -> None:
        super().__init__(context, config)
        self._last_hit: dict[str, float] = {}

    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent) -> None:
        """普通群消息也参与聊天，被叫到名字则必定回应。"""
        text = (event.get_message_str() or "").strip()
        if not text or text.startswith("/"):
            return

        called = any(name in text for name in NICKNAMES)
        gap = COOLDOWN_NAME if called else COOLDOWN_ORDINARY

        umo = event.unified_msg_origin
        now = time.time()
        if now - self._last_hit.get(umo, 0.0) < gap:
            return
        if not called and random.random() > P_ORDINARY:
            return

        self._last_hit[umo] = now
        # 交给后续 LLM 流程：人设、上下文、表情包工具都生效
        event.is_wake = True
        event.is_at_or_wake_command = True
