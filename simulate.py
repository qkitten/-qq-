# -*- coding: utf-8 -*-
"""本地人设模拟器：不接 QQ 也能测大肥鱼人设是否生效。
用法: python simulate.py "今天吃什么"
"""
import os
import sys
import urllib.request
import json


def load_persona() -> str:
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persona", "dafeiyu.md")
    with open(path, encoding="utf-8") as f:
        return f.read()


def main() -> None:
    if len(sys.argv) < 2:
        print('用法: python simulate.py "今天吃什么"')
        sys.exit(1)
    user_msg = " ".join(sys.argv[1:])
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("[!] 未设置 DEEPSEEK_API_KEY，仅打印人设预览:\n")
        print(load_persona())
        return

    body = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": load_persona()},
            {"role": "user", "content": user_msg},
        ],
        "max_tokens": 300,
    }).encode()

    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.load(resp)
    print(data["choices"][0]["message"]["content"])


if __name__ == "__main__":
    main()
