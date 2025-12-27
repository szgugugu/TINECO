#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试后端启动器功能
"""

import os
import sys
import subprocess
import tkinter as tk

# 添加当前目录到路径，以便导入backend_launcher
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend_launcher import BackendLauncher

def test_server_startup():
    """测试服务器启动"""
    print("开始测试服务器启动...")
    
    # 创建一个隐藏的Tkinter根窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏窗口
    
    # 创建启动器实例
    launcher = BackendLauncher(root)
    
    # 设置测试参数
    launcher.host_var.set("127.0.0.1")
    launcher.port_var.set("8000")
    
    # 获取后端目录
    backend_dir = launcher.get_backend_dir()
    print(f"后端目录: {backend_dir}")
    
    # 检查关键文件
    main_py = os.path.join(backend_dir, "main.py")
    print(f"main.py路径: {main_py}")
    print(f"main.py是否存在: {os.path.exists(main_py)}")
    
    # 检查其他关键文件
    critical_files = ["api", "core", "models", "database.py", "requirements.txt"]
    for item in critical_files:
        item_path = os.path.join(backend_dir, item)
        print(f"{item}是否存在: {os.path.exists(item_path)}")
    
    # 检查Python环境
    if getattr(sys, 'frozen', False):
        print("打包环境")
        try:
            result = subprocess.run(["python", "--version"], capture_output=True, text=True, timeout=5)
            print(f"Python版本: {result.stdout.strip()}")
        except Exception as e:
            print(f"无法找到Python解释器: {str(e)}")
    else:
        print("开发环境")
        print(f"Python解释器: {sys.executable}")
    
    # 尝试启动服务器
    print("\n尝试启动服务器...")
    try:
        launcher.start_server()
        
        # 等待一段时间检查服务器状态
        import time
        time.sleep(5)
        
        # 检查服务器是否启动成功
        launcher.check_server_started()
        
    except Exception as e:
        print(f"启动服务器时发生异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_server_startup()