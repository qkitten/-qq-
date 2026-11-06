"""大肥鱼表情包插件

能力：
1. ``send_meme``：让 LLM 在聊天时按情绪从本地表情包库里挑一张发出去
2. ``make_meme``：库里没有合适的图时，现场画一张（Pillow 本地绘制，不联网）
3. ``/存表情 关键词``：进入学习模式，随后发一张图给机器人，即可入库复用

表情包库目录：``memes/``，文件名里的关键词用 ``_`` 分隔，例如 ``无语_鄙视_1712.png``。
"""

import random
import shutil
import time
from pathlib import Path

from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont

from astrbot.api.all import Image
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star

PLUGIN_DIR = Path(__file__).parent
LIB_DIR = PLUGIN_DIR / "memes"
GEN_DIR = PLUGIN_DIR / "memes_generated"
IMG_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
LEARN_TTL = 180  # 学习模式有效期（秒）

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\msyh.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
]

# 首次启动自动生成的基础表情包：关键词 -> (主文字, 副文字)
DEFAULT_MEMES = [
    ("无语", "无语", "(¬_¬)"),
    ("笑", "哈哈哈", "(๑•̀ㅂ•́)و✧"),
    ("生气", "生气了", "(#`Д´)"),
    ("饿了", "饿了", "白饭呢？"),
    ("赞", "可以", "准了"),
    ("摸鱼", "摸鱼中", "别叫我"),
    ("困", "困了", "zzz"),
    ("委屈", "委屈", "呜"),
]


def _sniff_ext(path: Path) -> str:
    """按文件头判断真实图片格式，避免 QQ 缓存文件没有扩展名。"""
    try:
        with open(path, "rb") as f:
            head = f.read(12)
    except OSError:
        return ".png"
    if head[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if head[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return ".webp"
    return ".png"


class Main(Star):
    def __init__(self, context: Context, config: dict | None = None) -> None:
        super().__init__(context, config)
        self._pending: dict[str, tuple[str, float]] = {}
        self._font_cache: dict[int, ImageFont.FreeTypeFont] = {}
        LIB_DIR.mkdir(parents=True, exist_ok=True)
        GEN_DIR.mkdir(parents=True, exist_ok=True)
        self._ensure_default_memes()

    # ------------------------------------------------------------------ 字体 / 绘制

    def _font(self, size: int):
        cached = self._font_cache.get(size)
        if cached is not None:
            return cached
        for p in FONT_CANDIDATES:
            if Path(p).exists():
                try:
                    font = ImageFont.truetype(p, size)
                    self._font_cache[size] = font
                    return font
                except Exception:
                    continue
        font = ImageFont.load_default()
        self._font_cache[size] = font
        return font

    def _draw(self, main_text: str, sub_text: str = "", out: Path | None = None) -> Path:
        """画一张 512x512 的卡片式表情包，返回文件路径。"""
        main_text = (main_text or "…").strip()[:20]
        w = h = 512
        img = PILImage.new("RGB", (w, h))
        d = ImageDraw.Draw(img)

        # 蓝白渐变底
        for y in range(h):
            t = y / h
            d.line([(0, y), (w, y)], fill=(int(96 + 70 * t), int(172 + 40 * t), 255))

        # 白色卡片
        d.rounded_rectangle([30, 30, w - 30, h - 30], radius=40, fill=(255, 255, 255))

        # 主文字：按字数自动换行 + 自动字号
        per_line = 5 if len(main_text) <= 10 else 7
        lines = [main_text[i : i + per_line] for i in range(0, len(main_text), per_line)][:3]
        longest = max((len(x) for x in lines), default=1)
        size = 120 if longest <= 3 else 92 if longest <= 4 else 76 if longest <= 5 else 58
        font = self._font(size)
        line_h = size + 16
        total_h = line_h * len(lines)
        y = (h - total_h) // 2 - (26 if sub_text else 0)
        for line in lines:
            bbox = d.textbbox((0, 0), line, font=font)
            d.text(((w - (bbox[2] - bbox[0])) / 2 - bbox[0], y), line, font=font, fill=(28, 32, 44))
            y += line_h

        if sub_text:
            sub_font = self._font(44)
            bbox = d.textbbox((0, 0), sub_text, font=sub_font)
            d.text(
                ((w - (bbox[2] - bbox[0])) / 2 - bbox[0], y + 10),
                sub_text,
                font=sub_font,
                fill=(120, 132, 150),
            )

        mark_font = self._font(22)
        d.text((w - 210, h - 72), "大肥鱼 · 表情包", font=mark_font, fill=(178, 190, 205))

        out = out or GEN_DIR / f"gen_{int(time.time() * 1000)}.png"
        img.save(out)
        return out

    def _ensure_default_memes(self) -> None:
        if any(p.is_file() for p in LIB_DIR.iterdir()):
            return
        for kw, main_text, sub in DEFAULT_MEMES:
            try:
                self._draw(main_text, sub, out=LIB_DIR / f"{kw}_默认.png")
            except Exception as e:
                self.logger.warning(f"生成默认表情包失败 {kw}: {e}")
        self.logger.info(f"已生成 {len(DEFAULT_MEMES)} 张默认表情包")

    # ------------------------------------------------------------------ 库检索

    def _all_memes(self) -> list[Path]:
        if not LIB_DIR.exists():
            return []
        return [p for p in LIB_DIR.rglob("*") if p.suffix.lower() in IMG_EXTS]

    def _pick(self, keyword: str) -> Path | None:
        memes = self._all_memes()
        if not memes:
            return None
        kw = (keyword or "").strip().lower()
        if kw:
            scored: list[tuple[int, Path]] = []
            for p in memes:
                stem = p.stem.lower()
                score = 10 if kw in stem else sum(1 for ch in set(kw) if ch in stem)
                if score:
                    scored.append((score, p))
            if scored:
                top_score = max(s for s, _ in scored)
                return random.choice([p for s, p in scored if s == top_score])
        return random.choice(memes)

    # ------------------------------------------------------------------ LLM 工具

    @filter.llm_tool(name="send_meme")
    async def send_meme(self, event: AstrMessageEvent, keyword: str):
        """从表情包库挑一张图发出去。聊天里想表达情绪（笑、无语、生气、饿了、摸了）或接梗时调用，比文字更生动。

        Args:
            keyword(string): 表情包关键词，例如 笑、无语、生气、饿了、赞、摸鱼、困
        """
        path = self._pick(keyword)
        if path is None:
            path = self._draw(keyword or "…")
        yield event.image_result(str(path))

    @filter.llm_tool(name="make_meme")
    async def make_meme(self, event: AstrMessageEvent, text: str):
        """现场画一张新表情包（白卡片大字）。当库里没有合适的表情包，或想吐槽某个具体的梗时调用。

        Args:
            text(string): 表情包上的文字，不超过 10 个字
        """
        yield event.image_result(str(self._draw(text)))

    # ------------------------------------------------------------------ 学习 & 命令

    @filter.command("存表情")
    async def cmd_learn(self, event: AstrMessageEvent, keyword: str = ""):
        """教大肥鱼认识新表情包：发送 /存表情 关键词，然后在 3 分钟内发一张图片。"""
        kw = (keyword or "").strip()
        if not kw:
            yield event.plain_result("用法：/存表情 关键词，然后发一张图给我 (・ω・)")
            return
        self._pending[event.unified_msg_origin] = (kw, time.time() + LEARN_TTL)
        yield event.plain_result(f"好，{LEARN_TTL // 60} 分钟内把那张图发我，我记成「{kw}」")

    @filter.command("表情库")
    async def cmd_lib(self, event: AstrMessageEvent):
        """查看大肥鱼现在会发多少种表情包。"""
        memes = self._all_memes()
        kws = sorted({p.stem.split("_")[0] for p in memes})
        yield event.plain_result(
            f"我现在会 {len(memes)} 张表情包，关键词：{'、'.join(kws[:20]) if kws else '还没有'}\n"
            "想教新的：/存表情 关键词 → 再发一张图 (๑•̀ㅂ•́)و✧"
        )

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_any_message(self, event: AstrMessageEvent):
        """学习模式：收到图片就按用户给的关键词入库。"""
        umo = event.unified_msg_origin
        rec = self._pending.get(umo)
        if not rec:
            return
        kw, expire = rec
        if time.time() > expire:
            self._pending.pop(umo, None)
            return

        images = [c for c in event.get_messages() if isinstance(c, Image)]
        if not images:
            return

        try:
            src = Path(await images[0].convert_to_file_path())
            ext = _sniff_ext(src)
            dst = LIB_DIR / f"{kw}_{int(time.time())}{ext}"
            shutil.copyfile(src, dst)
        except Exception as e:
            self.logger.warning(f"保存表情包失败: {e}")
            yield event.plain_result("这张我接不住…再发一次试试？")
            return

        self._pending.pop(umo, None)
        yield event.plain_result(f"记住了 (๑•̀ㅂ•́)و✧ 以后说到「{kw}」我就发这张")
