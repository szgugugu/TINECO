# SystemMonitor 远程监控系统

## 概述

SystemMonitor 远程监控系统是一个基于 Web 的实时监控解决方案，允许您远程监控使用 SystemMonitor 软件的用户，并实时获取他们软件中的所有信息。此外，您还可以通过后台网页修改网络连通性测试配置，这些更改将自动同步到所有用户的 SystemMonitor 软件中。

## 系统架构

系统由以下组件组成：

1. **后端服务器** (FastAPI)
   - 处理客户端注册和数据收集
   - 提供 RESTful API 接口
   - 管理配置分发

2. **前端监控网页** (Bootstrap + Chart.js)
   - 实时显示所有客户端状态
   - 提供配置管理界面
   - 展示系统性能和网络测试结果

3. **客户端集成模块**
   - 远程监控功能直接集成到 SystemMonitor 源代码
   - 自动启动远程监控功能
   - 定期上报数据和获取配置更新

## 快速开始

### 1. 启动后端服务器

```bash
python start_backend.py
```

服务器启动后，您可以访问以下 URL：
- 监控面板: http://localhost:8000
- 配置管理: http://localhost:8000/config

### 2. 启动客户端

```bash
python start_client.py
```

或者，您也可以直接运行原始的 SystemMonitor，远程监控功能已自动集成：

```python
# SystemMonitor 启动时会自动启动远程监控功能
# 无需额外代码
```

## 功能特性

### 实时监控
- 查看所有在线/离线客户端
- 实时显示系统性能（CPU、内存使用率）
- 监控网络连通性测试结果
- 客户端详细信息展示

### 配置管理
- 动态修改网络测试目标
- 调整测试间隔
- 配置自动同步到所有客户端

### 扩展性
- 远程监控功能直接集成到 SystemMonitor
- 无需额外扩展模块
- 易于维护和升级

## 系统要求

- Python 3.7+
- 网络连接
- 现代浏览器（用于访问监控面板）

## 安装依赖

### 后端依赖
```bash
cd backend
pip install -r requirements.txt
```

### 客户端依赖
```bash
pip install requests
```

## 使用说明

### 监控面板
1. 访问 http://localhost:8000
2. 查看客户端列表，点击任意客户端查看详细信息
3. 系统性能图表会实时更新
4. 网络测试结果显示在表格中

### 配置管理
1. 访问 http://localhost:8000/config
2. 修改测试间隔和测试目标
3. 点击"保存配置"按钮
4. 配置将自动同步到所有客户端

## API 接口

### 客户端注册
```
POST /api/client/register
```

### 上报数据
```
POST /api/client/data
```

### 获取配置
```
GET /api/config/get?client_id={client_id}
```

### 更新配置
```
POST /api/config/update
```

### 获取所有客户端
```
GET /api/clients
```

### 获取特定客户端
```
GET /api/clients/{client_id}
```

## 故障排除

### 客户端无法连接到服务器
1. 检查服务器是否已启动
2. 确认防火墙设置
3. 验证网络连接

### 配置未同步
1. 检查客户端是否在线
2. 确认配置已正确保存
3. 客户端可能需要重启以应用新配置

## 开发说明

### 添加新功能
1. 修改后端 API (backend/main.py)
2. 更新前端界面 (templates/)
3. 扩展客户端功能 (system_monitor.py)

### 自定义服务器地址
修改以下文件中的服务器 URL：
- start_client.py
- system_monitor.py

## 许可证

本项目遵循与原始 SystemMonitor 项目相同的许可证。

## 联系方式

如有问题或建议，请联系开发团队。