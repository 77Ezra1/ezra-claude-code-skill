@echo off
chcp 65001 >nul
set /p url="请输入公众号文章链接: "
cd /d "%~dp0"
python scripts\save_article_visual_cn.py "%url%"
pause
