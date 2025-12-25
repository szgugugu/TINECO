import subprocess
import re

def parse_ping_output(output):
    """
    解析ping命令的输出，提取平均响应时间和丢包率
    """
    # 默认值
    avg_response_time = 0
    packet_loss = 100  # 默认丢包率为100%
    response_times = []
    
    # 逐行分析ping输出
    print(f"[DEBUG] Ping输出内容:\n{output}")
    for line in output.split('\n'):
        if "时间=" in line or "time=" in line:
            try:
                # 提取响应时间（毫秒）
                if "时间=" in line:  # 中文系统
                    time_str = line.split("时间=")[1].split("ms")[0]
                else:  # 英文系统
                    time_str = line.split("time=")[1].split("ms")[0]
                response_times.append(float(time_str))
            except (IndexError, ValueError):
                pass
        
        # 查找丢包率信息
        if "丢失 =" in line or "Lost =" in line:
            print(f"[DEBUG] 找到丢包率行: {line}")
            try:
                if "丢失 =" in line:  # 中文系统
                    # 中文系统格式: "丢失 = 0 (0% 丢失)"
                    if "(" in line and "%" in line:
                        # 使用括号内的百分比作为丢包率
                        loss_str = line.split("(")[1].split("%")[0]
                    else:
                        # 备用方法：直接分割
                        loss_str = line.split("丢失 = ")[1].split(" ")[0]
                    print(f"[DEBUG] 中文系统解析，loss_str={loss_str}")
                elif "Lost =" in line and "(" in line and "%" in line:  # 英文系统
                    loss_str = line.split("(")[1].split("%")[0]
                    print(f"[DEBUG] 英文系统解析，loss_str={loss_str}")
                packet_loss = float(loss_str)
                print(f"[DEBUG] 设置丢包率: {packet_loss}%")
            except (IndexError, ValueError) as e:
                print(f"[DEBUG] 丢包率解析失败: {e}")
                pass
    
    # 计算平均响应时间
    if response_times:
        avg_response_time = sum(response_times) / len(response_times)
    
    return avg_response_time, packet_loss

# 测试中文系统ping输出
chinese_output = """正在 Ping www.baidu.com [180.101.49.44] 具有 32 字节的数据:
来自 180.101.49.44 的回复: 字节=32 时间=8ms TTL=53
来自 180.101.49.44 的回复: 字节=32 时间=10ms TTL=53
来自 180.101.49.44 的回复: 字节=32 时间=11ms TTL=53
来自 180.101.49.44 的回复: 字节=32 时间=9ms TTL=53

180.101.49.44 的 Ping 统计信息:
    数据包: 已发送 = 4，已接收 = 4，丢失 = 0 (0% 丢失)，
往返行程的估计时间(以毫秒为单位):
    最短 = 8ms，最长 = 11ms，平均 = 9ms"""

avg_time, loss_rate = parse_ping_output(chinese_output)
print(f"\n结果: 平均响应时间={avg_time}ms, 丢包率={loss_rate}%")
assert avg_time == 9.5  # 四个响应时间: 8, 10, 11, 9，平均为9.5
assert loss_rate == 0.0

# 测试实际ping命令
print("\n测试实际ping命令...")
result = subprocess.run(['ping', '-n', '4', 'www.baidu.com'], capture_output=True, text=True)
real_avg_time, real_loss_rate = parse_ping_output(result.stdout)
print(f"\n实际结果: 平均响应时间={real_avg_time}ms, 丢包率={real_loss_rate}%")