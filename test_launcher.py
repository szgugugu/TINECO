import os
import sys
import time
import subprocess
import requests
from threading import Thread

def test_backend_launcher():
    """测试后端启动器是否能正常启动服务器"""
    print("测试后端启动器...")
    
    # 启动后端启动器
    launcher_exe = os.path.join(os.getcwd(), "BackendLauncher.exe")
    print(f"启动器路径: {launcher_exe}")
    
    # 使用subprocess启动GUI应用
    process = subprocess.Popen([launcher_exe])
    
    # 等待应用启动
    time.sleep(3)
    
    # 尝试连接默认端口
    try:
        response = requests.get("http://127.0.0.1:8000/api/clients", timeout=5)
        if response.status_code == 200:
            print("✓ 服务器启动成功！")
            print(f"响应内容: {response.text[:100]}...")
            return True
        else:
            print(f"✗ 服务器响应错误，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 无法连接到服务器: {str(e)}")
        return False
    finally:
        # 关闭启动器
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            pass

if __name__ == "__main__":
    test_backend_launcher()