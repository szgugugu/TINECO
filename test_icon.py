import tkinter as tk
import sys
import os

def resource_path(relative_path):
    """ 获取资源的绝对路径，无论是开发环境还是打包后的环境 """
    try:
        # PyInstaller创建的临时文件夹
        base_path = sys._MEIPASS
    except Exception:
        # 正常的Python环境
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# 创建测试窗口
root = tk.Tk()
root.title("图标测试")

# 尝试设置图标
icon_path = resource_path("icon.ico")
if os.path.exists(icon_path):
    try:
        root.iconbitmap(icon_path)
        print(f"图标加载成功: {icon_path}")
    except Exception as e:
        print(f"无法加载图标: {e}")
else:
    print(f"图标文件不存在: {icon_path}")

# 显示信息
label = tk.Label(root, text=f"图标路径: {icon_path}\n图标存在: {os.path.exists(icon_path)}")
label.pack(padx=20, pady=20)

root.mainloop()