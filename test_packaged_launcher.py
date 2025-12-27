import os
import sys
import time
import requests
import subprocess
import threading

def test_packaged_launcher():
    """测试打包后的启动器"""
    print("=== 测试打包后的启动器 ===")
    
    release_dir = os.path.join(os.path.dirname(__file__), 'release')
    launcher_exe = os.path.join(release_dir, 'SystemMonitorLauncher.exe')
    
    if not os.path.exists(launcher_exe):
        print(f"✗ 找不到启动器: {launcher_exe}")
        return False
    
    print(f"✓ 找到启动器: {launcher_exe}")
    
    # 启动打包后的exe
    print("\n1. 启动打包后的exe...")
    process = subprocess.Popen([launcher_exe], cwd=release_dir)
    
    # 等待一段时间让GUI启动
    print("等待GUI启动...")
    time.sleep(5)
    
    # 检查进程是否还在运行
    if process.poll() is None:
        print("✓ 打包后的exe正在运行")
    else:
        print(f"✗ 打包后的exe已退出，退出码: {process.poll()}")
        return False
    
    # 等待更多时间让用户手动测试
    print("\n2. 请手动测试GUI功能:")
    print("   - 点击'启动服务'按钮")
    print("   - 检查服务器是否正常启动")
    print("   - 点击'打开网页'按钮")
    print("   - 点击'停止服务'按钮")
    print("   - 关闭窗口")
    print("\n按回车键继续...")
    input()
    
    # 检查进程是否已退出
    if process.poll() is not None:
        print("✓ 打包后的exe已正常退出")
        return True
    else:
        print("⚠ 打包后的exe仍在运行，尝试终止...")
        process.terminate()
        try:
            process.wait(timeout=5)
            print("✓ 打包后的exe已终止")
            return True
        except:
            print("✗ 无法终止打包后的exe")
            return False

if __name__ == "__main__":
    success = test_packaged_launcher()
    if success:
        print("\n✓ 打包后的启动器测试通过！")
    else:
        print("\n✗ 打包后的启动器测试失败！")
    
    input("\n按回车键退出...")