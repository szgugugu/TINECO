@echo off
echo 启动SystemMonitor客户端...
echo.
echo 使用说明：
echo 1. 确保后端服务器已启动
echo 2. 可以通过命令行参数指定服务器地址
echo    例如: SystemMonitor.exe --server http://192.168.1.100:8000
echo.

:: 启动exe文件
dist\SystemMonitor.exe %*

pause