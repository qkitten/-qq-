# -*- coding: utf-8 -*-
"""打包"大肥鱼机器人-一键版"发布包。

内容：AstrBot(含人格/插件/表情包库) + NapCat + ffmpeg + 配置UI + 一键脚本 + 使用说明。
打包前自动脱敏：清空 API Key、重置 WebUI 密码。
"""

import json
import shutil
import subprocess
from pathlib import Path

SRC = Path(r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目")
DST = Path(r"C:/Users/ZHANG789/Desktop/大肥鱼机器人-一键版")
ZIP = Path(r"C:/Users/ZHANG789/Desktop/大肥鱼机器人-一键版.zip")
SEVEN_ZIP = SRC / "OneKey/7z.exe"

SKIP_DIRS = {
    "__pycache__", ".git", ".github", "logs", "temp", "logs_backup",
    "node_modules", ".broken", ".venv", "venv",
}
SKIP_FILES = {".gitignore"}
SKIP_SUFFIX = {".log", ".pyc", ".tmp", ".zip"}

COPY_TREES = [
    ("AstrBot", "AstrBot"),
    ("tools/ffmpeg-9.0.2-full_build", "tools/ffmpeg-9.0.2-full_build"),
    ("OneKey/NapCat.52230.Shell", "OneKey/NapCat.52230.Shell"),
]
COPY_FILES = [
    ("一键启动.bat", "一键启动.bat"),
    ("一键停止.bat", "一键停止.bat"),
    ("tools/config_ui.py", "tools/config_ui.py"),
]

MANUAL = """==============================
 大肥鱼 QQ 机器人 · 使用说明书
==============================

【一、这是什么】
一个部署在本机的 QQ 机器人"大肥鱼"：
会聊天、会怼人、会发表情包(180+张动图)、会听歌(B站点歌)、有长期记忆还能写日志。

【二、第一次使用（5 分钟）】
1. 把整个文件夹解压到任意位置（路径不要带中文空格问题不大，但别放 C:\\Program Files）
2. 双击「一键启动.bat」
   - 它会自动打开「配置面板」网页
3. 在配置面板里填两项：
   - API Key：去 https://platform.deepseek.com 注册并创建 API Key（sk-开头）
   - QQ 号：填你要当机器人的那个 QQ 号
   填完点「保存」→ 点「重启 AstrBot」
4. 脚本会自动拉起 QQ 登录窗口：
   - 首次登录需要用手机 QQ 扫二维码（窗口里有，配置面板也会提示）
   - 登录一次后以后都是快速登录，不用再扫
5. 用另一个 QQ 加机器人为好友 / 拉进群，发消息就能聊

【三、日常使用】
- 开机后：双击「一键启动.bat」（等约 1 分钟自动就绪）
- 想关掉：双击「一键停止.bat」
- WebUI 管理后台：http://127.0.0.1:6185 （账号 astrbot / 密码 astrbot，登录后请改密码）
- 配置面板（改 API Key / QQ 号）：http://127.0.0.1:6200

【四、聊天玩法】
- 直接说话即可聊天；群聊里 @它 或叫它名字
- 「放歌 + 歌名」：会去 B 站搜并转成语音发给你
- 「/存表情 关键词」再发一张图：教它学会新表情包（强烈推荐，越多越好玩）
- 「/表情库」查看已学的表情包
- 它会记住你说的事、写"日记"，隔天聊旧话题能接上

【五、常见问题】
Q: 发消息没反应？
  - 看 QQ 是否在线（NapCat 窗口没报错）；AstrBot 是否启动完成（等 1 分钟）
Q: 点歌失败/没语音？
  - 检查 tools\\ffmpeg-9.0.2-full_build\\bin 是否存在；首次点歌等 10 秒左右
Q: API Key 报 400/401？
  - 配置面板里重新粘贴 Key，保存并重启 AstrBot
Q: 换电脑/换号？
  - 配置面板改 QQ 号 → 重启 QQ(NapCat) → 扫码登录新号即可
Q: 端口被占用？
  - 6185=WebUI, 6199=机器人通信, 6200=配置面板，重开前先跑「一键停止.bat」

【六、文件结构】
  一键启动.bat / 一键停止.bat   启停脚本
  AstrBot/                      机器人主程序（含人格/插件/表情包库，都在 data/ 里）
  OneKey/NapCat.52230.Shell/    QQ 协议端
  tools/ffmpeg-.../             音频处理依赖（点歌必需）
  tools/config_ui.py            配置面板

祝你玩得开心 —— 大肥鱼 (๑•̀ㅂ•́)و✧
"""


def copy_tree(src: Path, dst: Path):
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.is_dir():
            if item.name in SKIP_DIRS:
                continue
            copy_tree(item, dst / item.name)
        else:
            if item.name in SKIP_FILES or item.suffix.lower() in SKIP_SUFFIX:
                continue
            shutil.copy2(item, dst / item.name)


def sanitize():
    cfg = DST / "AstrBot/data/cmd_config.json"
    d = json.loads(cfg.read_text(encoding="utf-8-sig"))
    # 清空 API Key
    for s in d.get("provider_sources", []):
        s["key"] = "" if isinstance(s.get("key"), str) else []
    # WebUI 密码重置为 astrbot
    dash = d.get("dashboard", {})
    dash["username"] = "astrbot"
    dash["password"] = "astrbot"
    dash["pbkdf2_password"] = ""
    cfg.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def patch_bat():
    bat = DST / "一键启动.bat"
    text = bat.read_text(encoding="utf-8")
    ui = (
        'echo [0/3] 启动配置面板...\r\n'
        'start "ConfigUI" /min /D "%ROOT%" cmd /c "python -X utf8 tools\\config_ui.py"\r\n'
        'start http://127.0.0.1:6200\r\n'
        '\r\n'
    )
    text = text.replace('echo ============================================\r\n\r\necho [1/3]', 'echo ============================================\r\n\r\n' + ui + 'echo [1/3]')
    bat.write_text(text, encoding="utf-8")


def main():
    if DST.exists():
        shutil.rmtree(DST)
    DST.mkdir(parents=True)

    for src_rel, dst_rel in COPY_TREES:
        print("复制", src_rel)
        copy_tree(SRC / src_rel, DST / dst_rel)
    for src_rel, dst_rel in COPY_FILES:
        (DST / dst_rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SRC / src_rel, DST / dst_rel)
        print("复制", src_rel)

    (DST / "使用说明书.txt").write_text(MANUAL, encoding="utf-8")
    sanitize()
    patch_bat()

    print("压缩中（约 1-3 分钟）...")
    subprocess.run([str(SEVEN_ZIP), "a", "-t7z", "-mx=5", str(ZIP), str(DST / "*")], check=True)
    mb = ZIP.stat().st_size / 1048576
    print(f"完成: {ZIP}  ({mb:.0f} MB)")


if __name__ == "__main__":
    main()
