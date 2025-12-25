import psutil
import socket

# 获取网络接口信息
addrs = psutil.net_if_addrs()

print(f"找到 {len(addrs)} 个网络接口:")
print()

for interface_name, interface_addresses in addrs.items():
    print(f"接口: {interface_name}")
    
    ipv4 = ""
    mac = ""
    
    for address in interface_addresses:
        print(f"  地址类型: {address.family}, 地址: {address.address}")
        if address.family == socket.AF_INET:
            ipv4 = address.address
        elif address.family == psutil.AF_LINK:
            mac = address.address
    
    print(f"  IPv4: {ipv4}")
    print(f"  MAC: {mac}")
    
    if mac:
        if not ipv4:
            ipv4 = "未连接"
        print(f"  将显示: ({interface_name}, {ipv4}, {mac})")
    
    print()