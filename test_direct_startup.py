#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试服务器启动功能
"""

import os
import sys
import subprocess
import threading
import time

def test_server_startup():
    """测试服务器启动"""
    print("开始测试服务器启动...")
    
    # 模拟打包环境
    is_frozen = getattr(sys, 'frozen', False)
    print(f"是否为打包环境: {is_frozen}")
    
    # 获取后端目录
    if is_frozen:
        # 打包后的exe，backend目录在临时目录中
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        print(f"打包环境，临时目录: {base_dir}")
        # 检查临时目录中是否有backend
        temp_backend_dir = os.path.join(base_dir, "backend")
        print(f"临时目录中的backend路径: {temp_backend_dir}")
        print(f"临时目录中的backend是否存在: {os.path.exists(temp_backend_dir)}")
        
        if os.path.exists(temp_backend_dir):
            backend_dir = temp_backend_dir
        else:
            # 如果临时目录中没有backend，尝试使用exe所在目录
            exe_dir = os.path.dirname(sys.executable)
            print(f"exe所在目录: {exe_dir}")
            backend_dir = os.path.join(exe_dir, "backend")
    else:
        # 开发环境
        base_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"开发环境，当前目录: {base_dir}")
        backend_dir = os.path.join(base_dir, "backend")
    
    print(f"后端目录: {backend_dir}")
    
    # 检查关键文件
    main_py = os.path.join(backend_dir, "main.py")
    print(f"main.py路径: {main_py}")
    print(f"main.py是否存在: {os.path.exists(main_py)}")
    
    if not os.path.exists(main_py):
        print(f"错误: 找不到main.py文件: {main_py}")
        return
    
    # 检查其他关键文件
    critical_files = ["main.py", "requirements.txt", "templates"]
    missing_files = []
    
    for item in critical_files:
        item_path = os.path.join(backend_dir, item)
        if not os.path.exists(item_path):
            missing_files.append(item)
    
    if missing_files:
        print(f"错误: 以下关键文件或目录缺失:")
        for item in missing_files:
            print(f"  - {item}")
        return
    
    # 检查Python环境
    if is_frozen:
        # 在打包环境中，检查python命令是否可用
        try:
            result = subprocess.run(["python", "--version"], capture_output=True, text=True, timeout=5)
            print(f"Python版本: {result.stdout.strip()}")
        except Exception as e:
            print(f"错误: 无法找到Python解释器: {str(e)}")
            return
    
    # 构建启动命令
    if is_frozen:
        # 打包后的环境，直接使用python命令
        python_exe = "python"
        print(f"使用的Python解释器: {python_exe}")
        
        # 直接运行main.py而不是使用uvicorn模块
        cmd = [
            python_exe, "main.py",
            "--host", "127.0.0.1",
            "--port", "8000"
        ]
    else:
        # 开发环境，使用当前Python解释器和uvicorn模块
        python_exe = sys.executable
        print(f"开发环境，使用的Python解释器: {python_exe}")
        
        cmd = [
            python_exe, "-m", "uvicorn", "main:app",
            "--host", "127.0.0.1",
            "--port", "8000"
        ]
    
    print(f"启动命令: {' '.join(cmd)}")
    print(f"工作目录: {backend_dir}")
    
    # 启动服务器进程
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        # Windows特定的创建标志
        creationflags = 0
        if os.name == 'nt':
            creationflags = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
        
        server_process = subprocess.Popen(
            cmd,
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            startupinfo=startupinfo,
            creationflags=creationflags
        )
        
        # 启动一个线程来读取进程输出
        server_output = []
        server_errors = []
        
        def read_output():
            try:
                # 读取标准输出
                for line in iter(server_process.stdout.readline, ''):
                    if line:
                        server_output.append(line.strip())
                        print(f"服务器输出: {line.strip()}")
                
                # 读取错误输出
                for line in iter(server_process.stderr.readline, ''):
                    if line:
                        server_errors.append(line.strip())
                        print(f"服务器错误: {line.strip()}")
            except Exception as e:
                print(f"读取进程输出异常: {str(e)}")
        
        output_thread = threading.Thread(target=read_output, daemon=True)
        output_thread.start()
        
        # 等待服务器启动
        print("等待服务器启动...")
        time.sleep(5)
        
        # 检查进程是否还在运行
        if server_process.poll() is not None:
            # 进程已退出
            exit_code = server_process.returncode
            print(f"服务器进程已退出，退出码: {exit_code}")
            
            # 尝试从错误输出中提取文件找不到的具体信息
            missing_file = None
            if server_errors:
                for error_line in server_errors:
                    if "No such file or directory" in error_line or "找不到指定文件" in error_line or "FileNotFoundError" in error_line:
                        # 尝试提取文件路径
                        import re
                        file_match = re.search(r"'([^']+)'", error_line)
                        if file_match:
                            missing_file = file_match.group(1)
                        break
            
            # 构建详细的错误消息
            error_msg = f"服务器启动失败，退出码: {exit_code}"
            
            if missing_file:
                error_msg = f"找不到指定文件: {missing_file}"
            
            if server_errors:
                error_msg += "\n\n错误信息:\n" + "\n".join(server_errors[-10:])
            
            if server_output:
                error_msg += "\n\n输出信息:\n" + "\n".join(server_output[-10:])
            
            print(error_msg)
        else:
            print("服务器进程正在运行")
        
        # 停止服务器
        print("停止服务器...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
        
    except Exception as e:
        print(f"启动服务器异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_server_startup()