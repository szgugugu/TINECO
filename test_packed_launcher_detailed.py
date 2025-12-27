import tkinter as tk
import sys
import os

# 模拟打包环境
sys.frozen = True
sys.executable = r"c:\Users\zhifeng.gu.TINECO\Documents\trae_projects\download_web\system-monitor\release\SystemMonitorLauncher.exe"
sys._MEIPASS = r"c:\Users\zhifeng.gu.TINECO\Documents\trae_projects\download_web\system-monitor\release"

from backend_launcher import BackendLauncher

# 创建测试窗口
root = tk.Tk()
root.title("测试修复后的打包启动器")
root.geometry("400x300")

# 创建文本框显示详细信息
text_frame = tk.Frame(root)
text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

text = tk.Text(text_frame, height=15, width=50)
text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(text_frame, command=text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text.config(yscrollcommand=scrollbar.set)

# 创建启动器实例
launcher = BackendLauncher(root)

# 添加测试按钮
def test_start_server():
    text.insert(tk.END, "开始测试服务器启动...\n")
    text.see(tk.END)
    root.update()
    
    result = launcher.start_server()
    text.insert(tk.END, f"启动服务器结果: {result}\n")
    text.see(tk.END)
    root.update()
    
    if result:
        text.insert(tk.END, "服务器启动成功！\n")
        text.see(tk.END)
        root.update()
        
        # 检查服务器状态
        import time
        text.insert(tk.END, "等待服务器完全启动...\n")
        text.see(tk.END)
        root.update()
        time.sleep(3)
        
        launcher.check_server_status()
        text.insert(tk.END, f"服务器运行状态: {launcher.is_server_running}\n")
        text.see(tk.END)
        root.update()
        
        if launcher.is_server_running:
            text.insert(tk.END, "服务器运行正常！\n")
            text.see(tk.END)
            root.update()
        else:
            text.insert(tk.END, "服务器启动后状态异常\n")
            text.see(tk.END)
            root.update()
    else:
        text.insert(tk.END, "服务器启动失败！\n")
        text.see(tk.END)
        root.update()

test_button = tk.Button(root, text="测试启动服务器", command=test_start_server)
test_button.pack(pady=10)

# 添加关闭按钮
def close_all():
    if launcher.is_server_running:
        text.insert(tk.END, "正在停止服务器...\n")
        text.see(tk.END)
        root.update()
        launcher.stop_server()
        text.insert(tk.END, "服务器已停止\n")
        text.see(tk.END)
        root.update()
    root.quit()

close_button = tk.Button(root, text="关闭", command=close_all)
close_button.pack(pady=10)

# 5秒后自动测试启动服务器
root.after(5000, test_start_server)

# 20秒后自动关闭
root.after(20000, close_all)

text.insert(tk.END, "测试修复后的打包启动器...\n")
text.insert(tk.END, "5秒后将自动测试启动服务器\n")
text.see(tk.END)
root.mainloop()
text.insert(tk.END, "测试完成\n")
print('测试完成')