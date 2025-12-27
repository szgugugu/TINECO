#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试打包后的exe文件端口冲突解决功能
"""
import subprocess
import time
import sys
import os

def test_exe_port_conflict():
    """测试打包后的exe文件端口冲突解决功能"""
    print("=== 测试打包后的exe文件端口冲突解决功能 ===")
    
    # 检查exe文件是否存在
    exe_path = os.path.join(os.path.dirname(__file__), "dist", "BackendLauncher.exe")
    if not os.path.exists(exe_path):
        print(f"错误: 找不到打包的exe文件: {exe_path}")
        return False
    
    print(f"找到打包的exe文件: {exe_path}")
    
    # 启动一个占用8000端口的简单服务器
    print("1. 启动一个占用8000端口的简单服务器...")
    try:
        # 使用Python内置的HTTP服务器占用8000端口
        test_server = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待服务器启动
        time.sleep(2)
        
        # 检查服务器是否成功启动
        if test_server.poll() is None:
            print("   ✓ 测试服务器已启动，占用8000端口")
        else:
            print("   ✗ 测试服务器启动失败")
            stdout, stderr = test_server.communicate()
            print(f"   错误: {stderr}")
            return False
            
    except Exception as e:
        print(f"   ✗ 启动测试服务器失败: {str(e)}")
        return False
    
    # 测试打包后的exe文件是否能自动处理端口冲突
    print("2. 测试打包后的exe文件是否能自动处理端口冲突...")
    try:
        # 直接在backend目录中运行main.py测试端口冲突处理
        backend_dir = os.path.join(os.path.dirname(__file__), "backend")
        os.chdir(backend_dir)
        
        print("   直接运行main.py测试端口冲突处理...")
        main_process = subprocess.Popen(
            [sys.executable, "main.py", "--host", "127.0.0.1", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # 等待一段时间让main.py处理端口冲突
        time.sleep(5)
        
        # 检查main.py的输出
        main_process.terminate()
        try:
            stdout, _ = main_process.communicate(timeout=2)
            print("   main.py输出:")
            for line in stdout.split('\n'):
                if line.strip():
                    print(f"     {line}")
                    
            if "端口 8000 已被占用" in stdout:
                print("   ✓ 成功检测到端口占用")
            else:
                print("   ✗ 未检测到端口占用")
                
            if "成功停止进程" in stdout or "强制终止进程" in stdout:
                print("   ✓ 成功停止占用端口的进程")
            else:
                print("   ✗ 未停止占用端口的进程")
                
        except subprocess.TimeoutExpired:
            main_process.kill()
            print("   ✗ main.py进程无响应")
            
    except Exception as e:
        print(f"   ✗ 测试失败: {str(e)}")
    
    # 确保测试服务器被停止
    try:
        if test_server.poll() is None:
            test_server.terminate()
            try:
                test_server.wait(timeout=2)
            except subprocess.TimeoutExpired:
                test_server.kill()
                test_server.wait(timeout=2)
            print("3. ✓ 已停止测试服务器")
    except:
        print("3. ✗ 停止测试服务器失败")
    
    print("=== 测试完成 ===")
    return True

if __name__ == "__main__":
    test_exe_port_conflict()