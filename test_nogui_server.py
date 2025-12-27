#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
非GUI版本的后端启动器，用于测试
"""
import os
import sys
import subprocess
import time
import json
from ctypes import windll

class BackendServerManager:
    def __init__(self):
        # 配置文件路径
        self.config_file = "backend_config.json"
        
        # 服务器进程
        self.server_process = None
        self.is_server_running = False
        
        # 默认配置
        self.default_config = {
            "host": "0.0.0.0",
            "port": "8000"
        }
        
        # 加载配置
        self.config = self.load_config()
        
        # 主机和端口
        self.host = self.config.get("host", "0.0.0.0")
        self.port = self.config.get("port", "8000")
    
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.default_config.copy()
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return self.default_config.copy()
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def get_backend_dir(self):
        """获取后端目录路径"""
        if getattr(sys, 'frozen', False):
            # 打包后的exe环境
            base_dir = os.path.dirname(sys.executable)
            backend_dir = os.path.join(base_dir, "backend")
            print(f"打包环境，当前目录: {base_dir}")
        else:
            # 开发环境
            base_dir = os.path.dirname(os.path.abspath(__file__))
            backend_dir = os.path.join(base_dir, "backend")
            print(f"开发环境，当前目录: {base_dir}")
        
        print(f"最终backend目录: {backend_dir}")
        return backend_dir
    
    def check_port_available(self, port):
        """检查端口是否可用"""
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(('localhost', int(port)))
                return result != 0
        except:
            return False
    
    def kill_process_on_port(self, port):
        """终止占用指定端口的进程"""
        try:
            # Windows系统
            if os.name == 'nt':
                # 查找占用端口的进程
                result = subprocess.run(
                    f'netstat -ano | findstr :{port}',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if f':{port}' in line and 'LISTENING' in line:
                            parts = line.split()
                            if len(parts) >= 5:
                                pid = parts[-1]
                                try:
                                    subprocess.run(['taskkill', '/F', '/PID', pid], 
                                                 capture_output=True)
                                    print(f"已终止占用端口 {port} 的进程 (PID: {pid})")
                                    time.sleep(1)
                                    return True
                                except Exception as e:
                                    print(f"终止进程失败: {e}")
            return False
        except Exception as e:
            print(f"检查端口占用失败: {e}")
            return False
    
    def start_server(self):
        """启动服务器"""
        if self.is_server_running:
            print("服务器已在运行中")
            return False
        
        # 检查端口是否可用
        port = self.port
        if not self.check_port_available(port):
            print(f"端口 {port} 已被占用，尝试终止占用进程...")
            if not self.kill_process_on_port(port):
                print(f"端口 {port} 已被占用")
                return False
        
        # 获取后端目录
        backend_dir = self.get_backend_dir()
        print(f"后端目录: {backend_dir}")
        
        if not os.path.exists(backend_dir):
            print(f"找不到后端目录: {backend_dir}")
            return False
        
        # 检查main.py是否存在
        main_py = os.path.join(backend_dir, "main.py")
        print(f"main.py路径: {main_py}")
        print(f"main.py是否存在: {os.path.exists(main_py)}")
        
        if not os.path.exists(main_py):
            print(f"找不到main.py文件: {main_py}")
            return False
        
        # 构建启动命令
        python_exe = sys.executable
        print(f"使用的Python解释器: {python_exe}")
        
        cmd = [
            python_exe, "main.py",
            "--host", self.host,
            "--port", self.port
        ]
        
        print(f"启动命令: {' '.join(cmd)}")
        print(f"工作目录: {backend_dir}")
        
        # 启动服务器进程
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        # Windows特定的创建标志
        creationflags = 0
        if os.name == 'nt':
            creationflags = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
        
        try:
            self.server_process = subprocess.Popen(
                cmd,
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            
            # 启动一个线程来读取进程输出
            import threading
            self.server_output = []
            self.server_errors = []
            
            def read_output():
                try:
                    # 读取标准输出
                    for line in iter(self.server_process.stdout.readline, ''):
                        if line:
                            self.server_output.append(line.strip())
                            print(f"服务器输出: {line.strip()}")
                    
                    # 读取错误输出
                    for line in iter(self.server_process.stderr.readline, ''):
                        if line:
                            self.server_errors.append(line.strip())
                            print(f"服务器错误: {line.strip()}")
                except:
                    pass
            
            output_thread = threading.Thread(target=read_output)
            output_thread.daemon = True
            output_thread.start()
            
            # 等待一段时间检查进程是否启动成功
            time.sleep(3)
            
            if self.server_process.poll() is None:
                self.is_server_running = True
                print(f"服务器启动成功，地址: http://{self.host}:{self.port}")
                return True
            else:
                print("服务器启动失败")
                if self.server_errors:
                    print("错误信息:", "\n".join(self.server_errors))
                return False
                
        except Exception as e:
            print(f"启动服务器时发生错误: {e}")
            return False
    
    def stop_server(self):
        """停止服务器"""
        if not self.is_server_running or not self.server_process:
            print("服务器未运行")
            return False
        
        try:
            # 尝试优雅地终止进程
            self.server_process.terminate()
            
            # 等待进程结束
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # 如果进程没有在5秒内结束，强制终止
                self.server_process.kill()
                self.server_process.wait()
            
            self.is_server_running = False
            self.server_process = None
            print("服务器已停止")
            return True
            
        except Exception as e:
            print(f"停止服务器时发生错误: {e}")
            return False

def test_server_manager():
    """测试服务器管理器"""
    print("=== 测试非GUI版本的服务器管理器 ===")
    
    manager = BackendServerManager()
    
    # 测试启动服务器
    print("\n1. 启动服务器...")
    success = manager.start_server()
    if success:
        print("✓ 服务器启动成功")
    else:
        print("✗ 服务器启动失败")
        return False
    
    # 等待服务器完全启动
    print("\n2. 等待服务器完全启动...")
    time.sleep(10)
    
    # 测试服务器响应
    print("\n3. 测试服务器响应...")
    try:
        import requests
        # 使用localhost而不是0.0.0.0进行连接
        response = requests.get("http://localhost:8000", timeout=5)
        if response.status_code == 200:
            print("✓ 服务器响应正常")
        else:
            print(f"✗ 服务器响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 无法连接到服务器: {e}")
        return False
    
    # 测试停止服务器
    print("\n4. 停止服务器...")
    success = manager.stop_server()
    if success:
        print("✓ 服务器停止成功")
    else:
        print("✗ 服务器停止失败")
        return False
    
    return True

if __name__ == "__main__":
    success = test_server_manager()
    if success:
        print("\n=== 测试结果: 通过 ===")
        print("✓ 非GUI版本的服务器管理器测试成功！")
    else:
        print("\n=== 测试结果: 失败 ===")
        print("✗ 非GUI版本的服务器管理器测试失败！")