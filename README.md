# 🐳 大肥鱼 QQ 机器人

> 一条住在你服务器里的蓝色鲸鱼娘。会陪聊、会怼人、会发表情包、会点歌、还会记日记。

基于 [AstrBot](https://github.com/AstrBotDevs/AstrBot) + [NapCat](https://github.com/NapNeko/NapCatQQ) 打造的**本地一键部署** QQ 机器人，开箱即用，无需服务器运维经验。

## ✨ 功能

- 💬 **拟人化聊天** — 短句、口语化、会阴阳怪气，没有 AI 客服腔
- 🖼️ **表情包自由** — 内置 180+ 张专属动图，按情绪自动配图；支持 `/存表情` 让它学习群友的梗图；没图还能现场画
- 🎵 **点歌听歌** — 对它说"放歌 + 歌名"，自动搜索 B 站并转成 QQ 语音发送
- 🧠 **长期记忆** — 自动记住群友的喜好和聊过的事，隔天能接上旧话题
- 📔 **自动写日志** — 话题告一段落就悄悄记流水账，翻旧账一绝
- 👥 **@人互动** — 回复里可以真正艾特指定群友
- 🎛️ **配置面板** — 网页一键修改 API Key / 绑定 QQ，一键重启

## 📦 项目结构

```
├── 一键启动.bat / 一键停止.bat   # Windows 启停脚本
├── 安装依赖.bat                  # 首次使用安装 Python 依赖
├── 使用说明书.txt                # 新手向完整说明
├── AstrBot/                      # 机器人主程序（人格/插件/表情包库在 data/ 下）
│   └── data/plugins/             # 内置插件：表情包 / 点歌 / 记忆 / @人 …
├── OneKey/NapCat.52230.Shell/    # QQ 协议端（NapCat）
└── tools/
    ├── ffmpeg-9.0.2-full_build/  # 音频转码（点歌必需）
    └── config_ui.py              # 配置面板（http://127.0.0.1:6200）
```

## 🚀 快速开始（Windows）

> 前置要求：Windows 10/11、Python 3.10+（安装时勾选 *Add python.exe to PATH*）

1. 克隆或下载本仓库
2. 双击 **`安装依赖.bat`**（只需一次，需联网）
3. 双击 **`一键启动.bat`** —— 自动打开配置面板
4. 在面板里填入：
   - **API Key**：到 [DeepSeek 开放平台](https://platform.deepseek.com/) 注册并创建（`sk-` 开头）
   - **QQ 号**：作为机器人的 QQ 账号
5. 点「保存」→「重启 AstrBot」，QQ 弹出二维码后用手机 QQ 扫码登录
6. 用另一个 QQ 加它好友或拉进群，开聊 🎉

## 🎮 聊天玩法

| 玩法 | 示例 |
|------|------|
| 日常闲聊 | 直接说话（群里 @它 或叫它名字） |
| 点歌 | `放黄昏` |
| 教表情包 | `/存表情 鄙视` 然后发一张图 |
| 查表情库 | `/表情库` |
| 查看记忆 | 直接问它"你还记得我吗" |

## ⚙️ 端口一览

| 端口 | 用途 |
|------|------|
| 6185 | AstrBot WebUI 管理后台（默认 `astrbot / astrbot`，**部署后请立即改密码**） |
| 6199 | OneBot 反向 WebSocket |
| 6200 | 配置面板 |

## 🧩 技术栈

- [AstrBot](https://github.com/AstrBotDevs/AstrBot) — 多平台 LLM 机器人框架
- [NapCatQQ](https://github.com/NapNeko/NapCatQQ) — 无头 QQ 协议端（OneBot 11）
- DeepSeek API — 大模型对话
- 自研插件：`feiyu_meme`（表情包）、`listen_music`（点歌）、`ai_memory`（记忆）、`at_tagger`（@人）

## ⚠️ 免责声明

- 仅供个人学习与娱乐使用，请遵守 QQ 用户协议与当地法律法规
- 请勿用于批量营销、骚扰等用途，账号风险自负
- 本项目不收集任何用户数据，所有数据均保存在本地

## 📄 License

[MIT](LICENSE)
