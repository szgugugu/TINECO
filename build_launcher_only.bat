@echo off
echo 正在打包后端启动软件（仅启动程序）...

REM 检查是否存在虚拟环境
if not exist ".venv\Scripts\activate.bat" (
    echo 错误: 未找到虚拟环境，请先运行 setup_venv.bat 创建虚拟环境
    pause
    exit /b 1
)

REM 激活虚拟环境
call .venv\Scripts\activate.bat

REM 检查是否存在图标文件
set ICON_OPTION=
if exist "icon.ico" (
    set ICON_OPTION=--icon=icon.ico
)

REM 使用PyInstaller只打包启动程序，不包含backend目录
echo 正在使用PyInstaller打包启动程序...
pyinstaller --onefile --windowed %ICON_OPTION% --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=requests --hidden-import=webbrowser --name=SystemMonitorLauncher backend_launcher.py

if %ERRORLEVEL% NEQ 0 (
    echo 打包失败！
    pause
    exit /b 1
)

echo 打包完成！
echo 可执行文件位置: dist\SystemMonitorLauncher.exe
echo.
echo 注意：请确保backend文件夹与exe文件在同一目录下
pause