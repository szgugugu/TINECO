#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动化测试GUI版本的启动器
"""
import os
import sys
import time
import subprocess
import requests
import threading
from tkinter import ttk

def test_gui_launcher():
    """测试GUI版本的启动器"""
    print("=== 测试GUI版本的启动器 ===")
    
    release_dir = os.path.join(os.path.dirname(__file__), 'release')
    launcher_exe = os.path.join(release_dir, 'SystemMonitorLauncher.exe')
    
    if not os.path.exists(launcher_exe):
        print(f"✗ 找不到启动器: {launcher_exe}")
        return False
    
    print(f"✓ 找到启动器: {launcher_exe}")
    
    # 导入GUI模块
    sys.path.insert(0, os.path.dirname(__file__))
    from backend_launcher import BackendLauncher
    
    # 创建一个虚拟的root窗口
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # 隐藏窗口
    
    # 创建后端启动器实例
    launcher = BackendLauncher(root)
    
    # 测试启动服务器
    print("\n1. 启动服务器...")
    # 添加更多调试信息
    print(f"端口: {launcher.port_var.get()}")
    print(f"主机: {launcher.host_var.get()}")
    print(f"后端目录: {launcher.get_backend_dir()}")
    
    success = launcher.start_server()
    print(f"start_server返回值: {success}")  # 添加调试信息
    if success:
        print("✓ 服务器启动命令已发送")
    else:
        print("✗ 服务器启动命令发送失败")
        # 尝试获取错误信息
        if hasattr(launcher, 'server_errors') and launcher.server_errors:
            print("错误信息:", "\n".join(launcher.server_errors))
        root.destroy()
        return False
    
    # 等待服务器完全启动
    print("\n2. 等待服务器完全启动...")
    time.sleep(10)
    
    # 检查服务器状态
    print("\n3. 检查服务器状态...")
    # 手动调用check_server_started方法，因为Tkinter事件循环在测试中可能不会正常运行
    try:
        launcher.check_server_started()
        if hasattr(launcher, 'is_server_running') and launcher.is_server_running:
            print("✓ 服务器状态为运行中")
        else:
            print("✗ 服务器状态为未运行")
            # 尝试获取更多调试信息
            if hasattr(launcher, 'server_errors') and launcher.server_errors:
                print("服务器错误:", "\n".join(launcher.server_errors))
            if hasattr(launcher, 'server_output') and launcher.server_output:
                print("服务器输出:", "\n".join(launcher.server_output))
            root.destroy()
            return False
    except Exception as e:
        print(f"✗ 检查服务器状态时发生异常: {e}")
        root.destroy()
        return False
    
    # 测试服务器响应
    print("\n4. 测试服务器响应...")
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        if response.status_code == 200:
            print("✓ 服务器响应正常")
        else:
            print(f"✗ 服务器响应异常: {response.status_code}")
            launcher.stop_server()
            root.destroy()
            return False
    except Exception as e:
        print(f"✗ 无法连接到服务器: {e}")
        launcher.stop_server()
        root.destroy()
        return False
    
    # 测试停止服务器
    print("\n5. 停止服务器...")
    success = launcher.stop_server()
    if success:
        print("✓ 服务器停止成功")
    else:
        print("✗ 服务器停止失败")
        root.destroy()
        return False
    
    # 销毁窗口
    root.destroy()
    
    return True

if __name__ == "__main__":
    success = test_gui_launcher()
    if success:
        print("\n=== 测试结果: 通过 ===")
        print("✓ GUI版本的启动器测试成功！")
        print("✓ Python解释器问题已修复！")
    else:
        print("\n=== 测试结果: 失败 ===")
        print("✗ GUI版本的启动器测试失败！")