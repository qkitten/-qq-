@echo off
chcp 65001 >nul
title 大肥鱼机器人 - 一键启动
setlocal
set "ROOT=%~dp0"
set "PATH=%PATH%;%ROOT%tools\ffmpeg-9.0.2-full_build\bin"

echo ============================================
echo   大肥鱼 QQ 机器人 一键启动
echo ============================================

echo [1/3] 清理旧进程...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im NapCatWinBootMain.exe >nul 2>&1
taskkill /f /im QQ.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2/3] 启动 AstrBot...
start "AstrBot" /min /D "%ROOT%AstrBot" cmd /c "python -X utf8 -u main.py > "%ROOT%astrbot_out.log" 2> "%ROOT%astrbot_err.log""

echo      等待 AstrBot 就绪（最长 3 分钟）...
set /a tries=0
:wait_astrbot
timeout /t 3 /nobreak >nul
powershell -NoProfile -Command "try{ $c=New-Object Net.Sockets.TcpClient; $c.Connect('127.0.0.1',6199); $c.Close(); exit 0 }catch{ exit 1 }" >nul 2>&1
if not errorlevel 1 goto astrbot_ok
set /a tries+=1
if %tries% lss 60 goto wait_astrbot
echo      [警告] AstrBot 未在预期时间内就绪，仍继续启动 NapCat...
:astrbot_ok
echo      AstrBot 已就绪。

echo [3/3] 启动 NapCat（快速登录 QQ 3847176954）...
start "NapCat" /min /D "%ROOT%OneKey\NapCat.52230.Shell" cmd /k "chcp 65001 >nul && NapCatWinBootMain.exe 3847176954"

echo ============================================
echo   启动完成！本窗口可以关闭。
echo   WebUI:  http://127.0.0.1:6185
echo   日志:   astrbot_out.log / napcat_new.log
echo ============================================
timeout /t 5 /nobreak >nul
