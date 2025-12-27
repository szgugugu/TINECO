#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试main.py的端口检测功能
"""
import subprocess
import time
import sys
import os

def test_simple_main_port():
    """简单测试main.py的端口检测功能"""
    print("=== 简单测试main.py的端口检测功能 ===")
    
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
        
        # 创建一个简单的测试脚本来调用main.py
        test_script = """
import subprocess
import sys
import time

# 直接运行main.py并捕获输出
print("正在运行main.py...")
process = subprocess.Popen(
    [sys.executable, "main.py", "--host", "127.0.0.1", "--port", "8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

# 实时读取输出
output_lines = []
start_time = time.time()
timeout = 10  # 10秒超时

while time.time() - start_time < timeout:
    if process.poll() is not None:
        break
        
    # 读取一行输出
    try:
        line = process.stdout.readline()
        if line:
            line = line.strip()
            output_lines.append(line)
            print(f"  输出: {line}")
            
            # 如果看到服务器启动信息，说明端口检测没有工作
            if "Uvicorn running on" in line:
                print("  服务器已启动，端口检测可能未工作")
                break
    except:
        pass
        
    time.sleep(0.1)

# 终止进程
if process.poll() is None:
    process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=2)

# 检查输出
port_detected = any("端口 8000 已被占用" in line for line in output_lines)
process_stopped = any("成功停止进程" in line or "强制终止进程" in line for line in output_lines)

if port_detected:
    print("✓ 成功检测到端口占用")
else:
    print("✗ 未检测到端口占用")
    
if process_stopped:
    print("✓ 成功停止占用端口的进程")
else:
    print("✗ 未停止占用端口的进程")
"""
        
        # 写入测试脚本
        with open("test_simple_main.py", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        # 运行测试脚本
        print("   运行简单测试...")
        result = subprocess.run(
            [sys.executable, "test_simple_main.py"],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        print(f"   返回码: {result.returncode}")
        print(f"   输出:")
        for line in result.stdout.split('\n'):
            if line.strip():
                print(f"     {line}")
                
        if result.stderr:
            print(f"   错误:")
            for line in result.stderr.split('\n'):
                if line.strip():
                    print(f"     {line}")
        
        # 清理测试脚本
        try:
            os.remove("test_simple_main.py")
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
    test_simple_main_port()