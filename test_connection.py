#!/usr/bin/env python3
"""
测试客户端连接脚本
用于测试客户端是否能成功连接到服务器
"""

import requests
import time
import hashlib
import socket
import platform
import os

def test_connection(server_url="http://localhost:8000"):
    """测试连接到服务器"""
    print(f"测试连接到服务器: {server_url}")
    
    try:
        # 测试基本连接
        response = requests.get(f"{server_url}/api/clients", timeout=5)
        print(f"连接测试成功，状态码: {response.status_code}")
        
        # 生成客户端信息
        computer_name = socket.gethostname()
        user_name = os.environ.get("USERNAME", "test_user")
        id_string = f"{computer_name}_{user_name}_test"
        client_id = hashlib.md5(id_string.encode()).hexdigest()[:16]
        
        client_info = {
            "client_id": client_id,
            "computer_name": f"{computer_name}_test",
            "user_name": user_name,
            "os_info": f"{platform.system()} {platform.release()}",
            "ip_address": get_local_ip(),
            "version": "1.0.0"
        }
        
        # 注册客户端
        print(f"注册测试客户端: {client_info['computer_name']}")
        response = requests.post(f"{server_url}/api/client/register", json=client_info, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"客户端注册成功，ID: {result['client_id']}")
            
            # 发送测试数据
            test_data = {
                "client_id": result['client_id'],
                "system_data": {
                    "cpu_percent": 25.5,
                    "memory_percent": 60.2,
                    "disk_usage": 45.8,
                    "uptime": 3600,
                    "timestamp": time.time()
                },
                "network_results": [
                    {
                        "target_name": "测试目标",
                        "target_address": "www.example.com",
                        "status": "success",
                        "latency": 25.5,
                        "packet_loss": 0.0,
                        "avg_latency": 23.2,
                        "avg_packet_loss": 0.1,
                        "timestamp": time.time()
                    }
                ]
            }
            
            response = requests.post(f"{server_url}/api/client/data", json=test_data, timeout=5)
            
            if response.status_code == 200:
                print("测试数据发送成功")
                
                # 查询客户端列表
                response = requests.get(f"{server_url}/api/clients", timeout=5)
                if response.status_code == 200:
                    clients = response.json().get("clients", [])
                    test_client = next((c for c in clients if c["client_id"] == result['client_id']), None)
                    if test_client:
                        print("测试客户端已在服务器上显示")
                        print(f"客户端信息: {test_client['info']['computer_name']} - {test_client['info']['user_name']}")
                        print(f"在线状态: {'在线' if test_client['is_online'] else '离线'}")
                    else:
                        print("警告: 测试客户端未在服务器上显示")
            else:
                print(f"测试数据发送失败，状态码: {response.status_code}")
        else:
            print(f"客户端注册失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"连接测试失败: {e}")

def get_local_ip():
    """获取本机IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="测试客户端连接")
    parser.add_argument("--server", "-s", default="http://localhost:8000", 
                       help="服务器地址 (默认: http://localhost:8000)")
    args = parser.parse_args()
    
    test_connection(args.server)