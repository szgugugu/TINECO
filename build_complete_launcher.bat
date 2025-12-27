@echo off
echo 正在打包SystemMonitor启动器（包含Python环境）...

REM 创建临时目录存放Python环境
if not exist "temp_python" mkdir temp_python

REM 复制虚拟环境中的Python解释器和必要文件
echo 复制Python解释器...
copy ".venv\Scripts\python.exe" "temp_python\"
copy ".venv\Scripts\python311.dll" "temp_python\" 2>nul
copy ".venv\Scripts\python310.dll" "temp_python\" 2>nul
copy ".venv\Scripts\python39.dll" "temp_python\" 2>nul

REM 复制虚拟环境中的标准库
echo 复制Python标准库...
xcopy ".venv\Lib" "temp_python\Lib\" /E /I /Q /H /Y

REM 复制虚拟环境中的site-packages
echo 复制Python包...
xcopy ".venv\Lib\site-packages" "temp_python\Lib\site-packages\" /E /I /Q /H /Y

REM 使用PyInstaller打包
echo 使用PyInstaller打包...
pyinstaller --onefile --windowed --name SystemMonitorLauncher ^
    --add-data "backend;backend" ^
    --add-data "temp_python;python_env" ^
    backend_launcher.py

REM 清理临时文件
echo 清理临时文件...
rmdir /S /Q temp_python

echo 打包完成！
pause