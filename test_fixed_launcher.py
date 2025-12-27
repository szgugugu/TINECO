import tkinter as tk
import sys
import os
from backend_launcher import BackendLauncher

# 创建测试窗口
root = tk.Tk()
root.title("测试修复后的启动器")
root.geometry("300x200")

# 创建启动器实例
launcher = BackendLauncher(root)

# 添加测试按钮
def test_start_server():
    print("开始测试服务器启动...")
    result = launcher.start_server()
    print(f"启动服务器结果: {result}")
    if result:
        print("服务器启动成功！")
        # 检查服务器状态
        import time
        time.sleep(3)  # 等待3秒让服务器完全启动
        launcher.check_server_status()
        print(f"服务器运行状态: {launcher.is_server_running}")
    else:
        print("服务器启动失败！")

test_button = tk.Button(root, text="测试启动服务器", command=test_start_server)
test_button.pack(pady=20)

# 添加关闭按钮
def close_all():
    if launcher.is_server_running:
        launcher.stop_server()
    root.quit()

close_button = tk.Button(root, text="关闭", command=close_all)
close_button.pack(pady=10)

# 5秒后自动测试启动服务器
root.after(5000, test_start_server)

# 20秒后自动关闭
root.after(20000, close_all)

print('测试修复后的启动器...')
root.mainloop()
print('测试完成')