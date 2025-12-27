#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试客户端程序
"""

import os
import sys
import importlib
import subprocess

def test_dependencies():
    """测试客户端依赖是否满足"""
    print("=" * 50)
    print("测试客户端依赖...")
    print("=" * 50)
    
    dependencies = [
        ("tkinter", "内置GUI库"),
        ("requests", "HTTP请求库"),
        ("psutil", "系统信息库"),
        ("PIL", "图像处理库"),
        ("win32clipboard", "Windows剪贴板库"),
        ("win32con", "Windows常量库"),
        ("ctypes", "系统调用库"),
        ("uuid", "UUID生成库"),
        ("json", "JSON处理库"),
        ("threading", "线程库"),
        ("argparse", "命令行参数解析库")
    ]
    
    missing_deps = []
    
    for dep_name, description in dependencies:
        try:
            if dep_name == "PIL":
                importlib.import_module("PIL")
            elif dep_name == "win32clipboard" or dep_name == "win32con":
                importlib.import_module("win32clipboard")
                importlib.import_module("win32con")
            else:
                importlib.import_module(dep_name)
            print(f"✓ {dep_name} - {description}")
        except ImportError:
            print(f"✗ {dep_name} - {description} (缺失)")
            missing_deps.append(dep_name)
    
    if missing_deps:
        print("\n缺少以下依赖:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\n请运行以下命令安装缺少的依赖:")
        print(f"pip install {' '.join(missing_deps)}")
        return False
    else:
        print("\n所有依赖都已满足!")
        return True

def test_client_files():
    """测试客户端文件是否存在"""
    print("\n" + "=" * 50)
    print("测试客户端文件...")
    print("=" * 50)
    
    required_files = [
        ("start_client.py", "客户端启动脚本"),
        ("system_monitor.py", "客户端主程序"),
        ("client_requirements.txt", "客户端依赖列表")
    ]
    
    missing_files = []
    
    for file_name, description in required_files:
        if os.path.exists(file_name):
            print(f"✓ {file_name} - {description}")
        else:
            print(f"✗ {file_name} - {description} (缺失)")
            missing_files.append(file_name)
    
    if missing_files:
        print("\n缺少以下文件:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("\n所有必需文件都存在!")
        return True

def test_client_import():
    """测试客户端模块是否可以正常导入"""
    print("\n" + "=" * 50)
    print("测试客户端模块导入...")
    print("=" * 50)
    
    try:
        # 测试导入主模块
        print("正在导入 system_monitor 模块...")
        import system_monitor
        print("✓ system_monitor 模块导入成功")
        
        # 检查SystemMonitor类
        if hasattr(system_monitor, 'SystemMonitor'):
            print("✓ SystemMonitor 类存在")
        else:
            print("✗ SystemMonitor 类不存在")
            return False
        
        # 检查远程监控方法
        if hasattr(system_monitor.SystemMonitor, 'start_remote_monitoring'):
            print("✓ start_remote_monitoring 方法存在")
        else:
            print("✗ start_remote_monitoring 方法不存在")
            return False
        
        print("\n模块导入测试通过!")
        return True
    except Exception as e:
        print(f"✗ 模块导入失败: {e}")
        return False

def test_server_connection():
    """测试与服务器连接"""
    print("\n" + "=" * 50)
    print("测试与服务器连接...")
    print("=" * 50)
    
    try:
        import requests
        
        # 默认服务器地址
        server_url = os.environ.get("SYSTEM_MONITOR_SERVER", "http://localhost:8000")
        print(f"测试服务器地址: {server_url}")
        
        # 测试基本连接
        try:
            response = requests.get(f"{server_url}/api/clients", timeout=5)
            if response.status_code == 200:
                print("✓ 服务器连接成功")
                print(f"✓ 服务器响应: {response.status_code}")
                return True
            else:
                print(f"✗ 服务器响应异常: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("✗ 无法连接到服务器")
            print("请确保服务器已启动 (运行 start_backend.py 或 console_launcher.py start)")
            return False
        except Exception as e:
            print(f"✗ 连接测试失败: {e}")
            return False
    except ImportError:
        print("✗ requests 库未安装")
        return False

def main():
    """主测试函数"""
    print("SystemMonitor 客户端测试程序")
    print("=" * 50)
    
    tests = [
        ("依赖测试", test_dependencies),
        ("文件测试", test_client_files),
        ("导入测试", test_client_import),
        ("服务器连接测试", test_server_connection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name}执行出错: {e}")
            results.append((test_name, False))
    
    # 输出测试结果摘要
    print("\n" + "=" * 50)
    print("测试结果摘要")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "通过" if result else "失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(results)} 测试通过")
    
    if passed == len(results):
        print("\n🎉 所有测试通过! 客户端程序正常。")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请检查上述问题。")
        return 1

if __name__ == "__main__":
    sys.exit(main())