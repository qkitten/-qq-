# 一键安装：官方 QQ Bot 三步接入（路线一）
$ErrorActionPreference = "Stop"

if (-not $env:DEEPSEEK_API_KEY) {
    Write-Host "[!] 请先设置环境变量: `$env:DEEPSEEK_API_KEY = '你的key'" -ForegroundColor Yellow
    exit 1
}

Write-Host "[1/3] 安装 QQ Bot 插件..." -ForegroundColor Cyan
npx @deepseek-ai/dsh plugin --profile qqbot add @tencent-connect/dsh-qqbot

Write-Host "[2/3] (可选) 安装大肥鱼人设插件..." -ForegroundColor Cyan
npx @deepseek-ai/dsh plugin add github:huaizhuanghub/dsh-persona-dafeiyu

Write-Host "[3/3] 启动 dsh（首次启动扫码绑定 QQ Bot）..." -ForegroundColor Cyan
npx @deepseek-ai/dsh --profile qqbot
