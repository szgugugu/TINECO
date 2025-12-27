@echo off
echo 正在打包后端启动软件...

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
    set ICON_OPTION=--icon=icon.ico --add-data="icon.ico;."
)

REM 添加backend目录到打包文件中
set DATA_OPTION=--add-data="backend;backend"

REM 使用PyInstaller打包
echo 正在使用PyInstaller打包...
pyinstaller --onefile --windowed %ICON_OPTION% %DATA_OPTION% --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=requests --hidden-import=webbrowser --name=BackendLauncher backend_launcher.py

if %ERRORLEVEL% NEQ 0 (
    echo 打包失败！
    pause
    exit /b 1
)

echo 打包完成！
echo 可执行文件位置: dist\BackendLauncher.exe
pause