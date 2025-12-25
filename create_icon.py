from PIL import Image, ImageDraw
import io
import os

def create_icon():
    # 创建一个64x64的图标
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制背景圆形
    draw.ellipse([4, 4, size-4, size-4], fill=(37, 99, 235, 255))  # #2563eb in RGB
    
    # 绘制网络图标 - 两个连接的计算机
    # 左侧计算机
    left_computer = [10, 25, 30, 39]  # x1, y1, x2, y2
    draw.rectangle(left_computer, fill=(255, 255, 255, 255))
    draw.rectangle([14, 28, 26, 34], fill=(37, 99, 235, 255))
    draw.rectangle([19, 39, 23, 42], fill=(255, 255, 255, 255))
    
    # 右侧计算机
    right_computer = [35, 25, 55, 39]
    draw.rectangle(right_computer, fill=(255, 255, 255, 255))
    draw.rectangle([39, 28, 51, 34], fill=(37, 99, 235, 255))
    draw.rectangle([44, 39, 48, 42], fill=(255, 255, 255, 255))
    
    # 连接线
    draw.line([30, 32, 35, 32], fill=(255, 255, 255, 255), width=2)
    draw.ellipse([31, 29, 34, 35], fill=(255, 255, 255, 255))
    
    # 系统监控图表
    chart_bg = [22, 48, 42, 63]
    draw.rectangle(chart_bg, fill=(255, 255, 255, 230))
    
    # CPU使用率条形图
    bar_width = 2
    bar_height = 5
    bar_x = 25
    bar_y = 50
    for i in range(5):
        height = 2 + i % 3
        draw.rectangle([bar_x + i*bar_width, bar_y + bar_height - height, 
                       bar_x + i*bar_width + bar_width - 1, bar_y + bar_height], 
                      fill=(16, 185, 129, 255))  # #10b981 in RGB
    
    # 内存使用率折线图
    points = [(25, 58), (28, 55), (31, 56), (34, 53), (37, 54), (40, 52), (43, 53)]
    for i in range(len(points) - 1):
        draw.line([points[i][0], points[i][1], points[i+1][0], points[i+1][1]], 
                 fill=(59, 130, 246, 255), width=1)
    
    # 保存为ICO文件
    img.save('icon.ico', format='ICO', sizes=[(64,64), (32,32), (16,16)])
    
    print("图标已创建: icon.ico")

if __name__ == "__main__":
    create_icon()