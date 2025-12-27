import sys
import os

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

if __name__ == "__main__":
    print("测试backend目录路径检测...")
    backend_dir = get_backend_dir()
    
    if os.path.exists(backend_dir):
        print(f"✓ backend目录存在: {backend_dir}")
        main_py = os.path.join(backend_dir, "main.py")
        if os.path.exists(main_py):
            print(f"✓ main.py存在: {main_py}")
        else:
            print(f"✗ main.py不存在: {main_py}")
    else:
        print(f"✗ backend目录不存在: {backend_dir}")
    
    input("按Enter键退出...")