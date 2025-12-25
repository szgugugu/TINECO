import subprocess
import platform
import re

def test_ping_parsing():
    """测试ping输出解析"""
    # 测试中文系统ping输出
    chinese_output = '''
正在 Ping www.baidu.com [182.61.200.7] 具有 32 字节的数据:
来自 182.61.200.7 的回复: 字节=32 时间=12ms TTL=53
来自 182.61.200.7 的回复: 字节=32 时间=10ms TTL=53
来自 182.61.200.7 的回复: 字节=32 时间=11ms TTL=53
来自 182.61.200.7 的回复: 字节=32 时间=13ms TTL=53

182.61.200.7 的 Ping 统计信息:
    数据包: 已发送 = 4，已接收 = 4，丢失 = 0 (0% 丢失)，
往返行程的估计时间(以毫秒为单位):
    最短 = 10ms，最长 = 13ms，平均 = 11ms
    '''
    
    # 测试英文系统ping输出
    english_output = '''
Pinging www.baidu.com [182.61.200.7] with 32 bytes of data:
Reply from 182.61.200.7: bytes=32 time=12ms TTL=53
Reply from 182.61.200.7: bytes=32 time=10ms TTL=53
Reply from 182.61.200.7: bytes=32 time=11ms TTL=53
Reply from 182.61.200.7: bytes=32 time=13ms TTL=53

Ping statistics for 182.61.200.7:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 10ms, Maximum = 13ms, Average = 11ms
    '''
    
    # 测试有丢包的情况
    loss_output = '''
正在 Ping 192.168.1.1 具有 32 字节的数据:
请求超时。
来自 192.168.1.1 的回复: 字节=32 时间=15ms TTL=64
请求超时。
请求超时。

192.168.1.1 的 Ping 统计信息:
    数据包: 已发送 = 4，已接收 = 1，丢失 = 3 (75% 丢失)，
往返行程的估计时间(以毫秒为单位):
    最短 = 15ms，最长 = 15ms，平均 = 15ms
    '''
    
    def parse_ping_output(output):
        """解析ping输出，返回平均响应时间和丢包率"""
        response_times = []
        packet_loss = 100.0  # 默认100%丢包
        
        lines = output.split('\n')
        for line in lines:
            # 解析响应时间 - 同时支持中英文系统
            if "time=" in line and "ms" in line:
                try:
                    time_str = line.split("time=")[1].split("ms")[0]
                    response_times.append(float(time_str))
                except (IndexError, ValueError):
                    pass
            elif "时间=" in line and "ms" in line:  # 中文系统
                try:
                    time_str = line.split("时间=")[1].split("ms")[0]
                    response_times.append(float(time_str))
                except (IndexError, ValueError):
                    pass
            
            # 查找丢包率信息
            print(f"检查行: {line}")  # 调试输出
            if "丢失 =" in line or "Lost =" in line:
                print(f"找到丢包率行: {line}")  # 调试输出
                try:
                    if "丢失 =" in line:  # 中文系统，格式: "丢失 = 0 (0% 丢失)"
                        if "(" in line and "%" in line:
                            loss_str = line.split("(")[1].split("%")[0]
                            print(f"解析中文丢包率: {loss_str}")  # 调试输出
                        else:
                            # 如果没有括号，尝试直接从数字中提取
                            numbers = re.findall(r'\d+', line)
                            if numbers:
                                loss_str = numbers[-1]  # 取最后一个数字（丢包数）
                                print(f"解析中文丢包率(备选): {loss_str}")  # 调试输出
                    elif "Lost =" in line and "(" in line and "%" in line:  # 英文系统
                            loss_str = line.split("(")[1].split("%")[0]
                            print(f"解析英文丢包率: {loss_str}")  # 调试输出
                    packet_loss = float(loss_str)
                    print(f"设置丢包率为: {packet_loss}")  # 调试输出
                except (IndexError, ValueError) as e:
                    print(f"解析丢包率失败: {e}")  # 调试输出
                    pass
        
        # 计算平均响应时间
        avg_response_time = None
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
        
        return avg_response_time, packet_loss
    
    # 测试中文系统输出
    print("中文系统ping输出:")
    print(chinese_output)
    print("="*50)
    avg_time, loss_rate = parse_ping_output(chinese_output)
    print(f"中文系统测试结果: 平均响应时间={avg_time}ms, 丢包率={loss_rate}%")
    assert avg_time == 11.5  # (12+10+11+13)/4
    assert loss_rate == 0.0
    
    # 测试英文系统输出
    avg_time, loss_rate = parse_ping_output(english_output)
    print(f"英文系统测试结果: 平均响应时间={avg_time}ms, 丢包率={loss_rate}%")
    assert avg_time == 11.5  # (12+10+11+13)/4
    assert loss_rate == 0.0
    
    # 测试有丢包的情况
    avg_time, loss_rate = parse_ping_output(loss_output)
    print(f"丢包情况测试结果: 平均响应时间={avg_time}ms, 丢包率={loss_rate}%")
    assert avg_time == 15.0
    assert loss_rate == 75.0
    
    print("所有测试通过!")

if __name__ == "__main__":
    test_ping_parsing()
