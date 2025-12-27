#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试main.py中的端口检测部分
"""
import sys
import os
import argparse
import psutil
import time

# 切换到后端目录
backend_dir = os.path.join(os.path.dirname(__file__), "backend")
os.chdir(backend_dir)

# 模拟命令行参数
sys.argv = ["main.py", "--host", "127.0.0.1", "--port", "8000"]

# 解析命令行参数
parser = argparse.ArgumentParser(description="SystemMonitor 后端服务器")
parser.add_argument("--host", default="0.0.0.0", help="服务器主机地址")
parser.add_argument("--port", type=int, default=8000, help="服务器端口号")
args = parser.parse_args()

print(f"检查端口 {args.port} 是否被占用...")

# 检查端口是否被占用
port_in_use = False
connections = []
for conn in psutil.net_connections():
    if conn.laddr.port == args.port and conn.status == 'LISTEN':
        port_in_use = True
        connections.append(conn)
        print(f"找到占用端口的连接: {conn}")

if port_in_use:
    print(f"端口 {args.port} 已被占用，尝试停止占用该端口的进程...")
    
    # 获取占用端口的进程ID
    for conn in connections:
        pid = conn.pid
        if pid:
            try:
                process = psutil.Process(pid)
                print(f"找到占用端口的进程: {process.name()} (PID: {pid})")
                
                # 尝试优雅地终止进程
                process.terminate()
                
                # 等待进程退出
                try:
                    process.wait(timeout=5)
                    print(f"成功停止进程 {pid}")
                except psutil.TimeoutExpired:
                    # 如果进程不退出，强制杀死
                    print(f"进程 {pid} 未响应，强制终止...")
                    process.kill()
                    process.wait(timeout=2)
                    print(f"强制终止进程 {pid}")
                    
            except psutil.NoSuchProcess:
                print(f"进程 {pid} 已不存在")
            except Exception as e:
                print(f"停止进程时出错: {str(e)}")
                sys.exit(1)
        
        break

# 等待端口释放
if port_in_use:
    print("等待端口释放...")
    for i in range(10):  # 最多等待10秒
        time.sleep(1)
        still_in_use = False
        for conn in psutil.net_connections():
            if conn.laddr.port == args.port and conn.status == 'LISTEN':
                still_in_use = True
                break
        
        if not still_in_use:
            print(f"端口 {args.port} 已释放")
            break
    else:
        print(f"无法释放端口 {args.port}，请手动检查")
        sys.exit(1)
else:
    print(f"端口 {args.port} 未被占用")