import sys
import os
import subprocess

def get_backend_dir():
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
        print(f"backend目录路径: {backend_dir}")  # 调试信息
        print(f"backend目录是否存在: {os.path.exists(backend_dir)}")  # 调试信息
        return backend_dir

def start_backend_server():
    """启动后端服务器"""
    try:
        backend_dir = get_backend_dir()
        main_py = os.path.join(backend_dir, "main.py")
        
        if not os.path.exists(main_py):
            print(f"错误: 找不到main.py文件: {main_py}")
            return False
        
        print(f"正在启动后端服务器: {main_py}")
        
        # 使用subprocess启动后端服务器
        process = subprocess.Popen(
            [sys.executable, main_py, "--port", "8000"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"后端服务器已启动，进程ID: {process.pid}")
        
        # 等待一段时间让服务器启动
        import time
        time.sleep(3)
        
        # 检查进程是否仍在运行
        if process.poll() is None:
            print("后端服务器运行正常")
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"后端服务器启动失败:")
            print(f"stdout: {stdout}")
            print(f"stderr: {stderr}")
            return False
            
    except Exception as e:
        print(f"启动后端服务器时出错: {e}")
        return False

if __name__ == "__main__":
    print("测试后端服务器启动...")
    if start_backend_server():
        print("✓ 后端服务器启动成功")
        print("可以通过 http://localhost:8000 访问系统监控")
    else:
        print("✗ 后端服务器启动失败")
    
    input("按Enter键退出...")