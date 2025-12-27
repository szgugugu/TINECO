#!/usr/bin/env python3
"""
SystemMonitor 客户端启动脚本 - 从项目根目录启动
"""

import os
import sys

# 添加client目录到Python路径
client_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "client")
if client_dir not in sys.path:
    sys.path.insert(0, client_dir)

# 导入并运行客户端启动脚本
from start_client import start_client

if __name__ == "__main__":
    import argparse
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="SystemMonitor 客户端")
    parser.add_argument("--server", "-s", type=str, help="服务器地址 (例如: http://192.168.1.100:8000)")
    args = parser.parse_args()
    
    start_client(args.server)