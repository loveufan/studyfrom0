@echo off
chcp 65001 > nul
cd /d f:\studyfrom0
python 上传脚本\git_auto_update.py %*
pause