"""
SystemMonitor 远程监控系统测试脚本
"""

import requests
import json
import time
import random
import threading

# 服务器URL
BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """测试API端点"""
    print("测试API端点...")
    
    # 测试获取所有客户端
    try:
        response = requests.get(f"{BASE_URL}/api/clients")
        if response.status_code == 200:
            print("✓ 获取所有客户端 API 正常")
        else:
            print(f"✗ 获取所有客户端 API 失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 获取所有客户端 API 错误: {e}")
    
    # 测试获取配置
    try:
        response = requests.get(f"{BASE_URL}/api/config/get?client_id=test")
        if response.status_code == 200:
            print("✓ 获取配置 API 正常")
        else:
            print(f"✗ 获取配置 API 失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 获取配置 API 错误: {e}")

def simulate_client(client_id, duration=60):
    """模拟客户端行为"""
    print(f"启动模拟客户端 {client_id}")
    
    # 注册客户端
    client_info = {
        "client_id": client_id,
        "computer_name": f"TestPC-{client_id}",
        "user_name": f"TestUser-{client_id}",
        "os_info": "Windows 10 Test",
        "ip_address": f"192.168.1.{100 + int(client_id[-1])}",
        "version": "v1.6.0"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/client/register", json=client_info)
        if response.status_code == 200:
            print(f"✓ 客户端 {client_id} 注册成功")
        else:
            print(f"✗ 客户端 {client_id} 注册失败: {response.status_code}")
            return
    except Exception as e:
        print(f"✗ 客户端 {client_id} 注册错误: {e}")
        return
    
    # 定期上报数据
    start_time = time.time()
    while time.time() - start_time < duration:
        # 生成随机系统数据
        system_data = {
            "cpu_percent": random.uniform(10, 80),
            "memory_percent": random.uniform(30, 70),
            "timestamp": time.time()
        }
        
        # 生成随机网络测试结果
        network_results = [
            {
                "target_name": "百度",
                "target_address": "www.baidu.com",
                "status": "正常" if random.random() > 0.2 else "异常",
                "latency": random.uniform(20, 100) if random.random() > 0.2 else None,
                "packet_loss": random.uniform(0, 5) if random.random() > 0.3 else None,
                "timestamp": time.time()
            },
            {
                "target_name": "TikTok",
                "target_address": "www.tiktok.com",
                "status": "正常" if random.random() > 0.3 else "异常",
                "latency": random.uniform(50, 200) if random.random() > 0.3 else None,
                "packet_loss": random.uniform(0, 10) if random.random() > 0.4 else None,
                "timestamp": time.time()
            },
            {
                "target_name": "测试服务器",
                "target_address": "162.128.207.69",
                "status": "正常" if random.random() > 0.15 else "异常",
                "latency": random.uniform(10, 50) if random.random() > 0.15 else None,
                "packet_loss": random.uniform(0, 2) if random.random() > 0.5 else None,
                "timestamp": time.time()
            }
        ]
        
        # 上报数据
        report_data = {
            "client_id": client_id,
            "system_data": system_data,
            "network_results": network_results
        }
        
        try:
            response = requests.post(f"{BASE_URL}/api/client/data", json=report_data)
            if response.status_code == 200:
                print(f"✓ 客户端 {client_id} 数据上报成功")
            else:
                print(f"✗ 客户端 {client_id} 数据上报失败: {response.status_code}")
        except Exception as e:
            print(f"✗ 客户端 {client_id} 数据上报错误: {e}")
        
        # 等待一段时间
        time.sleep(10)
    
    print(f"模拟客户端 {client_id} 完成")

def test_config_update():
    """测试配置更新"""
    print("测试配置更新...")
    
    # 新配置
    new_config = {
        "targets": [
            {"name": "百度", "address": "www.baidu.com"},
            {"name": "GitHub", "address": "github.com"},
            {"name": "Google", "address": "www.google.com"},
            {"name": "新测试服务器", "address": "192.168.1.100"}
        ],
        "interval": 2.0
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/config/update", json=new_config)
        if response.status_code == 200:
            print("✓ 配置更新成功")
        else:
            print(f"✗ 配置更新失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 配置更新错误: {e}")

def main():
    """主测试函数"""
    print("SystemMonitor 远程监控系统测试")
    print("=" * 50)
    
    # 测试API端点
    test_api_endpoints()
    print()
    
    # 启动模拟客户端
    client_threads = []
    for i in range(3):
        client_id = f"test-client-{i+1}"
        thread = threading.Thread(target=simulate_client, args=(client_id, 60))
        thread.start()
        client_threads.append(thread)
        time.sleep(2)  # 错开客户端启动时间
    
    # 等待一段时间让客户端上报数据
    print("等待客户端上报数据...")
    time.sleep(30)
    
    # 测试配置更新
    test_config_update()
    print()
    
    # 等待所有客户端完成
    for thread in client_threads:
        thread.join()
    
    print("测试完成！")
    print(f"请访问 {BASE_URL} 查看监控面板")
    print(f"请访问 {BASE_URL}/config 查看配置管理")

if __name__ == "__main__":
    main()