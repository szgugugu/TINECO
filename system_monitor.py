import tkinter as tk
from tkinter import ttk
import psutil
import platform
import socket
import subprocess
import threading
import time
import os
import sys
import io
from collections import deque
from ctypes import windll
from PIL import Image, ImageGrab
import win32clipboard
import win32con

# 获取屏幕DPI和缩放比例
def get_screen_info():
    try:
        # 获取屏幕尺寸
        screen_width = windll.user32.GetSystemMetrics(0)
        screen_height = windll.user32.GetSystemMetrics(1)
        
        # 获取DPI
        user32 = windll.user32
        gdi32 = windll.gdi32
        hdc = user32.GetDC(0)
        dpi_x = gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
        dpi_y = gdi32.GetDeviceCaps(hdc, 90)  # LOGPIXELSY
        user32.ReleaseDC(0, hdc)
        
        # 计算缩放比例 (以96 DPI为标准)
        scale_factor = dpi_x / 96.0
        
        return {
            'screen_width': screen_width,
            'screen_height': screen_height,
            'dpi_x': dpi_x,
            'dpi_y': dpi_y,
            'scale_factor': scale_factor
        }
    except Exception as e:
        # 如果获取失败，返回默认值
        return {
            'screen_width': 1920,
            'screen_height': 1080,
            'dpi_x': 96,
            'dpi_y': 96,
            'scale_factor': 1.0
        }

# # 设置中文字体
# plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
# plt.rcParams['axes.unicode_minus'] = False

# # 设置matplotlib风格为浅色
# mpl.rcParams['figure.facecolor'] = '#ffffff'
# mpl.rcParams['axes.facecolor'] = '#f8f9fa'
# mpl.rcParams['axes.edgecolor'] = '#1e293b'
# mpl.rcParams['axes.labelcolor'] = '#1e293b'
# mpl.rcParams['text.color'] = '#1e293b'
# mpl.rcParams['xtick.color'] = '#1e293b'
# mpl.rcParams['ytick.color'] = '#1e293b'
# mpl.rcParams['grid.color'] = '#e2e8f0'
# mpl.rcParams['legend.facecolor'] = '#ffffff'
# mpl.rcParams['legend.edgecolor'] = '#cbd5e1'

# 定义企业级主题颜色
class ThemeColors:
    # 企业级浅色主题 - 专业蓝色系
    BG_PRIMARY = '#ffffff'           # 主背景色 - 纯白色
    BG_SECONDARY = '#f8fafc'         # 次背景色 - 浅灰白
    BG_TERTIARY = '#f1f5f9'          # 第三背景色 - 更浅的灰白
    FG_PRIMARY = '#1e293b'           # 主前景色 - 深蓝灰
    FG_SECONDARY = '#475569'         # 次前景色 - 中蓝灰
    ACCENT = '#3b82f6'               # 强调色 - 专业蓝
    CORPORATE_BLUE = '#2563eb'       # 企业蓝
    SUCCESS = '#10b981'              # 成功色 - 现代绿
    WARNING = '#f59e0b'              # 警告色 - 琥珀色
    ERROR = '#ef4444'                # 错误色 - 鲜红色
    BORDER = '#cbd5e1'               # 边框色 - 浅蓝灰
    PROGRESS_BG = '#e2e8f0'           # 进度条背景色 - 浅灰蓝
    PROGRESS_BAR = '#3b82f6'         # 进度条填充色 - 专业蓝
    HIGHLIGHT = '#f1f5f9'            # 高亮色 - 更浅的灰白
    
    # 图表颜色
    CHART_BG = '#ffffff'            # 图表背景
    CHART_GRID = '#e2e8f0'          # 图表网格
    CPU_CHART_COLOR = '#3b82f6'    # CPU图表颜色
    MEMORY_CHART_COLOR = '#10b981'  # 内存图表颜色
    
    # 企业级深色主题（备用）
    DARK_BG_PRIMARY = '#1e293b'      # 深色主背景
    DARK_BG_SECONDARY = '#334155'    # 深色次背景
    DARK_FG_PRIMARY = '#f8fafc'      # 深色主前景
    DARK_FG_SECONDARY = '#e2e8f0'    # 深色次前景
    DARK_ACCENT = '#3b82f6'          # 深色强调色
    
    # 企业级强调色
    CORPORATE_BLUE = '#1e40af'       # 企业蓝
    CORPORATE_DARK = '#0f172a'       # 深色强调
    
    # 主题切换标志
    DARK_THEME = False

class SystemMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("TINECO 运维检测工具 v1.6.0")
        
        # 版本号
        self.version = "v1.6.0"
        
        # 获取屏幕信息
        self.screen_info = get_screen_info()
        
        # 根据屏幕尺寸和缩放率计算窗口大小
        self.calculate_window_size()
        
        # 设置窗口图标
        def resource_path(relative_path):
            """ 获取资源的绝对路径，无论是开发环境还是打包后的环境 """
            try:
                # PyInstaller创建的临时文件夹
                base_path = sys._MEIPASS
            except Exception:
                # 正常的Python环境
                base_path = os.path.abspath(".")
            
            return os.path.join(base_path, relative_path)
        
        # 尝试设置图标
        icon_path = resource_path("icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception as e:
                print(f"无法加载图标: {e}")
        
        # 设置深色主题背景
        self.root.configure(bg=ThemeColors.BG_PRIMARY)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 自定义企业级样式
        self.style.configure("TFrame", background=ThemeColors.BG_PRIMARY)
        self.style.configure("TLabelframe", background=ThemeColors.BG_PRIMARY, foreground=ThemeColors.FG_PRIMARY, bordercolor=ThemeColors.BORDER)
        self.style.configure("TLabelframe.Label", background=ThemeColors.BG_PRIMARY, foreground=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", 11, "bold"))
        
        # 企业级按钮样式
        self.style.configure("TButton", 
                        background=ThemeColors.CORPORATE_BLUE, 
                        foreground=ThemeColors.FG_PRIMARY, 
                        bordercolor=ThemeColors.BORDER, 
                        focuscolor='none',
                        font=("微软雅黑", 9))
        self.style.map("TButton", 
                    background=[('active', ThemeColors.ACCENT), ('pressed', ThemeColors.CORPORATE_DARK)], 
                    foreground=[('active', ThemeColors.FG_PRIMARY)])
        
        # 企业级标签样式
        self.style.configure("TLabel", background=ThemeColors.BG_PRIMARY, foreground=ThemeColors.FG_PRIMARY, font=("微软雅黑", 9))
        
        # 企业级树形视图样式
        self.style.configure("Treeview", 
                        background=ThemeColors.BG_SECONDARY, 
                        foreground=ThemeColors.FG_PRIMARY, 
                        fieldbackground=ThemeColors.BG_SECONDARY, 
                        bordercolor=ThemeColors.BORDER,
                        rowheight=25)
        self.style.configure("Treeview.Heading", 
                        background=ThemeColors.CORPORATE_BLUE, 
                        foreground=ThemeColors.FG_PRIMARY, 
                        font=("微软雅黑", 9, "bold"))
        
        # 企业级进度条样式
        self.style.configure("Green.Horizontal.TProgressbar", 
                        troughcolor=ThemeColors.PROGRESS_BG,
                        background=ThemeColors.PROGRESS_BAR,
                        bordercolor=ThemeColors.BORDER,
                        lightcolor=ThemeColors.PROGRESS_BAR,
                        darkcolor=ThemeColors.PROGRESS_BAR,
                        thickness=12)
        
        # 网络测试状态
        self.baidu_ping_running = False
        self.tiktok_ping_running = False
        self.baidu_thread = None
        self.tiktok_thread = None
        
        # CPU和内存数据初始化
        self.cpu_data = deque(maxlen=30)
        self.memory_data = deque(maxlen=30)
        self.time_data = deque(maxlen=30)
        self.max_data_points = 60  # 最多显示60个数据点
        
        # 创建界面（移除图表创建以提高启动速度）
        self.create_widgets()
        
        # 关闭窗口时的处理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 绑定窗口大小变化事件
        self.root.bind('<Configure>', self.on_window_resize)
        
        # 进一步延迟初始化系统信息，加快界面显示速度
        self.root.after(200, self.update_system_info)
        
        # 进一步延迟启动性能监控，加快界面显示速度
        self.root.after(1000, self.update_performance_data)
        
        # 自动启动连通性测试
        self.root.after(1000, self.start_network_tests)
        
    def create_charts(self):
        """创建CPU和内存使用率图表"""
        # 获取缩放率
        scale = self.screen_info['scale_factor']
        
        # 创建图表容器
        self.chart_frame = tk.Frame(self.root, bg=ThemeColors.BG_PRIMARY)
        
        # 创建matplotlib图形
        # 根据缩放率调整图表大小
        chart_width = 6 * scale
        chart_height = 4 * scale
        dpi = 100
        
        # CPU使用率显示 - 使用进度条替代图表
        cpu_frame = tk.Frame(self.chart_frame, bg=ThemeColors.BG_PRIMARY)
        cpu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=int(5 * scale), pady=int(5 * scale))
        
        tk.Label(cpu_frame, text="CPU使用率", color=ThemeColors.FG_PRIMARY, 
                bg=ThemeColors.BG_PRIMARY, font=("Arial", int(10 * scale))).pack(pady=(0, 5))
        
        self.cpu_progress = ttk.Progressbar(cpu_frame, length=int(150 * scale), mode='determinate')
        self.cpu_progress.pack(pady=5)
        
        self.cpu_label = tk.Label(cpu_frame, text="0%", color=ThemeColors.FG_PRIMARY, 
                                 bg=ThemeColors.BG_PRIMARY, font=("Arial", int(9 * scale)))
        self.cpu_label.pack()
        
        # 内存使用率显示 - 使用进度条替代图表
        memory_frame = tk.Frame(self.chart_frame, bg=ThemeColors.BG_PRIMARY)
        memory_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=int(5 * scale), pady=int(5 * scale))
        
        tk.Label(memory_frame, text="内存使用率", color=ThemeColors.FG_PRIMARY, 
                bg=ThemeColors.BG_PRIMARY, font=("Arial", int(10 * scale))).pack(pady=(0, 5))
        
        self.memory_progress = ttk.Progressbar(memory_frame, length=int(150 * scale), mode='determinate')
        self.memory_progress.pack(pady=5)
        
        self.memory_label = tk.Label(memory_frame, text="0%", color=ThemeColors.FG_PRIMARY, 
                                    bg=ThemeColors.BG_PRIMARY, font=("Arial", int(9 * scale)))
        self.memory_label.pack()
        
        # 设置刻度标签颜色
        # for label in self.cpu_ax.get_xticklabels() + self.cpu_ax.get_yticklabels():
        #     label.set_color(ThemeColors.FG_PRIMARY)
        #     label.set_fontsize(int(7 * scale))
        
        # for label in self.memory_ax.get_xticklabels() + self.memory_ax.get_yticklabels():
        #     label.set_color(ThemeColors.FG_PRIMARY)
        #     label.set_fontsize(int(7 * scale))
    
    def update_charts(self, cpu_percent, memory_percent):
        """更新进度条数据"""
        # 更新CPU进度条
        self.cpu_progress['value'] = cpu_percent
        self.cpu_label.config(text=f"{cpu_percent:.1f}%")
        
        # 更新内存进度条
        self.memory_progress['value'] = memory_percent
        self.memory_label.config(text=f"{memory_percent:.1f}%")
        
        # 保存历史数据（用于可能的未来功能）
        current_time = time.strftime("%H:%M:%S")
        self.cpu_data.append(cpu_percent)
        self.memory_data.append(memory_percent)
        self.time_data.append(current_time)
    
    def on_window_resize(self, event):
        """处理窗口大小变化事件，调整图表大小"""
        # 只在主窗口大小变化时处理，避免递归调用
        if event.widget == self.root:
            # 获取当前缩放率
            scale = self.screen_info['scale_factor']
            
            # 更新图表大小
            chart_width = 6 * scale
            chart_height = 4 * scale
            
            # 更新CPU图表
            self.cpu_figure.set_size_inches(chart_width, chart_height)
            self.cpu_canvas.draw()
            
            # 更新内存图表
            self.memory_figure.set_size_inches(chart_width, chart_height)
            self.memory_canvas.draw()
    
    def calculate_window_size(self):
        """根据屏幕尺寸和缩放率计算窗口大小"""
        # 基准窗口尺寸（在96 DPI下）- 继续加宽窗口以满足用户需求
        base_width = 1560  # 继续增加窗口宽度至2000
        base_height = 750  # 保持高度不变
        
        # 基准最小窗口尺寸
        base_min_width = 1560  # 精简最小宽度至1000
        base_min_height = 750  # 精简最小高度至550
        
        # 根据屏幕尺寸和缩放率调整
        scale = self.screen_info['scale_factor']
        
        # 根据屏幕尺寸进一步调整
        screen_width = self.screen_info['screen_width']
        screen_height = self.screen_info['screen_height']
        
        # 计算窗口占屏幕的比例
        width_ratio = 0.65  # 精简宽度比例至65%
        height_ratio = 0.7  # 精简高度比例至70%
        
        # 根据屏幕尺寸调整比例
        if screen_width < 1920 or screen_height < 1080:
            # 小屏幕
            width_ratio = 0.7  # 小屏幕宽度比例
            height_ratio = 0.8  # 小屏幕高度比例
        elif screen_width >= 2560 and screen_height >= 1440:
            # 大屏幕
            width_ratio = 0.45  # 大屏幕宽度比例
            height_ratio = 0.55  # 大屏幕高度比例
        
        # 计算窗口尺寸
        window_width = int(min(base_width * scale, screen_width * width_ratio))
        window_height = int(min(base_height * scale, screen_height * height_ratio))
        
        # 计算最小窗口尺寸
        min_width = int(base_min_width * scale)
        min_height = int(base_min_height * scale)
        
        # 设置窗口大小和最小尺寸
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.minsize(min_width, min_height)
        
        # 居中窗口
        self.center_window()
        
        # 绑定窗口大小变化事件
        self.root.bind('<Configure>', self.on_window_resize)
    
    def center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # 计算居中位置
        x = (self.screen_info['screen_width'] // 2) - (window_width // 2)
        y = (self.screen_info['screen_height'] // 2) - (window_height // 2)
        
        # 设置窗口位置
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def on_window_resize(self, event):
        """窗口大小变化事件处理"""
        # 只在根窗口大小变化时处理
        if event.widget == self.root:
            # 可以在这里添加响应式布局逻辑
            # 例如调整字体大小、元素间距等
            pass
        
    def create_widgets(self):
        # 根据缩放率调整UI元素大小
        scale = self.screen_info['scale_factor']
        
        # 创建主框架 - 使用tk.Frame以更好地控制背景
        # 根据缩放率调整内边距
        padding_x = int(15 * scale)
        padding_y = int(15 * scale)
        self.main_frame = tk.Frame(self.root, bg=ThemeColors.BG_PRIMARY)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=padding_x, pady=padding_y)
        
        # 创建标题框架
        title_height = int(60 * scale)
        self.title_frame = tk.Frame(self.main_frame, bg=ThemeColors.BG_PRIMARY, height=title_height)
        self.title_frame.pack(fill=tk.X, pady=(0, int(15 * scale)))
        self.title_frame.pack_propagate(False)  # 防止框架被内容撑大
        
        # 创建企业级标题 - 根据缩放率调整字体大小
        title_font_size = int(20 * scale)
        self.title_label = tk.Label(
            self.title_frame, 
            text=f"TINECO 运维检测工具", 
            font=("微软雅黑", title_font_size, "bold"),
            bg=ThemeColors.BG_PRIMARY,
            fg=ThemeColors.CORPORATE_BLUE
        )
        self.title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # 创建内容区域 - 使用tk.Frame以保持一致的背景
        self.content_frame = tk.Frame(self.main_frame, bg=ThemeColors.BG_PRIMARY)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧列 - 系统信息
        left_container = tk.Frame(self.content_frame, bg=ThemeColors.BG_PRIMARY)
        left_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, int(5 * scale)))
        frame_font_size = int(12 * scale)
        left_frame = tk.LabelFrame(left_container, text="系统信息",
                                   bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.CORPORATE_BLUE,
                                   font=("微软雅黑", frame_font_size, "bold"), relief=tk.RAISED, bd=1)
        left_frame.pack(fill=tk.BOTH, expand=True, padx=int(10 * scale), pady=int(10 * scale))
        
        self.create_system_info_section(left_frame)
        
        # 中间列 - 性能监控
        middle_container = tk.Frame(self.content_frame, bg=ThemeColors.BG_PRIMARY)
        middle_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=int(5 * scale))
        middle_frame = tk.LabelFrame(middle_container, text="性能监控",
                                     bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.CORPORATE_BLUE,
                                     font=("微软雅黑", frame_font_size, "bold"), relief=tk.RAISED, bd=1)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=int(10 * scale), pady=int(10 * scale))
        
        self.create_performance_section(middle_frame)
        
        # 右侧列 - 网络测试
        right_container = tk.Frame(self.content_frame, bg=ThemeColors.BG_PRIMARY)
        right_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(int(5 * scale), 0))
        right_frame = tk.LabelFrame(right_container, text="网络测试",
                                   bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.CORPORATE_BLUE,
                                   font=("微软雅黑", frame_font_size, "bold"), relief=tk.RAISED, bd=1)
        right_frame.pack(fill=tk.BOTH, expand=True, padx=int(10 * scale), pady=int(10 * scale))
        
        self.create_network_section(right_frame)
        
    def create_system_info_section(self, parent):
        # 获取缩放率
        scale = self.screen_info['scale_factor']
        
        # 创建信息卡片容器
        info_cards_frame = ttk.Frame(parent)
        info_cards_frame.pack(fill=tk.X, pady=(0, int(15 * scale)))
        
        # 当前用户卡片 - 企业级样式
        user_card = tk.Frame(info_cards_frame, bg=ThemeColors.BG_SECONDARY, relief=tk.RAISED, bd=1)
        user_card.pack(fill=tk.X, pady=int(5 * scale))
        
        label_font_size = int(10 * scale)
        user_label = tk.Label(user_card, text="当前用户", bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", label_font_size, "bold"))
        user_label.pack(anchor=tk.W, padx=int(10 * scale), pady=(int(5 * scale), 0))
        
        self.username_var = tk.StringVar()
        user_value = tk.Label(user_card, textvariable=self.username_var, bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.FG_PRIMARY, font=("微软雅黑", label_font_size))
        user_value.pack(anchor=tk.W, padx=int(10 * scale), pady=(0, int(5 * scale)))
        
        # 计算机名称卡片 - 企业级样式
        computer_card = tk.Frame(info_cards_frame, bg=ThemeColors.BG_SECONDARY, relief=tk.RAISED, bd=1)
        computer_card.pack(fill=tk.X, pady=int(5 * scale))
        
        computer_label = tk.Label(computer_card, text="计算机名称", bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", label_font_size, "bold"))
        computer_label.pack(anchor=tk.W, padx=int(10 * scale), pady=(int(5 * scale), 0))
        
        self.computername_var = tk.StringVar()
        computer_value = tk.Label(computer_card, textvariable=self.computername_var, bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.FG_PRIMARY, font=("微软雅黑", label_font_size))
        computer_value.pack(anchor=tk.W, padx=int(10 * scale), pady=(0, int(5 * scale)))
        
        # 操作系统卡片 - 企业级样式
        os_card = tk.Frame(info_cards_frame, bg=ThemeColors.BG_SECONDARY, relief=tk.RAISED, bd=1)
        os_card.pack(fill=tk.X, pady=int(5 * scale))
        
        os_label = tk.Label(os_card, text="操作系统", bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", label_font_size, "bold"))
        os_label.pack(anchor=tk.W, padx=int(10 * scale), pady=(int(5 * scale), 0))
        
        self.os_var = tk.StringVar()
        os_value = tk.Label(os_card, textvariable=self.os_var, bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.FG_PRIMARY, font=("微软雅黑", label_font_size))
        os_value.pack(anchor=tk.W, padx=int(10 * scale), pady=(0, int(5 * scale)))
        
        # 网络适配器 - 企业级样式
        adapter_frame = ttk.Frame(parent)
        adapter_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_font_size = int(11 * scale)
        adapter_title = tk.Label(adapter_frame, text="网络适配器", bg=ThemeColors.BG_PRIMARY, fg=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", title_font_size, "bold"))
        adapter_title.pack(anchor=tk.W, pady=(0, int(5 * scale)))
        
        # 创建树形视图容器
        tree_container = tk.Frame(adapter_frame, bg=ThemeColors.BG_SECONDARY, relief=tk.SUNKEN, bd=1)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        # 创建树形视图显示网络适配器信息
        columns = ("适配器名称", "IP地址", "MAC地址")
        # 根据缩放率调整树形视图高度
        tree_height = int(10 * scale)
        self.adapter_tree = ttk.Treeview(tree_container, columns=columns, show="headings", height=tree_height)
        
        # 设置列标题和宽度 - 根据缩放率调整列宽
        self.adapter_tree.heading("适配器名称", text="适配器名称")
        self.adapter_tree.column("适配器名称", width=int(120 * scale))
        self.adapter_tree.heading("IP地址", text="IP地址")
        self.adapter_tree.column("IP地址", width=int(100 * scale))
        self.adapter_tree.heading("MAC地址", text="MAC地址")
        self.adapter_tree.column("MAC地址", width=int(120 * scale))
        
        # 不添加滚动条 - 禁用垂直滚动
        self.adapter_tree.configure(yscrollcommand=None)
        
        # 布局
        self.adapter_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=int(1 * scale), pady=int(1 * scale))
        
    def create_performance_section(self, parent):
        # 获取缩放率
        scale = self.screen_info['scale_factor']
        
        # CPU使用率显示 - 简化版本
        cpu_frame = tk.Frame(parent, bg=ThemeColors.BG_SECONDARY, relief=tk.RAISED, bd=1)
        cpu_frame.pack(fill=tk.X, pady=int(5 * scale), padx=int(5 * scale))
        
        label_font_size = int(10 * scale)
        cpu_label = tk.Label(cpu_frame, text="CPU使用率:", bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", label_font_size, "bold"))
        cpu_label.pack(side=tk.LEFT, padx=int(5 * scale))
        
        self.cpu_var = tk.StringVar(value="0.0%")
        cpu_value = tk.Label(cpu_frame, textvariable=self.cpu_var, bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.SUCCESS, font=("微软雅黑", label_font_size, "bold"))
        cpu_value.pack(side=tk.LEFT, padx=int(5 * scale))
        
        # 内存使用率显示 - 简化版本
        memory_frame = tk.Frame(parent, bg=ThemeColors.BG_SECONDARY, relief=tk.RAISED, bd=1)
        memory_frame.pack(fill=tk.X, pady=int(5 * scale), padx=int(5 * scale))
        
        memory_label = tk.Label(memory_frame, text="内存使用率:", bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", label_font_size, "bold"))
        memory_label.pack(side=tk.LEFT, padx=int(5 * scale))
        
        self.memory_var = tk.StringVar(value="0.0%")
        memory_value = tk.Label(memory_frame, textvariable=self.memory_var, bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.SUCCESS, font=("微软雅黑", label_font_size, "bold"))
        memory_value.pack(side=tk.LEFT, padx=int(5 * scale))
        
        # 添加图表显示区域
        # self.chart_frame.pack(fill=tk.BOTH, expand=True, pady=int(10 * scale), padx=int(5 * scale))  # 注释掉以移除图表显示
        
        # 内存详情
        self.memory_detail_var = tk.StringVar(value="0.00 GB / 0.00 GB")
        detail_font_size = int(9 * scale)
        memory_detail = tk.Label(memory_frame, textvariable=self.memory_detail_var, bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.FG_SECONDARY, font=("微软雅黑", detail_font_size))
        memory_detail.pack(side=tk.LEFT, padx=int(10 * scale))
        
        # 内存占用前3进程 - 简化版本
        title_font_size = int(11 * scale)
        process_frame = tk.LabelFrame(parent, text="内存占用前三进程",
                                     bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.CORPORATE_BLUE,
                                     font=("微软雅黑", title_font_size, "bold"), relief=tk.RAISED, bd=1)
        process_frame.pack(fill=tk.BOTH, expand=True, padx=int(5 * scale), pady=int(5 * scale))
        
        # 创建树形视图显示进程信息
        process_columns = ("进程名", "内存占用(MB)", "PID")
        # 根据缩放率调整树形视图高度
        tree_height = max(3, int(3 * scale))
        self.process_tree = ttk.Treeview(process_frame, columns=process_columns, show="headings", height=tree_height)
        
        # 设置列标题和宽度 - 根据缩放率调整列宽
        self.process_tree.heading("进程名", text="进程名")
        self.process_tree.heading("内存占用(MB)", text="内存占用(MB)")
        self.process_tree.heading("PID", text="PID")
        
        self.process_tree.column("进程名", width=int(120 * scale))
        self.process_tree.column("内存占用(MB)", width=int(80 * scale))
        self.process_tree.column("PID", width=int(60 * scale))
        
        # 不添加滚动条 - 禁用垂直滚动
        self.process_tree.configure(yscrollcommand=None)
        
        self.process_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=int(5 * scale), pady=int(5 * scale))
        
    def create_network_section(self, parent):
        # 获取缩放率
        scale = self.screen_info['scale_factor']
        
        # 网络连通性测试
        network_container = tk.Frame(parent, bg=ThemeColors.BG_PRIMARY)
        network_container.pack(fill=tk.BOTH, expand=True, pady=int(5 * scale), padx=int(5 * scale))
        
        title_font_size = int(12 * scale)
        network_frame = tk.LabelFrame(network_container, text="网络连通性测试",
                                     bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.CORPORATE_BLUE,
                                     font=("微软雅黑", title_font_size, "bold"), relief=tk.RAISED, bd=1)
        network_frame.pack(fill=tk.X, padx=int(10 * scale), pady=int(10 * scale))
        
        # 网络测试控制按钮
        network_control_frame = tk.Frame(network_frame, bg=ThemeColors.BG_SECONDARY)
        network_control_frame.pack(fill=tk.X, pady=int(5 * scale))
        
        button_font_size = int(9 * scale)
        self.network_start_btn = tk.Button(network_control_frame, text="开始测试", command=self.start_network_tests,
                                          bg=ThemeColors.CORPORATE_BLUE, fg="white", font=("微软雅黑", button_font_size, "bold"),
                                          relief=tk.FLAT, padx=int(10 * scale), pady=int(5 * scale))
        self.network_start_btn.pack(side=tk.LEFT, padx=int(5 * scale))
        
        self.network_stop_btn = tk.Button(network_control_frame, text="停止测试", command=self.stop_network_tests,
                                         state=tk.DISABLED, bg=ThemeColors.ERROR, fg="white",
                                         font=("微软雅黑", button_font_size, "bold"), relief=tk.FLAT, padx=int(10 * scale), pady=int(5 * scale))
        self.network_stop_btn.pack(side=tk.LEFT, padx=int(5 * scale))
        
        # 添加截图按钮
        self.screenshot_btn = tk.Button(network_control_frame, text="截图", command=self.take_screenshot,
                                      bg=ThemeColors.SUCCESS, fg="white", font=("微软雅黑", button_font_size, "bold"),
                                      relief=tk.FLAT, padx=int(10 * scale), pady=int(5 * scale))
        self.screenshot_btn.pack(side=tk.LEFT, padx=int(5 * scale))
        
        # 网络测试状态
        self.network_status_var = tk.StringVar(value="未开始")
        label_font_size = int(10 * scale)
        network_status_label = tk.Label(network_control_frame, textvariable=self.network_status_var,
                                       bg=ThemeColors.BG_SECONDARY, fg=ThemeColors.FG_PRIMARY, font=("微软雅黑", label_font_size))
        network_status_label.pack(side=tk.LEFT, padx=int(10 * scale))
        
        
        
        # 测试目标列表（带节点描述）
        self.test_targets = [
            ("10.100.4.254", "局域网网关节点"),
            ("10.100.4.13", "局域网出口节点"),
            ("171.221.219.1", "电信运营商网关节点"),
            ("162.128.207.69", "新加坡SDWAN专线节点"),
            ("www.baidu.com", "广域网国内业务"),
            ("www.youtube.com", "广域网国际业务"),
            ("icss-de.tineco.com", "icss国际业务系统"),
            ("tineco.s9.udeskglobal.com", "UD国际业务系统")
        ]
        
        # 测试结果卡片 - 根据缩放率调整
        results_card = tk.Frame(network_frame, bg=ThemeColors.BG_TERTIARY, relief=tk.SUNKEN, bd=1)
        results_card.pack(fill=tk.BOTH, expand=True, pady=int(5 * scale))
        
        # 测试结果标题 - 根据缩放率调整字体
        title_font_size = int(10 * scale)
        results_title = tk.Label(results_card, text="测试结果", bg=ThemeColors.BG_TERTIARY, fg=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", title_font_size, "bold"))
        results_title.pack(anchor=tk.W, padx=int(10 * scale), pady=(int(5 * scale), int(2 * scale)))
        
        # 创建统一的网格布局框架 - 包含标题和数据行
        unified_frame = tk.Frame(results_card, bg=ThemeColors.BG_TERTIARY)
        unified_frame.pack(fill=tk.X, padx=int(10 * scale), pady=(0, int(2 * scale)))
        
        # 配置网格列，确保对齐
        unified_frame.columnconfigure(0, weight=0, minsize=int(20 * 8 * scale))  # 节点描述列
        unified_frame.columnconfigure(1, weight=0, minsize=int(22 * 8 * scale))  # 测试地址列 - 适当增加宽度
        unified_frame.columnconfigure(2, weight=0, minsize=int(8 * 8 * scale))   # 状态列
        unified_frame.columnconfigure(3, weight=0, minsize=int(10 * 8 * scale))  # 延迟列
        unified_frame.columnconfigure(4, weight=0, minsize=int(10 * 8 * scale))  # 丢包率列
        unified_frame.columnconfigure(5, weight=0, minsize=int(10 * 8 * scale))  # 平均延迟列
        unified_frame.columnconfigure(6, weight=0, minsize=int(10 * 8 * scale))  # 平均丢包率列
        
        # 设置统一的列宽
        desc_width = int(20 * scale)
        target_width = int(22 * scale)  # 适当增加测试地址列宽度
        status_width = int(8 * scale)
        time_width = int(10 * scale)
        packet_loss_width = int(10 * scale)
        avg_time_width = int(10 * scale)
        avg_packet_loss_width = int(10 * scale)
        
        # 设置统一的间距
        left_pad = int(2 * scale)
        middle_pad = 0  # 移除列之间的额外间距
        
        header_font_size = int(9 * scale)
        
        # 添加列标题 - 第0行
        # 节点描述标题
        desc_header = tk.Label(unified_frame, text="节点描述", bg=ThemeColors.BG_TERTIARY, fg=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", header_font_size, "bold"), width=desc_width, anchor=tk.W)
        desc_header.grid(row=0, column=0, padx=(left_pad, 0), sticky="w")
        
        # 测试地址标题
        target_header = tk.Label(unified_frame, text="测试地址", bg=ThemeColors.BG_TERTIARY, fg=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", header_font_size, "bold"), width=target_width, anchor=tk.W)
        target_header.grid(row=0, column=1, padx=(left_pad, 0), sticky="w")
        
        # 状态标题
        status_header = tk.Label(unified_frame, text="状态", bg=ThemeColors.BG_TERTIARY, fg=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", header_font_size, "bold"), width=status_width, anchor=tk.CENTER)
        status_header.grid(row=0, column=2, padx=(0, middle_pad), sticky="w")
        
        # 当前值标题
        current_header = tk.Label(unified_frame, text="延迟", bg=ThemeColors.BG_TERTIARY, fg=ThemeColors.FG_SECONDARY, font=("微软雅黑", header_font_size), width=time_width, anchor=tk.CENTER)
        current_header.grid(row=0, column=3, padx=(0, middle_pad), sticky="w")
        
        # 当前丢包率标题
        current_loss_header = tk.Label(unified_frame, text="丢包率", bg=ThemeColors.BG_TERTIARY, fg=ThemeColors.FG_SECONDARY, font=("微软雅黑", header_font_size), width=packet_loss_width, anchor=tk.CENTER)
        current_loss_header.grid(row=0, column=4, padx=(0, middle_pad), sticky="w")
        
        # 平均值标题
        avg_header = tk.Label(unified_frame, text="平均延迟", bg=ThemeColors.BG_TERTIARY, fg=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", header_font_size, "bold"), width=avg_time_width, anchor=tk.CENTER)
        avg_header.grid(row=0, column=5, padx=(0, middle_pad), sticky="w")
        
        # 平均丢包率标题
        avg_loss_header = tk.Label(unified_frame, text="平均丢包", bg=ThemeColors.BG_TERTIARY, fg=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", header_font_size, "bold"), width=avg_packet_loss_width, anchor=tk.CENTER)
        avg_loss_header.grid(row=0, column=6, padx=(0, middle_pad), sticky="w")
        
        # 初始化移动平均值数据结构
        self.network_history = {}
        self.moving_average_size = 10  # 移动平均窗口大小
        
        # 测试结果 - 在同一框架中添加数据行，从第1行开始
        self.test_results = {}
        for i, (target, description) in enumerate(self.test_targets):
            label_font_size = int(9 * scale)
            row = i + 1  # 数据行从第1行开始，第0行是标题
            
            # 节点描述标签
            desc_label = tk.Label(unified_frame, text=description, bg=ThemeColors.BG_TERTIARY, fg=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", label_font_size, "bold"), width=desc_width, anchor=tk.W)
            desc_label.grid(row=row, column=0, padx=(left_pad, 0), sticky="w")
            
            # 测试地址标签
            target_label = tk.Label(unified_frame, text=target, bg=ThemeColors.BG_TERTIARY, fg=ThemeColors.FG_PRIMARY, font=("微软雅黑", label_font_size), width=target_width, anchor=tk.W)
            target_label.grid(row=row, column=1, padx=(left_pad, 0), sticky="w")
            
            status_var = tk.StringVar(value="未测试")
            status_label = tk.Label(unified_frame, textvariable=status_var, bg=ThemeColors.BG_TERTIARY, fg=ThemeColors.FG_SECONDARY, font=("微软雅黑", label_font_size, "bold"), width=status_width, anchor=tk.CENTER)
            status_label.grid(row=row, column=2, padx=(0, middle_pad), sticky="w")
            
            time_var = tk.StringVar(value="- ms")
            time_label = tk.Label(unified_frame, textvariable=time_var, bg=ThemeColors.BG_TERTIARY, fg=ThemeColors.FG_SECONDARY, font=("微软雅黑", label_font_size, "bold"), width=time_width, anchor=tk.CENTER)
            time_label.grid(row=row, column=3, padx=(0, middle_pad), sticky="w")
            
            packet_loss_var = tk.StringVar(value="- %")
            packet_loss_label = tk.Label(unified_frame, textvariable=packet_loss_var, bg=ThemeColors.BG_TERTIARY, fg=ThemeColors.FG_SECONDARY, font=("微软雅黑", label_font_size), width=packet_loss_width, anchor=tk.CENTER)
            packet_loss_label.grid(row=row, column=4, padx=(0, middle_pad), sticky="w")
            
            # 添加平均响应时间显示
            avg_time_var = tk.StringVar(value="- ms")
            avg_time_label = tk.Label(unified_frame, textvariable=avg_time_var, bg=ThemeColors.BG_TERTIARY, fg=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", label_font_size, "bold"), width=avg_time_width, anchor=tk.CENTER)
            avg_time_label.grid(row=row, column=5, padx=(0, middle_pad), sticky="w")
            
            # 添加平均丢包率显示
            avg_packet_loss_var = tk.StringVar(value="- %")
            avg_packet_loss_label = tk.Label(unified_frame, textvariable=avg_packet_loss_var, bg=ThemeColors.BG_TERTIARY, fg=ThemeColors.CORPORATE_BLUE, font=("微软雅黑", label_font_size, "bold"), width=avg_packet_loss_width, anchor=tk.CENTER)
            avg_packet_loss_label.grid(row=row, column=6, padx=(0, middle_pad), sticky="w")
            
            # 存储结果数据（包括状态标签用于颜色控制）
            self.test_results[target] = {
                "status_var": status_var,
                "status_label": status_label,
                "time_var": time_var,
                "packet_loss_var": packet_loss_var,
                "avg_time_var": avg_time_var,
                "avg_packet_loss_var": avg_packet_loss_var
            }
            
            # 初始化移动平均值数据结构
            self.network_history[target] = {
                "response_times": [],  # 存储最近的响应时间
                "packet_losses": [],   # 存储最近的丢包率
                "avg_time_var": avg_time_var,  # 平均响应时间显示
                "avg_packet_loss_var": avg_packet_loss_var  # 平均丢包率显示
            }
    
    def update_system_info(self):
        """更新系统信息"""
        # 获取用户名
        self.username_var.set(psutil.users()[0].name if psutil.users() else "未知")
        
        # 获取计算机名
        self.computername_var.set(socket.gethostname())
        
        # 获取操作系统信息
        self.os_var.set(f"{platform.system()} {platform.release()}")
        
        # 初始化时立即更新网络适配器信息
        if not hasattr(self, 'adapter_update_counter'):
            self.adapter_update_counter = 0
            self.update_adapter_info()  # 初始化时立即更新
        
        # 每次都更新网络适配器信息，实现5秒刷新一次
        self.update_adapter_info()
    
    def update_adapter_info(self):
        """更新网络适配器信息"""
        # 清除现有数据
        for item in self.adapter_tree.get_children():
            self.adapter_tree.delete(item)
        
        # 获取网络接口信息
        addrs = psutil.net_if_addrs()
        # 获取网络接口状态信息
        stats = psutil.net_if_stats()
        
        for interface_name, interface_addresses in addrs.items():
            ipv4 = ""
            mac = ""
            
            for address in interface_addresses:
                if address.family == socket.AF_INET:
                    ipv4 = address.address
                elif address.family == psutil.AF_LINK:
                    mac = address.address
            
            # 检查接口是否连接
            is_connected = False
            if interface_name in stats:
                # isup为True表示接口已连接，False表示媒体已断开连接
                is_connected = stats[interface_name].isup
            
            # 如果接口未连接，IP显示为"未连接"
            if not is_connected:
                ipv4 = "未连接"
            elif not ipv4:  # 如果接口连接但没有IP地址
                ipv4 = "正在获取IP..."
            
            if not mac:  # 如果没有MAC地址，显示为"未知"
                mac = "未知"
                
            # 添加所有接口到树形视图
            self.adapter_tree.insert("", "end", values=(interface_name, ipv4, mac))
        
        # 如果没有适配器信息，添加一条提示信息
        if not self.adapter_tree.get_children():
            self.adapter_tree.insert("", "end", values=("未找到网络适配器", "", ""))
    
    def update_performance_data(self):
        """更新性能数据"""
        # 获取CPU使用率 - 不使用interval参数避免阻塞
        cpu_percent = psutil.cpu_percent()
        self.cpu_var.set(f"{cpu_percent:.1f}%")
        
        # 获取内存信息
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        self.memory_var.set(f"{memory_percent:.1f}%")
        
        # 计算已用内存和总内存（GB）
        used_gb = memory.used / (1024**3)
        total_gb = memory.total / (1024**3)
        self.memory_detail_var.set(f"{used_gb:.2f} GB / {total_gb:.2f} GB")
        
        # 注释掉图表更新，完全移除图表以提高性能
        # self.update_charts(cpu_percent, memory_percent)
        
        # 初始化计数器（在首次运行时）
        if not hasattr(self, 'process_update_counter'):
            self.process_update_counter = 0
            self.system_update_counter = 0
        
        # 每次更新都获取进程信息，确保进程列表始终显示
        self.update_top_processes()
        
        # 每7次更新一次系统信息（包括网络适配器），减少资源消耗
        self.system_update_counter += 1
        if self.system_update_counter >= 7:
            self.update_system_info()
            self.system_update_counter = 0
        
        # 延长更新间隔至5秒，进一步减少CPU占用
        self.root.after(5000, self.update_performance_data)
    
    def update_top_processes(self):
        """更新内存占用前3的进程"""
        # 清除现有数据
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        # 获取所有进程
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                memory_info = proc.info['memory_info']
                if memory_info:
                    memory_mb = memory_info.rss / (1024 * 1024)  # 转换为MB
                    processes.append((name, memory_mb, pid))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # 按内存使用量排序并取前3
        processes.sort(key=lambda x: x[1], reverse=True)
        top_3 = processes[:3]
        
        # 添加到树形视图
        for name, memory_mb, pid in top_3:
            self.process_tree.insert("", "end", values=(name, f"{memory_mb:.1f}", pid))
    
    def start_network_tests(self):
        """开始网络连通性测试"""
        if not hasattr(self, 'network_test_thread') or not self.network_test_thread.is_alive():
            self.network_start_btn.config(state=tk.DISABLED)
            self.network_stop_btn.config(state=tk.NORMAL)
            self.network_status_var.set("测试中...")
            
            # 初始化停止标志
            self.network_stop_thread = False
            
            # 初始化线程列表
            self.network_test_threads = []
            
            # 重置所有测试结果
            for target, result in self.test_results.items():
                result["status_var"].set("等待中")
                result["time_var"].set("- ms")
                result["packet_loss_var"].set("- %")
            
            # 重置移动平均值历史数据
            for target in self.network_history:
                self.network_history[target]["response_times"] = []
                self.network_history[target]["packet_losses"] = []
                self.network_history[target]["avg_time_var"].set("- ms")
                self.network_history[target]["avg_packet_loss_var"].set("- %")
            
            self.network_test_thread = threading.Thread(target=self.test_network_targets)
            self.network_test_thread.daemon = True
            self.network_test_thread.start()
    
    def stop_network_tests(self):
        """停止网络连通性测试"""
        if hasattr(self, 'network_stop_thread'):
            self.network_stop_thread = True
            self.network_status_var.set("正在停止...")
            self.network_stop_btn.config(state=tk.DISABLED)
            
            # 使用异步方式检查线程状态，避免UI卡顿
            self.root.after(100, self.check_threads_stopped)
    
    def check_threads_stopped(self):
        """检查所有线程是否已停止，避免UI卡顿"""
        all_stopped = True
        if hasattr(self, 'network_test_threads'):
            for thread in self.network_test_threads:
                if thread.is_alive():
                    all_stopped = False
                    break
        
        if all_stopped:
            # 所有线程已停止，完成测试
            self.root.after(0, self.network_test_completed)
        else:
            # 仍有线程在运行，继续检查
            self.root.after(100, self.check_threads_stopped)
    
    def test_network_targets(self):
        """网络连通性测试线程 - 同时测试所有8个地址"""
        # 创建线程池同时测试所有地址
        threads = []
        for i, target in enumerate(self.test_targets):
            address = target[0] if isinstance(target, tuple) else target
            description = target[1] if isinstance(target, tuple) else address
            
            # 为每个目标创建测试线程
            thread = threading.Thread(target=self.test_single_target_thread, args=(address, description, i))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        # 保存线程引用，确保可以停止所有线程
        self.network_test_threads = threads
        
        # 不等待线程完成，让它们在后台持续运行
        # 测试完成标记
        self.root.after(0, self.network_test_started)
    
    def test_single_target_thread(self, target, description, index):
        """单个目标测试线程 - 持续ping"""
        # 持续ping循环
        while True:
            # 检查是否需要停止
            if hasattr(self, 'network_stop_thread') and self.network_stop_thread:
                # 线程即将退出，更新状态为"已停止"
                self.root.after(0, lambda: self.update_test_result(target, "已停止", "- ms", "- %"))
                break
            
            # 执行ping测试
            try:
                # 执行ping命令，发送1个包以快速获取响应时间
                output = subprocess.check_output(
                    ["ping", "-n", "1", target],
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=10,  # 设置超时为10秒
                    creationflags=subprocess.CREATE_NO_WINDOW  # 隐藏控制台窗口
                )
                
                # 解析结果获取响应时间和丢包率
                response_times = []
                packet_loss = 100  # 默认丢包率为100%
                
                # 逐行分析ping输出
                for line in output.split('\n'):
                    # 增强的响应时间解析，支持更多格式
                    if "时间=" in line or "time=" in line or "ms" in line.lower():
                        try:
                            # 尝试多种解析方法
                            time_extracted = False
                            
                            # 方法1: 标准中文格式 "时间=32ms"
                            if "时间=" in line:
                                time_part = line.split("时间=")[1]
                                if "ms" in time_part:
                                    time_str = time_part.split("ms")[0].strip()
                                    response_times.append(float(time_str))
                                    time_extracted = True
                            
                            # 方法2: 标准英文格式 "time=32ms" 或 "time=32.5ms"
                            if not time_extracted and "time=" in line:
                                time_part = line.split("time=")[1]
                                if "ms" in time_part:
                                    time_str = time_part.split("ms")[0].strip()
                                    response_times.append(float(time_str))
                                    time_extracted = True
                            
                            # 方法3: 正则表达式匹配各种时间格式
                            if not time_extracted:
                                import re
                                # 匹配 "时间=32ms", "time=32.5ms", "=32ms", "32ms" 等格式
                                time_patterns = [
                                    r'时间[=:](\d+\.?\d*)\s*ms',
                                    r'time[=:](\d+\.?\d*)\s*ms',
                                    r'[=:](\d+\.?\d*)\s*ms',
                                    r'(\d+\.?\d*)\s*ms'
                                ]
                                
                                for pattern in time_patterns:
                                    match = re.search(pattern, line, re.IGNORECASE)
                                    if match:
                                        time_str = match.group(1)
                                        response_times.append(float(time_str))
                                        time_extracted = True
                                        break
                            
                            # 方法4: 通用数字+ms模式
                            if not time_extracted:
                                import re
                                # 查找任何数字+ms的组合
                                match = re.search(r'(\d+\.?\d*)\s*ms', line, re.IGNORECASE)
                                if match:
                                    time_str = match.group(1)
                                    response_times.append(float(time_str))
                                    time_extracted = True
                                        
                        except (IndexError, ValueError, AttributeError):
                            # 如果所有方法都失败，继续下一行
                            pass
                    
                    # 查找丢包率信息 - 增强解析
                    if any(keyword in line for keyword in ["丢失 =", "Lost =", "packets transmitted", "packets received"]):
                        try:
                            # 中文系统格式: "丢失 = 0 (0% 丢失)"
                            if "丢失 =" in line:
                                if "(" in line and "%" in line:
                                    loss_str = line.split("(")[1].split("%")[0]
                                else:
                                    loss_str = line.split("丢失 = ")[1].split(" ")[0]
                                packet_loss = float(loss_str)
                            
                            # 英文系统格式: "Lost = 0 (0% loss)" 或统计行
                            elif "Lost =" in line or "lost" in line.lower():
                                if "(" in line and "%" in line:
                                    loss_str = line.split("(")[1].split("%")[0]
                                    packet_loss = float(loss_str)
                                elif "packets transmitted" in line and "packets received" in line:
                                    # 解析统计行: "4 packets transmitted, 4 received, 0% packet loss"
                                    import re
                                    match = re.search(r'(\d+)%\s*packet\s*loss', line, re.IGNORECASE)
                                    if match:
                                        packet_loss = float(match.group(1))
                                
                        except (IndexError, ValueError, AttributeError):
                            pass
                
                # 获取响应时间（单次ping）
                response_time = None
                if response_times:
                    response_time = response_times[0]  # 直接使用第一个响应时间
                
                # 增强的结果判断逻辑
                if response_time is not None and packet_loss < 100:
                    # 测试成功，有响应时间且丢包率小于100%
                    self.root.after(0, self.update_test_result, target, "成功", f"{response_time:.1f} ms", f"{packet_loss:.1f}%")
                elif packet_loss < 100:
                    # 有连通性但无法获取延迟，可能是解析问题
                    self.root.after(0, self.update_test_result, target, "已连接", "延迟解析失败", f"{packet_loss:.1f}%")
                elif response_time is not None:
                    # 能解析延迟但丢包率100%，可能是间歇性连接
                    self.root.after(0, self.update_test_result, target, "不稳定", f"{response_time:.1f} ms", f"{packet_loss:.1f}%")
                else:
                    # 完全无法连接
                    self.root.after(0, self.update_test_result, target, "失败", "- ms", f"{packet_loss:.1f}%")
                    
            except subprocess.TimeoutExpired:
                # 超时
                self.root.after(0, self.update_test_result, target, "超时", "- ms", "100%")
            except subprocess.CalledProcessError:
                # 连接失败
                self.root.after(0, self.update_test_result, target, "失败", "- ms", "100%")
            except Exception as e:
                # 其他错误
                self.root.after(0, self.update_test_result, target, "错误", "- ms", "100%")
            
            # 等待1秒后进行下一次测试
            import time
            time.sleep(1)
    
    
    
    def update_test_result(self, target, status, response_time, packet_loss):
        """更新单个测试结果 - 带颜色编码和移动平均值计算"""
        if target in self.test_results:
            # 根据状态设置颜色和字体
            if status in ["成功", "已连接"]:
                # 成功状态：绿色加粗
                fg_color = ThemeColors.SUCCESS
                font_weight = "bold"
            elif status in ["失败", "超时", "错误"]:
                # 失败状态：红色加粗
                fg_color = ThemeColors.ERROR
                font_weight = "bold"
            else:
                # 其他状态：默认颜色
                fg_color = ThemeColors.FG_PRIMARY
                font_weight = "normal"
            
            # 更新状态显示（带颜色）
            self.test_results[target]["status_var"].set(status)
            
            # 更新时间和丢包率显示
            self.test_results[target]["time_var"].set(response_time)
            self.test_results[target]["packet_loss_var"].set(packet_loss)
            
            # 获取缩放率
            scale = self.screen_info['scale_factor']
            label_font_size = int(9 * scale)
            
            # 更新状态标签的颜色和字体
            if "status_label" in self.test_results[target]:
                self.test_results[target]["status_label"].config(
                    fg=fg_color,
                    font=("微软雅黑", label_font_size, font_weight)
                )
            
            # 更新移动平均值
            self.update_moving_average(target, response_time, packet_loss)
    
    def update_moving_average(self, target, response_time, packet_loss):
        """收集测试数据，在测试结束时计算平均值"""
        # 只在测试进行中时收集数据，不显示平均值
        if not hasattr(self, 'network_stop_thread') or self.network_stop_thread:
            return
            
        if target not in self.network_history:
            return
            
        # 解析响应时间
        try:
            if response_time != "- ms" and "解析失败" not in response_time:
                # 提取数值部分
                time_value = float(response_time.split(" ")[0])
                self.network_history[target]["response_times"].append(time_value)
        except (ValueError, IndexError):
            pass
        
        # 解析丢包率
        try:
            if packet_loss != "- %":
                # 提取数值部分
                loss_value = float(packet_loss.split("%")[0])
                self.network_history[target]["packet_losses"].append(loss_value)
        except (ValueError, IndexError):
            pass
    
    def calculate_and_display_averages(self):
        """计算并显示所有目标的平均值"""
        for target in self.network_history:
            # 计算平均响应时间
            if self.network_history[target]["response_times"]:
                avg_time = sum(self.network_history[target]["response_times"]) / len(self.network_history[target]["response_times"])
                self.network_history[target]["avg_time_var"].set(f"{avg_time:.1f} ms")
            
            # 计算平均丢包率
            if self.network_history[target]["packet_losses"]:
                avg_loss = sum(self.network_history[target]["packet_losses"]) / len(self.network_history[target]["packet_losses"])
                self.network_history[target]["avg_packet_loss_var"].set(f"{avg_loss:.1f} %")
    
    def network_test_started(self):
        """网络测试已启动"""
        self.network_status_var.set("测试中...")
        self.network_start_btn.config(state=tk.DISABLED)
        self.network_stop_btn.config(state=tk.NORMAL)
    
    def network_test_completed(self):
        """网络测试完成"""
        # 计算并显示平均值
        self.calculate_and_display_averages()
        
        self.network_status_var.set("测试完成")
        self.network_start_btn.config(state=tk.NORMAL)
        self.network_stop_btn.config(state=tk.DISABLED)
        # 注意：不要重置network_stop_thread标志，保持为True以停止平均值更新
    
    def take_screenshot(self):
        """截取软件窗口并复制到剪贴板"""
        try:
            # 获取窗口位置和大小
            self.root.update_idletasks()  # 确保窗口布局已更新
            x = self.root.winfo_rootx()
            y = self.root.winfo_rooty()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            
            # 截取窗口区域
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            
            # 将图像复制到剪贴板，添加重试机制
            output = io.BytesIO()
            screenshot.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]  # 去掉BMP文件头
            output.close()
            
            # 尝试打开剪贴板，最多重试3次
            retry_count = 0
            max_retries = 3
            clipboard_success = False
            
            while retry_count < max_retries and not clipboard_success:
                try:
                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    win32clipboard.SetClipboardData(win32con.CF_DIB, data)
                    win32clipboard.CloseClipboard()
                    clipboard_success = True
                except Exception as clipboard_error:
                    retry_count += 1
                    if retry_count < max_retries:
                        # 短暂等待后重试
                        time.sleep(0.5)
                    else:
                        # 最后一次尝试失败，抛出异常
                        raise Exception(f"剪贴板操作失败: {str(clipboard_error)}")
            
            if clipboard_success:
                # 显示成功提示
                self.network_status_var.set("截图已复制到剪贴板，可使用Ctrl+V粘贴")
                self.root.after(3000, lambda: self.network_status_var.set(""))
            
        except Exception as e:
            print(f"截图失败: {e}")
            self.network_status_var.set("截图失败，请重试")
            self.root.after(3000, lambda: self.network_status_var.set(""))
    
    def on_closing(self):
        """窗口关闭时的处理"""
        if hasattr(self, 'network_stop_thread'):
            self.network_stop_thread = True
        
        if hasattr(self, 'network_test_thread') and self.network_test_thread.is_alive():
            self.network_test_thread.join(timeout=1)
        
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitor(root)
    root.mainloop()