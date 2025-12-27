import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import time
import json
import os
import sys
from ctypes import windll
import requests

class BackendLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("SystemMonitor 服务端")
        self.root.geometry("345x350")
        self.root.resizable(False, False)
        
        # 获取屏幕DPI和缩放比例
        try:
            user32 = windll.user32
            gdi32 = windll.gdi32
            hdc = user32.GetDC(0)
            dpi_x = gdi32.GetDeviceCaps(hdc, 88)
            user32.ReleaseDC(0, hdc)
            scale_factor = dpi_x / 96.0
        except:
            scale_factor = 1.0
        
        # 设置窗口图标
        try:
            if os.path.exists("icon.ico"):
                self.root.iconbitmap("icon.ico")
        except:
            pass
        
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
        
        # 创建UI
        self.create_ui()
        
        # 检查服务器状态
        self.check_server_status()
        
        # 设置窗口关闭协议
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="SystemMonitor 服务端", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 服务器配置框架
        config_frame = ttk.LabelFrame(main_frame, text="服务器配置", padding="10")
        config_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        config_frame.columnconfigure(1, weight=1)
        
        # 主机地址
        ttk.Label(config_frame, text="主机地址:").grid(row=0, column=0, sticky="w", pady=5)
        self.host_var = tk.StringVar(value=self.config.get("host", self.default_config["host"]))
        self.host_entry = ttk.Entry(config_frame, textvariable=self.host_var, width=30)
        self.host_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # 端口号
        ttk.Label(config_frame, text="端口号:").grid(row=1, column=0, sticky="w", pady=5)
        self.port_var = tk.StringVar(value=self.config.get("port", self.default_config["port"]))
        self.port_entry = ttk.Entry(config_frame, textvariable=self.port_var, width=30)
        self.port_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # 控制按钮框架
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        
        # 启动/停止按钮
        self.start_button = ttk.Button(control_frame, text="启动服务", command=self.toggle_server)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 保存配置按钮
        save_button = ttk.Button(control_frame, text="保存配置", command=self.save_config)
        save_button.pack(side=tk.LEFT)
        
        # 状态框架
        status_frame = ttk.LabelFrame(main_frame, text="服务状态", padding="10")
        status_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        status_frame.columnconfigure(0, weight=1)
        
        # 状态标签
        self.status_label = ttk.Label(status_frame, text="未运行", font=("Arial", 12))
        self.status_label.grid(row=0, column=0, sticky="w")
        
        # 状态指示器
        self.status_indicator = tk.Canvas(status_frame, width=20, height=20)
        self.status_indicator.grid(row=0, column=1, sticky="e")
        self.update_status_indicator(False)
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return self.default_config.copy()
        else:
            return self.default_config.copy()
    
    def save_config(self):
        """保存配置文件"""
        try:
            config = {
                "host": self.host_var.get(),
                "port": self.port_var.get()
            }
            
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            
            self.config = config
            messagebox.showinfo("成功", "配置已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {str(e)}")
    
    def update_status_indicator(self, is_running):
        """更新状态指示器"""
        self.status_indicator.delete("all")
        color = "green" if is_running else "red"
        self.status_indicator.create_oval(5, 5, 15, 15, fill=color, outline="")
    
    def check_server_status(self):
        """检查服务器状态"""
        try:
            port = self.port_var.get()
            response = requests.get(f"http://127.0.0.1:{port}/api/clients", timeout=2)
            if response.status_code == 200:
                self.is_server_running = True
                self.status_label.config(text="运行中")
                self.start_button.config(text="停止服务")
            else:
                self.is_server_running = False
                self.status_label.config(text="未运行")
                self.start_button.config(text="启动服务")
        except:
            self.is_server_running = False
            self.status_label.config(text="未运行")
            self.start_button.config(text="启动服务")
        
        self.update_status_indicator(self.is_server_running)
    
    def toggle_server(self):
        """切换服务器状态"""
        if self.is_server_running:
            self.stop_server()
        else:
            self.start_server()
    
    def get_backend_dir(self):
        """获取后端目录路径"""
        # 如果是打包后的exe，backend目录应该与exe在同一目录
        if getattr(sys, 'frozen', False):
            # 打包后的exe，backend目录与exe在同一目录
            exe_dir = os.path.dirname(sys.executable)
            print(f"打包环境，exe所在目录: {exe_dir}")  # 调试信息
            backend_dir = os.path.join(exe_dir, "backend")
            print(f"backend目录路径: {backend_dir}")  # 调试信息
            print(f"backend目录是否存在: {os.path.exists(backend_dir)}")  # 调试信息
            return backend_dir
        else:
            # 开发环境
            base_dir = os.path.dirname(os.path.abspath(__file__))
            print(f"开发环境，当前目录: {base_dir}")  # 调试信息
        
        backend_dir = os.path.join(base_dir, "backend")
        print(f"最终backend目录: {backend_dir}")  # 调试信息
        return backend_dir
    
    def start_server(self):
        """启动服务器"""
        try:
            # 检查端口是否被占用
            port = self.port_var.get()
            if self.is_port_in_use(port):
                messagebox.showerror("错误", f"端口 {port} 已被占用")
                return False
            
            # 获取后端目录
            backend_dir = self.get_backend_dir()
            print(f"后端目录: {backend_dir}")  # 调试信息
            
            if not os.path.exists(backend_dir):
                messagebox.showerror("错误", f"找不到后端目录: {backend_dir}\n请确保backend目录与BackendLauncher.exe在同一目录下")
                return False
            
            # 检查main.py是否存在
            main_py = os.path.join(backend_dir, "main.py")
            print(f"main.py路径: {main_py}")  # 调试信息
            print(f"main.py是否存在: {os.path.exists(main_py)}")  # 调试信息
            
            if not os.path.exists(main_py):
                messagebox.showerror("错误", f"找不到main.py文件: {main_py}")
                return False
            
            # 检查其他关键文件
            critical_files = ["main.py", "requirements.txt", "templates"]
            missing_files = []
            
            for item in critical_files:
                item_path = os.path.join(backend_dir, item)
                if not os.path.exists(item_path):
                    missing_files.append(item)
            
            if missing_files:
                error_msg = f"以下关键文件或目录缺失:\n" + "\n".join(missing_files)
                error_msg += f"\n\n请确保backend目录完整，包含所有必要的文件和子目录"
                messagebox.showerror("错误", error_msg)
                return False
            
            # 构建启动命令
            # 在打包环境中，需要使用打包的Python解释器
            if getattr(sys, 'frozen', False):
                # 打包后的环境，首先尝试使用打包的Python解释器
                python_exe = os.path.join(sys._MEIPASS, 'python.exe')
                if not os.path.exists(python_exe):
                    # 如果找不到python.exe，尝试其他可能的名称
                    python_exe = os.path.join(sys._MEIPASS, 'python3.exe')
                    if not os.path.exists(python_exe):
                        # 如果还是找不到，尝试使用虚拟环境的Python解释器
                        # 尝试多个可能的虚拟环境位置
                        exe_dir = os.path.dirname(sys.executable)
                        possible_venv_paths = [
                            os.path.join(exe_dir, '.venv', 'Scripts', 'python.exe'),
                            os.path.join(exe_dir, 'venv', 'Scripts', 'python.exe'),
                            os.path.join(exe_dir, 'env', 'Scripts', 'python.exe'),
                            os.path.join(os.path.dirname(exe_dir), '.venv', 'Scripts', 'python.exe'),
                            os.path.join(os.path.dirname(exe_dir), 'venv', 'Scripts', 'python.exe'),
                            os.path.join(os.path.dirname(exe_dir), 'env', 'Scripts', 'python.exe'),
                        ]
                        
                        # 尝试每个可能的虚拟环境路径
                        venv_found = False
                        for venv_python in possible_venv_paths:
                            if os.path.exists(venv_python):
                                python_exe = venv_python
                                venv_found = True
                                break
                        
                        if not venv_found:
                            # 尝试使用系统Python
                            python_exe = 'python'
                            # 验证系统Python是否可用
                            try:
                                subprocess.run([python_exe, '--version'], 
                                             stdout=subprocess.PIPE, 
                                             stderr=subprocess.PIPE, 
                                             check=True)
                            except (subprocess.CalledProcessError, FileNotFoundError):
                                # 系统Python不可用，尝试更多可能的路径
                                possible_python_paths = [
                                    r'C:\Python311\python.exe',
                                    r'C:\Python310\python.exe',
                                    r'C:\Python39\python.exe',
                                    r'C:\Python38\python.exe',
                                    r'C:\Program Files\Python311\python.exe',
                                    r'C:\Program Files\Python310\python.exe',
                                    r'C:\Program Files\Python39\python.exe',
                                    r'C:\Program Files\Python38\python.exe',
                                    r'C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe',
                                    r'C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe',
                                    r'C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe',
                                ]
                                
                                # 展开用户名环境变量
                                expanded_paths = []
                                for path in possible_python_paths:
                                    if '%USERNAME%' in path:
                                        expanded_path = path.replace('%USERNAME%', os.environ.get('USERNAME', ''))
                                        expanded_paths.append(expanded_path)
                                    else:
                                        expanded_paths.append(path)
                                
                                # 尝试每个可能的Python路径
                                python_found = False
                                for path in expanded_paths:
                                    if os.path.exists(path):
                                        try:
                                            subprocess.run([path, '--version'], 
                                                         stdout=subprocess.PIPE, 
                                                         stderr=subprocess.PIPE, 
                                                         check=True)
                                            python_exe = path
                                            python_found = True
                                            break
                                        except subprocess.CalledProcessError:
                                            continue
                                
                                if not python_found:
                                    messagebox.showerror("错误", "找不到可用的Python解释器。\n请确保已安装Python并添加到系统PATH，或者重新安装应用程序。")
                                    return False
            else:
                # 开发环境，使用当前Python解释器
                python_exe = sys.executable
            print(f"使用的Python解释器: {python_exe}")  # 调试信息
            
            # 直接运行main.py而不是使用uvicorn模块
            cmd = [
                python_exe, "main.py",
                "--host", self.host_var.get(),
                "--port", self.port_var.get()
            ]
            print(f"启动命令: {' '.join(cmd)}")  # 调试信息
            print(f"工作目录: {backend_dir}")  # 调试信息
            
            # 启动服务器进程
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            # Windows特定的创建标志
            creationflags = 0
            if os.name == 'nt':
                creationflags = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
            
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
                    # 检查进程是否还存在
                    if self.server_process is None:
                        print("服务器进程为None，停止读取输出")
                        return
                    
                    # 读取标准输出
                    if self.server_process.stdout:
                        for line in iter(self.server_process.stdout.readline, ''):
                            if line:
                                self.server_output.append(line.strip())
                                print(f"服务器输出: {line.strip()}")  # 调试信息
                                if getattr(sys, 'frozen', False):
                                    # 在打包环境中，立即刷新输出
                                    sys.stdout.flush()
                    
                    # 读取错误输出
                    if self.server_process and self.server_process.stderr:
                        for line in iter(self.server_process.stderr.readline, ''):
                            if line:
                                self.server_errors.append(line.strip())
                                print(f"服务器错误: {line.strip()}")  # 调试信息
                                if getattr(sys, 'frozen', False):
                                    # 在打包环境中，立即刷新输出
                                    sys.stdout.flush()
                except Exception as e:
                    print(f"读取进程输出异常: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    if getattr(sys, 'frozen', False):
                        # 在打包环境中，立即刷新输出
                        sys.stdout.flush()
            
            output_thread = threading.Thread(target=read_output, daemon=True)
            output_thread.start()
            
            # 在控制台版本中，打印启动命令
            if getattr(sys, 'frozen', False):
                print(f"启动命令: {' '.join(cmd)}")
                print(f"工作目录: {backend_dir}")
                sys.stdout.flush()
            
            # 等待服务器启动
            self.root.after(3000, self.check_server_started)  # 增加等待时间
            
            # 更新UI
            self.status_label.config(text="启动中...")
            self.start_button.config(text="启动中...", state="disabled")
            
            # 显式返回True表示启动命令已成功发送
            print("服务器启动命令已成功发送")
            return True
            
        except Exception as e:
            print(f"启动服务器异常: {str(e)}")  # 调试信息
            messagebox.showerror("错误", f"启动服务器失败: {str(e)}")
            return False
    
    def stop_server(self):
        """停止服务器"""
        try:
            if self.server_process:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                self.server_process = None
            
            self.is_server_running = False
            self.status_label.config(text="未运行")
            self.start_button.config(text="启动服务", state="normal")
            self.update_status_indicator(False)
            return True
            
        except Exception as e:
            messagebox.showerror("错误", f"停止服务器失败: {str(e)}")
            return False
    
    def check_server_started(self):
        """检查服务器是否启动成功"""
        try:
            port = self.port_var.get()
            print(f"检查服务器状态，端口: {port}")  # 调试信息
            
            # 检查进程是否还在运行
            if self.server_process and self.server_process.poll() is not None:
                # 进程已退出
                exit_code = self.server_process.returncode
                print(f"服务器进程已退出，退出码: {exit_code}")
                
                # 收集所有错误信息
                error_details = []
                
                # 检查是否有错误输出
                if hasattr(self, 'server_errors') and self.server_errors:
                    error_details.append("错误输出:")
                    error_details.extend(self.server_errors)
                
                # 检查是否有标准输出
                if hasattr(self, 'server_output') and self.server_output:
                    if error_details:
                        error_details.append("\n标准输出:")
                    else:
                        error_details.append("标准输出:")
                    error_details.extend(self.server_output)
                
                # 尝试从错误输出中提取文件找不到的具体信息
                missing_file = None
                if hasattr(self, 'server_errors') and self.server_errors:
                    for error_line in self.server_errors:
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
                    error_msg = f"找不到指定文件: {missing_file}\n\n请检查以下文件是否存在:\n1. {missing_file}\n2. 确保backend目录与BackendLauncher.exe在同一目录下\n3. 检查Python环境和相关依赖是否正确安装"
                
                if error_details:
                    error_msg += "\n\n详细信息:\n" + "\n".join(error_details[-20:])  # 显示最后20行
                
                self.is_server_running = False
                self.status_label.config(text="启动失败")
                self.start_button.config(text="启动服务", state="normal")
                self.update_status_indicator(False)
                messagebox.showerror("错误", error_msg)
                return
            
            response = requests.get(f"http://127.0.0.1:{port}/api/clients", timeout=2)
            print(f"服务器响应状态码: {response.status_code}")  # 调试信息
            
            if response.status_code == 200:
                self.is_server_running = True
                self.status_label.config(text="运行中")
                self.start_button.config(text="停止服务", state="normal")
                self.update_status_indicator(True)
            else:
                self.is_server_running = False
                self.status_label.config(text="启动失败")
                self.start_button.config(text="启动服务", state="normal")
                self.update_status_indicator(False)
                messagebox.showerror("错误", "服务器启动失败")
        except Exception as e:
            print(f"检查服务器状态异常: {str(e)}")  # 调试信息
            
            # 尝试获取进程输出
            error_msg = f"服务器启动失败: {str(e)}"
            if hasattr(self, 'server_errors') and self.server_errors:
                error_msg += "\n\n错误信息:\n" + "\n".join(self.server_errors[-10:])
            
            if hasattr(self, 'server_output') and self.server_output:
                error_msg += "\n\n输出信息:\n" + "\n".join(self.server_output[-10:])
            
            self.is_server_running = False
            self.status_label.config(text="启动失败")
            self.start_button.config(text="启动服务", state="normal")
            self.update_status_indicator(False)
            messagebox.showerror("错误", error_msg)
    
    def is_port_in_use(self, port):
        """检查端口是否被占用"""
        try:
            # 方法1: 使用socket连接测试
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', int(port)))
            s.close()
            socket_in_use = result == 0
            
            # 方法2: 使用netstat检查是否有进程在监听该端口
            if os.name == 'nt':  # Windows
                import subprocess
                try:
                    output = subprocess.check_output(f'netstat -ano | findstr ":{port}" | findstr "LISTENING"', 
                                                  shell=True, text=True)
                    netstat_in_use = len(output.strip()) > 0
                    
                    # 只有当netstat显示有进程在监听时，才认为端口被占用
                    return netstat_in_use
                except subprocess.CalledProcessError:
                    # 如果netstat命令执行失败，假设端口未被占用
                    return False
            else:
                # 非Windows系统，使用socket测试结果
                return socket_in_use
        except:
            return False
    
    def on_closing(self):
        """窗口关闭事件"""
        if self.is_server_running:
            if messagebox.askokcancel("退出", "服务器正在运行，确定要退出吗？"):
                self.stop_server()
                self.root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    print("后端启动器启动中...")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python路径: {sys.executable}")
    print(f"是否为打包环境: {getattr(sys, 'frozen', False)}")
    
    if getattr(sys, 'frozen', False):
        print(f"临时目录: {getattr(sys, '_MEIPASS', 'None')}")
        print(f"可执行文件路径: {sys.executable}")
    
    root = tk.Tk()
    app = BackendLauncher(root)
    root.mainloop()