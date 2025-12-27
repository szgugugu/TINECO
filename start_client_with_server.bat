@echo off
echo SystemMonitor 客户端启动脚本
echo.
echo 使用方法:
echo 1. 直接运行此脚本将连接到本地服务器 (localhost:8000)
echo 2. 运行 "start_client_with_server.bat 服务器地址" 连接到指定服务器
echo    例如: start_client_with_server.bat http://192.168.1.100:8000
echo.

if "%~1"=="" (
    echo 没有指定服务器地址，使用默认地址: http://localhost:8000
    python start_client.py
) else (
    echo 使用服务器地址: %~1
    python start_client.py --server %~1
)

pause