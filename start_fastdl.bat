@echo off
title CS 1.6 FastDL (nginx)
cd /d "D:\csServer\nginx\nginx-1.31.0"
echo Starting nginx FastDL on port 8080...
nginx.exe
echo nginx running. Press any key to stop.
pause >nul
nginx.exe -s stop
echo Stopped.
