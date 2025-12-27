#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试Tkinter在打包环境中是否正常工作
"""
import tkinter as tk
import sys

def test_tkinter():
    """测试Tkinter"""
    print("测试Tkinter...")
    print(f"当前工作目录: {sys.executable}")
    print(f"是否为打包环境: {getattr(sys, 'frozen', False)}")
    
    try:
        # 创建一个简单的窗口
        root = tk.Tk()
        root.title("Tkinter测试")
        root.geometry("300x200")
        
        # 添加一个标签
        label = tk.Label(root, text="如果你看到这个窗口，说明Tkinter工作正常")
        label.pack(pady=20)
        
        # 添加一个按钮
        def on_click():
            print("按钮被点击了")
            label.config(text="按钮被点击了！")
        
        button = tk.Button(root, text="点击我", command=on_click)
        button.pack(pady=10)
        
        # 添加一个退出按钮
        exit_button = tk.Button(root, text="退出", command=root.quit)
        exit_button.pack(pady=10)
        
        print("Tkinter窗口已创建，启动主循环...")
        root.mainloop()
        print("Tkinter测试完成")
        return True
    except Exception as e:
        print(f"Tkinter测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_tkinter()