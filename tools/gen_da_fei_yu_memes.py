# -*- coding: utf-8 -*-
"""批量生成大肥鱼专属表情包，写入 feiyu_meme 插件的 memes/ 库。"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目/AstrBot/data/plugins/astrbot_plugin_feiyu_meme/memes")
FONT = r"C:\Windows\Fonts\msyhbd.ttc"
W = H = 512


def font(size):
    return ImageFont.truetype(FONT, size)


def whale(d, cx, cy, scale, mood="happy"):
    """画一只圆滚滚的蓝色小鲸鱼，mood 决定表情。"""
    s = scale
    body = (86, 164, 255)
    dark = (60, 128, 220)
    # 身体
    d.ellipse([cx - 90 * s, cy - 60 * s, cx + 90 * s, cy + 60 * s], fill=body)
    # 尾巴
    d.polygon([(cx - 85 * s, cy), (cx - 130 * s, cy - 35 * s), (cx - 115 * s, cy + 5 * s), (cx - 130 * s, cy + 30 * s)], fill=body)
    # 肚皮
    d.ellipse([cx - 55 * s, cy + 5 * s, cx + 70 * s, cy + 58 * s], fill=(225, 242, 255))
    # 眼睛
    for ex in (cx + 18 * s, cx + 62 * s):
        if mood == "closed":
            d.arc([ex - 9 * s, cy - 18 * s, ex + 9 * s, cy + 2 * s], 20, 160, fill=(30, 40, 60), width=int(5 * s))
        else:
            d.ellipse([ex - 7 * s, cy - 16 * s, ex + 7 * s, cy - 2 * s], fill=(25, 32, 48))
    # 腮红
    d.ellipse([cx + 40 * s, cy + 6 * s, cx + 66 * s, cy + 20 * s], fill=(255, 170, 180))
    # 嘴
    mx, my = cx + 40 * s, cy + 8 * s
    if mood == "happy":
        d.arc([mx - 16 * s, my - 12 * s, mx + 16 * s, my + 14 * s], 15, 165, fill=(25, 32, 48), width=int(5 * s))
    elif mood == "angry":
        d.line([(mx - 14 * s, my + 8 * s), (mx + 14 * s, my - 2 * s)], fill=(25, 32, 48), width=int(5 * s))
    elif mood == "flat":
        d.line([(mx - 12 * s, my), (mx + 12 * s, my)], fill=(25, 32, 48), width=int(5 * s))
    elif mood == "wow":
        d.ellipse([mx - 8 * s, my - 6 * s, mx + 8 * s, my + 12 * s], fill=(25, 32, 48))
    # 喷水
    if mood in ("happy", "wow"):
        d.polygon([(cx - 10 * s, cy - 58 * s), (cx - 16 * s, cy - 92 * s), (cx - 2 * s, cy - 92 * s)], fill=(190, 225, 255))
        d.ellipse([cx - 26 * s, cy - 104 * s, cx - 8 * s, cy - 88 * s], fill=(190, 225, 255))
    # 生气符号 / 泪滴 / zzz 由调用方补充
    return dark


MEMES = [
    # (关键词列表, 主文字, 副文字, mood, extra)
    (["嘴硬", "傲娇"], "才不是", "哼", "flat", None),
    (["白饭", "讨饭", "饿了"], "白饭拿来", "不干活", "wow", None),
    (["好耶", "开心", "兴奋"], "好耶！！", "冲冲冲", "happy", "spark"),
    (["震惊", "瓜"], "吃瓜", "让朕看看", "wow", None),
    (["疑惑", "问号"], "啊？", "你在说啥", "flat", "question"),
    (["拒绝", "摆烂", "拒绝"], "不干", "摆了", "closed", None),
    (["困", "困"], "睡了", "勿扰", "closed", "zzz"),
    (["哭", "委屈"], "呜呜呜", "鱼没有泪腺", "flat", "tears"),
    (["炸毛", "生气"], "你礼貌吗", "！", "angry", "anger"),
    (["拆台", "旧账", "记仇"], "小本本", "记下了", "flat", "book"),
    (["拽", "得意"], "那当然", "本鱼最棒", "happy", "spark"),
    (["无语", "汗"], "……", "你是懂聊天的", "flat", "sweat"),
    (["赞", "夸"], "准了", "勉强表扬", "happy", "spark"),
    (["摸鱼", "偷懒"], "摸鱼中", "生人勿近", "closed", "zzz"),
    (["瞌睡", "深夜"], "凌晨三点", "鱼也要睡", "closed", "zzz"),
    (["抢话", "来了"], "本鱼有话说", "都让让", "happy", None),
]


def draw(main, sub, mood, extra, out: Path):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(96 + 70 * t), int(172 + 40 * t), 255))
    d.rounded_rectangle([24, 24, W - 24, H - 24], radius=40, fill=(255, 255, 255))

    # 鲸鱼在上方偏左
    whale(d, 200, 170, 1.25, mood)
    if extra == "anger":
        d.polygon([(320, 90), (335, 60), (345, 85), (370, 75), (355, 105), (375, 112), (330, 125)], fill=(255, 90, 90))
    elif extra == "zzz":
        f = font(34)
        for i, (zx, zy) in enumerate([(300, 90), (330, 60), (358, 34)]):
            d.text((zx, zy), "z", font=f, fill=(90, 130, 200))
    elif extra == "tears":
        d.ellipse([236, 190, 258, 226], fill=(120, 190, 255))
        d.ellipse([286, 196, 306, 230], fill=(120, 190, 255))
    elif extra == "question":
        d.text((310, 70), "？", font=font(84), fill=(70, 110, 190))
    elif extra == "sweat":
        d.polygon([(330, 100), (344, 124), (316, 124)], fill=(150, 210, 255))
    elif extra == "spark":
        for sx, sy in [(330, 80), (365, 120), (300, 55)]:
            d.polygon([(sx, sy - 14), (sx + 5, sy - 4), (sx + 15, sy), (sx + 5, sy + 5), (sx, sy + 14), (sx - 5, sy + 5), (sx - 15, sy), (sx - 5, sy - 4)], fill=(255, 214, 90))
    elif extra == "book":
        d.rounded_rectangle([280, 60, 390, 140], radius=10, fill=(255, 240, 200), outline=(180, 140, 80), width=4)
        d.line([(300, 85), (368, 85)], fill=(150, 110, 60), width=4)
        d.line([(300, 108), (350, 108)], fill=(150, 110, 60), width=4)

    # 主文字
    size = 84 if len(main) <= 5 else 68
    f1 = font(size)
    bbox = d.textbbox((0, 0), main, font=f1)
    d.text(((W - bbox[2] + bbox[0]) / 2 - bbox[0], 330), main, font=f1, fill=(40, 60, 110))
    # 副文字
    if sub:
        f2 = font(36)
        b2 = d.textbbox((0, 0), sub, font=f2)
        d.text(((W - b2[2] + b2[0]) / 2 - b2[0], 428), sub, font=f2, fill=(120, 150, 200))

    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print("生成", out.name)


random.seed(2026)
for keywords, main, sub, mood, extra in MEMES:
    name = "_".join(dict.fromkeys(keywords)) + "_" + str(random.randint(1000, 9999)) + ".png"
    draw(main, sub, mood, extra, OUT / name)
print("done")
