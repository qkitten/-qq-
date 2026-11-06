@echo off
chcp 65001 >nul
title 大肥鱼机器人 - 一键停止
echo 正在停止 AstrBot / NapCat / QQ ...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im NapCatWinBootMain.exe >nul 2>&1
taskkill /f /im QQ.exe >nul 2>&1
echo 已全部停止。
timeout /t 3 /nobreak >nul
