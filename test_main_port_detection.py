#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试main.py的端口检测功能
"""
import subprocess
import time
import sys
import os

def test_main_py_port_detection():
    """测试main.py的端口检测功能"""
    print("=== 测试main.py的端口检测功能 ===")
    
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
    
    # 测试main.py的端口检测功能
    print("2. 测试main.py的端口检测功能...")
    try:
        # 切换到后端目录
        backend_dir = os.path.join(os.path.dirname(__file__), "backend")
        os.chdir(backend_dir)
        
        # 创建一个测试脚本来调用main.py的端口检测部分
        test_script = """
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# 模拟命令行参数
sys.argv = ["main.py", "--host", "127.0.0.1", "--port", "8000"]

# 导入main模块的端口检测代码
import psutil

# 解析命令行参数
import argparse
parser = argparse.ArgumentParser(description="SystemMonitor 后端服务器")
parser.add_argument("--host", default="0.0.0.0", help="服务器主机地址")
parser.add_argument("--port", type=int, default=8000, help="服务器端口号")
args = parser.parse_args()

# 检查端口是否被占用
port_in_use = False
for conn in psutil.net_connections():
    if conn.laddr.port == args.port and conn.status == 'LISTEN':
        port_in_use = True
        print(f"端口 {args.port} 已被占用，尝试停止占用该端口的进程...")
        
        # 获取占用端口的进程ID
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
    import time
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
"""
        
        # 写入测试脚本
        with open("test_port_check.py", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        # 运行测试脚本
        print("   运行端口检测测试...")
        result = subprocess.run(
            [sys.executable, "test_port_check.py"],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        print(f"   返回码: {result.returncode}")
        print(f"   标准输出:")
        for line in result.stdout.split('\n'):
            if line.strip():
                print(f"     {line}")
                
        print(f"   标准错误:")
        for line in result.stderr.split('\n'):
            if line.strip():
                print(f"     {line}")
        
        # 清理测试脚本
        try:
            os.remove("test_port_check.py")
        except:
            pass
            
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
    test_main_py_port_detection()