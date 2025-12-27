#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试修复后的backend_launcher.py
"""
import os
import sys
import tkinter as tk

# 添加backend目录到Python路径
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# 导入修复后的backend_launcher
from backend_launcher import BackendLauncher

def test_backend_launcher():
    """测试后端启动器"""
    print("测试修复后的后端启动器...")
    
    # 创建一个虚拟的root窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏窗口
    
    # 创建后端启动器实例
    launcher = BackendLauncher(root)
    
    # 测试启动服务器
    print("尝试启动服务器...")
    try:
        success = launcher.start_server()
        if success:
            print("✓ 服务器启动成功")
            
            # 等待几秒钟让服务器完全启动
            import time
            time.sleep(5)
            
            # 测试停止服务器
            print("尝试停止服务器...")
            success = launcher.stop_server()
            if success:
                print("✓ 服务器停止成功")
            else:
                print("✗ 服务器停止失败")
        else:
            print("✗ 服务器启动失败")
    except Exception as e:
        print(f"✗ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 销毁窗口
        root.destroy()

if __name__ == "__main__":
    test_backend_launcher()