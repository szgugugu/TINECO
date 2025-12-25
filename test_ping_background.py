import subprocess
import time

# 测试ping命令是否在后台运行
print("测试ping命令后台运行...")

try:
    # 使用与系统监控应用相同的参数执行ping命令
    output = subprocess.check_output(
        ["ping", "-n", "2", "127.0.0.1"],  # 发送2个包到本地回环地址
        stderr=subprocess.STDOUT,
        text=True,
        timeout=5,
        creationflags=subprocess.CREATE_NO_WINDOW  # 隐藏控制台窗口
    )
    
    print("ping命令执行完成，没有显示控制台窗口")
    print("输出结果:")
    print(output[:200] + "..." if len(output) > 200 else output)  # 只显示前200个字符
    
except subprocess.CalledProcessError as e:
    print(f"ping命令执行失败: {e}")
except subprocess.TimeoutExpired:
    print("ping命令超时")
except Exception as e:
    print(f"发生错误: {e}")

print("\n测试完成。如果您没有看到控制台窗口弹出，说明ping命令已在后台运行。")
time.sleep(2)  # 等待2秒以便用户观察