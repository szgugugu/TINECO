import sys
import os
import time
import threading
import tkinter as tk

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入BackendLauncher
from backend_launcher_debug2 import BackendLauncher

def auto_test_launcher():
    """自动测试启动器"""
    print("=== 自动测试启动器 ===")
    
    # 创建一个虚拟的root窗口
    root = tk.Tk()
    
    # 创建后端启动器实例
    launcher = BackendLauncher(root)
    
    # 等待GUI初始化完成
    root.update()
    
    # 模拟点击启动按钮
    def click_start_button():
        print("模拟点击启动按钮...")
        launcher.start_server()
    
    # 延迟执行点击操作
    root.after(1000, click_start_button)
    
    # 5秒后关闭窗口
    def close_window():
        print("关闭窗口...")
        root.quit()
    
    root.after(10000, close_window)
    
    # 运行GUI
    root.mainloop()

if __name__ == "__main__":
    auto_test_launcher()