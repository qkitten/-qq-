# -*- coding: utf-8 -*-
"""大肥鱼机器人配置 UI（端口 6200）。

可修改：
- 绑定的 QQ 号（写入 一键启动.bat 的 NapCat 快速登录参数）
- DeepSeek API Key（写入 AstrBot 的 provider_sources）
支持保存后一键重启 AstrBot / NapCat。
"""

import json
import os
import re
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # 脚本位于 <项目>/tools/ 下，项目根即上一级
CFG = ROOT / "AstrBot/data/cmd_config.json"
BAT = ROOT / "一键启动.bat"
FFMPEG_BIN = str(ROOT / "tools/ffmpeg-9.0.2-full_build/bin")
PORT = 6200

HTML = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>大肥鱼机器人 · 配置</title>
<style>
  :root{--bg:#0d1220;--card:#161d31;--line:#232c47;--txt:#e8edf7;--dim:#8b96b3;--acc:#4f8dff;--ok:#3ecf8e;--err:#ff6b6b}
  *{box-sizing:border-box;margin:0}
  body{background:var(--bg);color:var(--txt);font-family:"Microsoft YaHei",system-ui,sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:32px;width:100%;max-width:480px;box-shadow:0 12px 40px rgba(0,0,0,.45)}
  h1{font-size:20px;margin-bottom:4px}
  .sub{color:var(--dim);font-size:13px;margin-bottom:24px}
  label{display:block;font-size:13px;color:var(--dim);margin:16px 0 6px}
  input{width:100%;background:#0f1526;border:1px solid var(--line);border-radius:10px;color:var(--txt);padding:11px 13px;font-size:14px;outline:none}
  input:focus{border-color:var(--acc)}
  .row{display:flex;gap:8px;margin-top:4px}
  .row input{flex:1}
  button{cursor:pointer;border:none;border-radius:10px;padding:11px 14px;font-size:14px;font-weight:600;color:#fff}
  .ghost{background:var(--line);color:var(--dim)}
  .primary{background:var(--acc);width:100%;margin-top:24px}
  .actions{display:flex;gap:10px;margin-top:12px}
  .actions button{flex:1;font-weight:500;background:var(--line)}
  .actions button:hover{filter:brightness(1.2)}
  .msg{margin-top:16px;font-size:13px;min-height:18px}
  .ok{color:var(--ok)} .err{color:var(--err)}
  .whale{font-size:34px;text-align:center;margin-bottom:8px}
</style>
</head>
<body>
<div class="card">
  <div class="whale">🐳</div>
  <h1>大肥鱼机器人配置</h1>
  <div class="sub">修改后点「保存」，需要生效时再点对应重启按钮</div>

  <label>绑定的 QQ 号（机器人账号）</label>
  <input id="qq" placeholder="例如 3847176954" inputmode="numeric">

  <label>DeepSeek API Key</label>
  <div class="row">
    <input id="key" type="password" placeholder="sk-...">
    <button class="ghost" onclick="toggleKey()" type="button">显示</button>
  </div>

  <button class="primary" onclick="save()">保存</button>
  <div class="actions">
    <button onclick="restart('astrbot')">重启 AstrBot</button>
    <button onclick="restart('napcat')">重启 QQ(NapCat)</button>
  </div>
  <div class="msg" id="msg"></div>
</div>
<script>
const $=id=>document.getElementById(id);
function show(t,ok){const m=$('msg');m.textContent=t;m.className='msg '+(ok?'ok':'err')}
async function load(){
  const r=await fetch('/api/config');const j=await r.json();
  $('qq').value=j.qq||'';$('key').value=j.key||'';
}
async function save(){
  const qq=$('qq').value.trim(),key=$('key').value.trim();
  if(!/^\\d{5,12}$/.test(qq)){show('QQ 号格式不对',false);return}
  const r=await fetch('/api/config',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({qq,key})});
  const j=await r.json();show(j.message,j.ok);
}
async function restart(t){
  if(!confirm('确定重启'+(t==='astrbot'?' AstrBot':'QQ(NapCat)')+'？'))return;
  show('正在重启…',true);
  const r=await fetch('/api/restart',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target:t})});
  const j=await r.json();show(j.message,j.ok);
}
function toggleKey(){const k=$('key');k.type=k.type==='password'?'text':'password'}
load();
</script>
</body>
</html>"""


def read_config():
    return json.loads(CFG.read_text(encoding="utf-8-sig"))


def write_config(d):
    tmp = CFG.with_suffix(".tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(CFG)


def get_values():
    d = read_config()
    qq = ""
    if BAT.exists():
        m = re.search(r"NapCatWinBootMain\.exe (\d+)", BAT.read_text(encoding="utf-8"))
        qq = m.group(1) if m else ""
    key = ""
    for s in d.get("provider_sources", []):
        if s.get("id", "").startswith("deepseek"):
            k = s.get("key", "")
            key = k[0] if isinstance(k, list) and k else (k if isinstance(k, str) else "")
    return qq, key


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            self._send(200, HTML, "text/html; charset=utf-8")
        elif self.path == "/api/config":
            qq, key = get_values()
            self._send(200, json.dumps({"qq": qq, "key": key}, ensure_ascii=False))
        else:
            self._send(404, '{"ok":false,"message":"not found"}')

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            self._send(400, '{"ok":false,"message":"请求格式错误"}')
            return

        if self.path == "/api/config":
            qq = str(payload.get("qq", "")).strip()
            key = str(payload.get("key", "")).strip()
            if not re.fullmatch(r"\d{5,12}", qq):
                self._send(400, '{"ok":false,"message":"QQ 号格式不对"}')
                return
            # 1) 写 bat（QQ 号）
            if BAT.exists():
                text = BAT.read_text(encoding="utf-8")
                text = re.sub(r"NapCatWinBootMain\.exe \d+", f"NapCatWinBootMain.exe {qq}", text)
                BAT.write_text(text, encoding="utf-8")
            # 2) 写 API key
            d = read_config()
            hit = False
            for s in d.get("provider_sources", []):
                if s.get("id", "").startswith("deepseek"):
                    s["key"] = [key] if isinstance(s.get("key"), list) else key
                    hit = True
            if hit:
                write_config(d)
            msg = "已保存（QQ + API Key）" if hit else "已保存 QQ；未找到 DeepSeek 供应商，key 未写入"
            self._send(200, json.dumps({"ok": True, "message": msg}, ensure_ascii=False))

        elif self.path == "/api/restart":
            target = payload.get("target")
            try:
                if target == "astrbot":
                    subprocess.run(["taskkill", "/f", "/im", "python.exe"],
                                   capture_output=True)
                    subprocess.Popen(
                        ["python", "-X", "utf8", "-u", "main.py"],
                        cwd=str(ROOT / "AstrBot"),
                        env={**os.environ, "Path": os.environ["Path"] + ";" + FFMPEG_BIN},
                        stdout=open(ROOT / "astrbot_out.log", "w", encoding="utf-8"),
                        stderr=open(ROOT / "astrbot_err.log", "w", encoding="utf-8"),
                        creationflags=subprocess.CREATE_NO_WINDOW,
                    )
                    self._send(200, '{"ok":true,"message":"AstrBot 重启中，约 1 分钟生效"}')
                elif target == "napcat":
                    for name in ("NapCatWinBootMain.exe", "QQ.exe"):
                        subprocess.run(["taskkill", "/f", "/im", name], capture_output=True)
                    nap_dir = ROOT / "OneKey/NapCat.52230.Shell"
                    qq, _ = get_values()
                    subprocess.Popen(
                        f'cmd /k "chcp 65001 >nul && NapCatWinBootMain.exe {qq}"',
                        cwd=str(nap_dir), shell=True,
                        creationflags=subprocess.CREATE_NEW_CONSOLE,
                    )
                    self._send(200, '{"ok":true,"message":"QQ(NapCat) 重启中，若弹二维码请扫码"}')
                else:
                    self._send(400, '{"ok":false,"message":"未知重启目标"}')
            except Exception as exc:
                self._send(500, json.dumps({"ok": False, "message": f"重启失败: {exc}"}, ensure_ascii=False))
        else:
            self._send(404, '{"ok":false,"message":"not found"}')

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"配置 UI: http://127.0.0.1:{PORT}")
    server.serve_forever()
