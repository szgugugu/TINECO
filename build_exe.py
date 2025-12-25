import os
import sys
import subprocess
import shutil

def build_exe():
    print("开始打包系统监控应用程序为exe文件...")
    
    # 检查是否安装了pyinstaller
    try:
        import PyInstaller
        print("已检测到PyInstaller")
    except ImportError:
        print("正在安装PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 创建图标目录（如果不存在）
    if not os.path.exists("dist"):
        os.makedirs("dist")
    
    # PyInstaller命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                        # 打包成单个exe文件
        "--noconsole",                      # 隐藏控制台窗口，后台运行
        "--name=TINECO_System_Monitor",     # exe文件名
        "--icon=icon.ico",                  # 应用程序图标
        "--add-data=icon.ico;.",           # 包含图标文件
        "--hidden-import=tkinter",         # 明确指定tkinter
        "--hidden-import=PIL.Image",        # 明确指定PIL
        "--hidden-import=PIL.ImageDraw",    # 明确指定PIL.ImageDraw
        "--hidden-import=matplotlib",      # 明确指定matplotlib
        "--hidden-import=matplotlib.backends.backend_tkagg", # 明确指定matplotlib后端
        "system_monitor.py"                 # 要打包的Python文件
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("打包成功!")
        print(f"可执行文件位于: {os.path.abspath('dist/TINECO_System_Monitor.exe')}")
        
        # 复制其他必要文件到dist目录
        if os.path.exists("icon.ico"):
            shutil.copy("icon.ico", "dist/")
            print("已复制图标文件到dist目录")
        
        # 创建启动脚本
        with open("dist/启动系统监控.bat", "w", encoding="utf-8") as f:
            f.write("@echo off\n")
            f.write("start TINECO_System_Monitor.exe\n")
        
        print("已创建启动脚本: 启动系统监控.bat")
        return True
    else:
        print("打包失败:")
        print(result.stderr)
        return False

if __name__ == "__main__":
    build_exe()