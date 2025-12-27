import os
import sys
import subprocess

def main():
    print("测试服务器启动...")
    print(f"当前工作目录: {os.getcwd()}")
    
    # 获取backend目录
    # 如果是打包后的exe，使用sys._MEIPASS获取临时目录
    if getattr(sys, 'frozen', False):
        # 打包后的exe，backend目录在临时目录中
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        print(f"打包环境，临时目录: {base_dir}")
        backend_dir = os.path.join(base_dir, "backend")
    else:
        # 开发环境
        backend_dir = os.path.join(os.getcwd(), "backend")
    
    print(f"Backend目录: {backend_dir}")
    print(f"Backend目录是否存在: {os.path.exists(backend_dir)}")
    
    if os.path.exists(backend_dir):
        # 检查main.py
        main_py = os.path.join(backend_dir, "main.py")
        print(f"main.py路径: {main_py}")
        print(f"main.py是否存在: {os.path.exists(main_py)}")
        
        if os.path.exists(main_py):
            # 构建启动命令
            cmd = ["python", "main.py", "--host", "127.0.0.1", "--port", "8000"]
            print(f"启动命令: {' '.join(cmd)}")
            
            # 启动服务器进程
            try:
                process = subprocess.Popen(
                    cmd,
                    cwd=backend_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # 读取输出
                stdout, stderr = process.communicate(timeout=10)
                
                print(f"退出码: {process.returncode}")
                print(f"标准输出:\n{stdout}")
                print(f"错误输出:\n{stderr}")
                
            except subprocess.TimeoutExpired:
                print("服务器启动超时，但这可能是正常的（服务器在后台运行）")
                process.terminate()
            except Exception as e:
                print(f"启动服务器异常: {str(e)}")
    else:
        print("Backend目录不存在，无法启动服务器")

if __name__ == "__main__":
    main()