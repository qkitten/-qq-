@echo off
chcp 65001 >nul
title NapCat 大肥鱼 QQ 机器人
cd /d "%~dp0NapCat.Shell"

set "NAPCAT_PATCH_PACKAGE=%cd%\qqnt.json"
set "NAPCAT_LOAD_PATH=%cd%\loadNapCat.js"
set "NAPCAT_INJECT_PATH=%cd%\NapCatWinBootHook.dll"
set "NAPCAT_LAUNCHER_PATH=%cd%\NapCatWinBootMain.exe"
set "NAPCAT_MAIN_PATH=%cd%\napcat.mjs"

echo ================================================
echo  正在用你已安装的 QQ 9.9.31 启动 NapCat
echo  请用 QQ 小号扫描控制台出现的二维码
echo ================================================
echo.

"%NAPCAT_LAUNCHER_PATH%" "C:\Program Files (x86)\Tencent\QQNT\QQ.exe" "%NAPCAT_INJECT_PATH%"

echo.
echo NapCat 已退出，错误码 %ERRORLEVEL%
pause
