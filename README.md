# YouTube 视频下载器

一个简单的 YouTube 视频下载工具，支持：
- 视频和音频下载
- 多种格式选择
- 字幕下载
- 批量下载
- 下载历史记录

## 部署

1. 克隆仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 设置环境变量
4. 运行：`uvicorn main:app --reload`

## 环境变量

- `DOWNLOAD_DIR`: 下载目录
- `PROXY`: 代理服务器（可选）
- `SECRET_KEY`: 安全密钥
- `API_KEY`: API访问密钥 