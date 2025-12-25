import tkinter as tk
from tkinter import ttk
import psutil
import socket

# 创建测试窗口
root = tk.Tk()
root.title("网络适配器测试")
root.geometry("600x300")

# 创建框架
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# 创建标签
tk.Label(frame, text="网络适配器信息", font=("微软雅黑", 12, "bold")).pack(pady=5)

# 创建树形视图
adapter_tree = ttk.Treeview(frame, columns=("适配器名称", "IP地址", "MAC地址"), show="headings")
adapter_tree.heading("适配器名称", text="适配器名称")
adapter_tree.heading("IP地址", text="IP地址")
adapter_tree.heading("MAC地址", text="MAC地址")

adapter_tree.column("适配器名称", width=150)
adapter_tree.column("IP地址", width=150)
adapter_tree.column("MAC地址", width=200)

adapter_tree.pack(fill=tk.BOTH, expand=True)

def update_adapter_info():
    """更新网络适配器信息"""
    # 清除现有数据
    for item in adapter_tree.get_children():
        adapter_tree.delete(item)
    
    # 获取网络接口信息
    addrs = psutil.net_if_addrs()
    
    for interface_name, interface_addresses in addrs.items():
        ipv4 = ""
        mac = ""
        
        for address in interface_addresses:
            if address.family == socket.AF_INET:
                ipv4 = address.address
            elif address.family == psutil.AF_LINK:
                mac = address.address
        
        # 显示所有网络适配器，即使没有IP地址
        if mac:  # 只要MAC地址存在就显示
            if not ipv4:  # 如果没有IP地址，显示为"未连接"
                ipv4 = "未连接"
            adapter_tree.insert("", "end", values=(interface_name, ipv4, mac))
    
    # 如果没有适配器信息，添加一条提示信息
    if not adapter_tree.get_children():
        adapter_tree.insert("", "end", values=("未找到网络适配器", "", ""))
    
    # 每5秒更新一次
    root.after(5000, update_adapter_info)

# 初始更新
update_adapter_info()

# 添加按钮用于手动刷新
tk.Button(frame, text="刷新", command=update_adapter_info).pack(pady=5)

root.mainloop()