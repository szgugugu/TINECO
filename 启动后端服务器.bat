@echo off
echo 启动SystemMonitor后端服务器...
echo.

REM 检查是否存在后端启动器
if exist "dist\BackendLauncher.exe" (
    echo 使用图形界面启动后端服务器...
    start "" "dist\BackendLauncher.exe"
) else (
    echo 错误: 找不到后端启动器，请先运行打包脚本
    pause
)