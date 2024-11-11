# SCUM 北极熊内置机器人源代码

一个功能强大的SCUM游戏服务器内置管理机器人,提供全面的游戏管理、玩家服务和自动化运维功能。

## 核心功能

### 1. 玩家管理系统
- 玩家数据管理(等级/称号/权限等)
- 签到奖励系统
- VIP会员体系
- 装备卡系统
- 在线奖励发放

### 2. 经济系统
- 多币种管理(美金/熊币)
- 商城交易系统
- 红包系统
- 抽奖系统
- 礼包系统

### 3. 游戏玩法
- 龙虎斗小游戏
- 副本挑战系统  
- 车辆保险系统
- 物品回收系统
- 空投召唤系统

### 4. 权限管理
- 管理员权限分配
- 权限使用监控
- 自动警告封禁
- 管理日志记录

### 5. 运维功能
- FTP日志管理
- 自动重连机制
- 状态监控预警
- 数据备份恢复
- 配置热更新

## 技术特性

- Python实现
- Web界面管理
- SQLite数据存储
- 多线程处理 
- 事件驱动
- 配置热加载
- FTP协议支持
- 异常处理机制
- 日志记录追踪

## 系统要求

- Windows 系统
- Python 3.7+
- 管理员权限运行

## 安装步骤

1. 安装Python环境:
```bash
# 安装Python 3.7+
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

3. 运行程序:
```bash
python main.py
```

## 配置说明

主要配置项:
```json
{
  "ftpConfig": {
    "host": "",
    "port": "",
    "user": "",
    "password": ""
  },
  "gameConfig": {
    "serverName": "",
    "adminList": []
  },
  "moduleConfig": {
    "vip": true,
    "shop": true,
    "lottery": true
  }
}
```

## 数据库结构

主要数据表:
- user_list: 玩家信息
- card_list: 礼品卡
- sign_log: 签到记录  
- lhd_log: 龙虎斗记录
- admin_log: 管理日志

## API接口

提供Web API:
- 用户管理
- 商品管理  
- 日志查询
- 配置修改
- 等

## 常见问题

1. 启动失败
- 检查权限
- 检查配置
- 查看日志

2. 掉线问题
- 检查网络
- 调整超时
- 查看状态

## 贡献指南

1. Fork 项目
2. 创建分支 
3. 提交代码
4. 发起 PR

## 开发计划

- [ ] 新增游戏玩法
- [ ] 优化性能
- [ ] 完善文档
- [ ] 修复Bug

## 版本记录

### v1.0
- 基础功能完成
- 稳定性提升
- Bug修复


## 许可证

MIT License

## 免责声明

本项目仅供学习交流使用,请遵守当地法律法规。

---
