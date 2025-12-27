#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试端口检测功能
"""
import subprocess
import time
import sys
import psutil

def test_port_detection():
    """测试端口检测功能"""
    print("=== 测试端口检测功能 ===")
    
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
    
    # 检查端口是否被占用
    print("2. 检查端口8000是否被占用...")
    port = 8000
    port_in_use = False
    found_connections = []
    
    try:
        for conn in psutil.net_connections():
            if conn.laddr.port == port and conn.status == 'LISTEN':
                port_in_use = True
                found_connections.append(conn)
                print(f"   找到占用端口的连接: {conn}")
        
        if port_in_use:
            print(f"   ✓ 端口 {port} 被占用")
            
            # 获取占用端口的进程
            for conn in found_connections:
                pid = conn.pid
                if pid:
                    try:
                        process = psutil.Process(pid)
                        print(f"   找到占用端口的进程: {process.name()} (PID: {pid})")
                        
                        # 尝试优雅地终止进程
                        print(f"   尝试停止进程 {pid}...")
                        process.terminate()
                        
                        # 等待进程退出
                        try:
                            process.wait(timeout=5)
                            print(f"   ✓ 成功停止进程 {pid}")
                        except psutil.TimeoutExpired:
                            # 如果进程不退出，强制杀死
                            print(f"   进程 {pid} 未响应，强制终止...")
                            process.kill()
                            process.wait(timeout=2)
                            print(f"   ✓ 强制终止进程 {pid}")
                            
                    except psutil.NoSuchProcess:
                        print(f"   进程 {pid} 已不存在")
                    except Exception as e:
                        print(f"   停止进程时出错: {str(e)}")
        else:
            print(f"   ✗ 端口 {port} 未被占用")
            
    except Exception as e:
        print(f"   ✗ 检查端口时出错: {str(e)}")
    
    # 等待端口释放
    if port_in_use:
        print("3. 等待端口释放...")
        for i in range(10):  # 最多等待10秒
            time.sleep(1)
            still_in_use = False
            try:
                for conn in psutil.net_connections():
                    if conn.laddr.port == port and conn.status == 'LISTEN':
                        still_in_use = True
                        break
            except:
                pass
            
            if not still_in_use:
                print(f"   ✓ 端口 {port} 已释放")
                break
        else:
            print(f"   ✗ 无法释放端口 {port}")
    
    # 确保测试服务器被停止
    try:
        if test_server.poll() is None:
            test_server.terminate()
            try:
                test_server.wait(timeout=2)
            except subprocess.TimeoutExpired:
                test_server.kill()
                test_server.wait(timeout=2)
            print("4. ✓ 已停止测试服务器")
    except:
        print("4. ✗ 停止测试服务器失败")
    
    print("=== 测试完成 ===")
    return True

if __name__ == "__main__":
    test_port_detection()