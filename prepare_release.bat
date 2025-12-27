@echo off
echo 准备发布目录结构...

REM 创建发布目录
if not exist "release" mkdir release
if not exist "release\backend" mkdir release\backend

REM 复制backend目录内容到发布目录
echo 复制backend目录内容...
xcopy /E /I /Y backend release\backend

REM 复制打包后的exe文件
echo 复制exe文件...
if exist "dist\SystemMonitorLauncher.exe" (
    copy /Y dist\SystemMonitorLauncher.exe release\
) else (
    echo 错误: 找不到打包后的exe文件，请先运行 build_launcher_only.bat
    pause
    exit /b 1
)

REM 复制配置文件（如果存在）
if exist "backend_config.json" (
    copy /Y backend_config.json release\
)

REM 复制图标文件（如果存在）
if exist "icon.ico" (
    copy /Y icon.ico release\
)

REM 创建README文件
echo 创建README文件...
echo SystemMonitor 后端服务 > release\README.txt
echo. >> release\README.txt
echo 使用说明: >> release\README.txt
echo 1. 双击运行 SystemMonitorLauncher.exe >> release\README.txt
echo 2. 在界面中配置服务器地址和端口 >> release\README.txt
echo 3. 点击"启动服务器"按钮启动后端服务 >> release\README.txt
echo. >> release\README.txt
echo 注意: 请勿删除backend文件夹及其内容 >> release\README.txt

echo.
echo 发布目录准备完成！
echo 发布目录位置: release\
echo.
echo 目录结构:
release\
echo ├── SystemMonitorLauncher.exe
echo ├── backend\
echo │   └── [后端文件]
echo └── README.txt
echo.
pause