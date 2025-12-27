import tkinter as tk
import sys
import os
from backend_launcher import BackendLauncher

root = tk.Tk()
launcher = BackendLauncher(root)
root.after(2000, lambda: launcher.start_server())
root.after(10000, lambda: root.quit())
print('测试最终版本...')
root.mainloop()
print('测试完成')