@echo off
chcp 65001 >nul
cd /d "%~dp0"
python scripts\wechat_cli_cn.py
pause
