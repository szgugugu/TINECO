@echo off
title SystemMonitor 远程监控系统启动器

echo.
echo ========================================
echo    SystemMonitor 远程监控系统
echo ========================================
echo.
echo 请选择要执行的操作：
echo.
echo 1. 启动后端服务器
echo 2. 启动客户端
echo 3. 启动测试程序
echo 4. 同时启动后端服务器和客户端
echo 5. 退出
echo.

set /p choice=请输入选项 (1-5): 

if "%choice%"=="1" (
    echo.
    echo 正在启动后端服务器...
    python start_backend.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo 正在启动客户端...
    python start_client.py
    pause
) else if "%choice%"=="3" (
    echo.
    echo 正在启动测试程序...
    echo 请确保后端服务器已启动！
    python test_system.py
    pause
) else if "%choice%"=="4" (
    echo.
    echo 正在同时启动后端服务器和客户端...
    echo 首先启动后端服务器...
    start "SystemMonitor 后端服务器" cmd /k "python start_backend.py"
    echo 等待服务器启动...
    timeout /t 5 /nobreak > nul
    echo 启动客户端...
    start "SystemMonitor 客户端" cmd /k "python start_client.py"
    echo.
    echo 系统已启动！
    echo 监控面板: http://localhost:8000
    echo 配置管理: http://localhost:8000/config
    echo.
    pause
) else if "%choice%"=="5" (
    exit
) else (
    echo.
    echo 无效选项，请重新运行脚本！
    pause
)