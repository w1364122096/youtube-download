# 更新日志

## [1.2.1] - 2024-03-21

### 修复
- 添加了 SQLAlchemy 依赖检查
- 改进了数据库初始化
- 添加了错误处理和日志

### 改进
- 数据库文件移至 data 目录
- 添加了数据库状态日志

## [1.2.0] - 2024-03-21

### 新增功能
- 视频管理系统
  - 视频重命名
  - 标签管理
  - 搜索和筛选
  - 排序功能
- 下载历史记录
  - 操作历史
  - 时间记录
  - 详细信息
- 数据持久化
  - SQLite 数据库支持
  - 视频元数据存储
  - 标签系统

### 改进
- 优化了界面布局
- 添加了分页支持
- 改进了视频信息显示
- 添加了标签筛选

## [1.1.2] - 2024-03-21

### 优化
- 提升下载速度
  - 启用并行下载
  - 优化缓冲区大小
  - 优化分片大小
  - 添加重试机制
- 改进格式选择
  - 优化视频编码选择
  - 优化音频质量
- 添加下载信息保存

### 改进
- 添加音频下载支持
- 优化错误处理
- 改进重试机制

## [1.1.1] - 2024-03-21

### 修复
- 修复了下载目录初始化问题
- 实现了下载按钮功能
- 添加了下载进度显示

### 改进
- 优化了错误处理
- 添加了下载完成提示

## [1.1.0] - 2024-03-21

### 新增功能
- 已下载视频管理功能
  - 视频列表显示
  - 本地下载功能
  - 删除视频功能
- 下载度显示
  - 实时进度条
  - 下载速度显示
  - 剩余时间显示
- 自动刷新下载列表

### 改进
- 优化了界面布局
- 添加了文件大小显示
- 添加了下载时间记录

## [1.0.0] - 2024-03-21

### 初始功能
- 基本的视频下载功能
- 视频格式选择
- 字幕下载支持
- 批量下载支持
- 备份管理系统

## [1.2.2] - 2024-03-21

### 新增
- 添加英文语言支持
- 添加中文语言支持
- 完整的翻译文件

### 改进
- 所有界面文本支持国际化
- 改进了文本组织结构

## [1.2.3] - 2024-03-21

### 优化
- 改进长视频下载
  - 使用 aria2 下载器
  - 优化分片下载
  - 增加并行下载数
  - 智能重试机制
- 网络优化
  - 增加超时时间
  - 优化重试策略
  - 改进缓冲设置

## [1.2.4] - 2024-03-21

### 新增
- 添加打开下载文件夹功能
  - 下载完成后可直接打开文件夹
  - 支持 Windows/macOS/Linux
  - 添加文件夹图标按钮

### 改进
- 优化下载完成提示
- 改进用户体验

## [1.2.5] - 2024-03-21

### 改进
- 优化界面布局
  - 移动打开文件夹按钮到已下载视频标题旁
  - 简化下载完成提示
  - 改进按钮文本和图标

### 修复
- 修复了一些文本编码问题
- 改进了错误处理

## [1.2.6] - 2024-03-21

### 改进
- 添加 ffmpeg 检查
- 优化错误处理
  - 添加友好的错误提示
  - 改进错误恢复机制
- 改进下载配置
  - 添加错误容忍
  - 优化合并设置

## [1.2.7] - 2024-03-21

### 改进
- 优化视频下载
  - 改进格式选择逻辑
  - 优先选择 MP4 格式
  - 简化格式处理
- 改进错误处理
  - 优化错误提示
  - 改进错误恢复
- 界面优化
  - 改进文本显示
  - 修复编码问题

## [1.2.10] - 2024-03-21

### 改进
- 优化下载功能
  - 简化下载配置
  - 移除高级选项
  - 提升稳定性
- 界面优化
  - 改进布局
  - 修复编码问题
  - 优化用户体验
- 错误处理
  - 优化错误提示
  - 改进错误恢复

## [1.2.9] - 2024-03-21

### 改进
- 优化下载功能

## [1.2.11] - 2024-03-21

### 改进
- 优化下载功能
  - 修复 SSL 证书问题
  - 改进网络连接设置
  - 添加重试机制
- 错误处理
  - 优化错误提示
  - 添加超时设置
- 网络优化
  - 添加自定义 User-Agent
  - 优化代理设置
- 新增功能
  - 添加打开下载文件夹功能
  - 添加 FFmpeg 检查功能
  - 改进错误处理机制
  - 添加视频信息缓存
  - 添加下载进度回调
  - 添加下载队列管理
  - 添加队列状态查询

## [1.2.12] - 2024-03-21

### 改进
- 优化下载功能
  - 移除 FFmpeg 依赖
  - 简化下载配置
  - 使用单一格式下载
- 错误处理
  - 优化错误提示
  - 改进错误恢复
- 网络优化
  - 优化 SSL 证书处理
  - 改进网络连接设置

## [1.2.13] - 2024-03-21

### 改进
- 优化下载功能
  - 移除下载队列限制
  - 自动清理已完成任务
  - 改进进度显示
- 用户体验
  - 优化状态提示
  - 改进下载流程
  - 修复编码问题