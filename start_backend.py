"""
SystemMonitor 后端服务器启动脚本
"""

import os
import sys
import subprocess

def start_backend():
    """启动后端服务器"""
    # 获取backend目录路径
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
    
    # 检查backend目录是否存在
    if not os.path.exists(backend_dir):
        print(f"错误: 找不到backend目录: {backend_dir}")
        return False
    
    # 检查是否安装了所需的依赖
    requirements_file = os.path.join(backend_dir, 'requirements.txt')
    if os.path.exists(requirements_file):
        print("正在检查并安装后端依赖...")
        try:
            # 使用当前Python环境安装依赖
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", requirements_file
            ])
            print("依赖安装完成")
        except subprocess.CalledProcessError as e:
            print(f"安装依赖失败: {e}")
            return False
    
    # 切换到backend目录
    original_dir = os.getcwd()
    os.chdir(backend_dir)
    
    try:
        # 启动后端服务器
        print("正在启动后端服务器...")
        print("服务器地址: http://localhost:8000")
        print("监控面板: http://localhost:8000")
        print("配置管理: http://localhost:8000/config")
        print("按 Ctrl+C 停止服务器")
        
        # 使用uvicorn启动FastAPI应用
        subprocess.call([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
        
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动服务器时发生错误: {e}")
    finally:
        # 恢复原始工作目录
        os.chdir(original_dir)
    
    return True

if __name__ == "__main__":
    start_backend()