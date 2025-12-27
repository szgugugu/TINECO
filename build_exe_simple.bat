@echo off
echo 正在打包SystemMonitor客户端为exe文件...

:: 确保所有依赖项已安装
pip install -r client_requirements.txt

:: 使用PyInstaller打包
pyinstaller --onefile --windowed --icon=icon.ico --add-data="icon.ico;." --add-data="client_config.py;." --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=PIL.ImageGrab --hidden-import=win32clipboard --hidden-import=win32con --hidden-import=psutil --hidden-import=requests --name=SystemMonitor system_monitor.py

echo 打包完成！
echo 可执行文件位于 dist\SystemMonitor.exe
pause