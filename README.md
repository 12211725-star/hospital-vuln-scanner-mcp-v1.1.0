# Hospital Vulnerability Scanner MCP Server

[![PyPI Version](https://img.shields.io/pypi/v/hospital-vuln-mcp.svg)](https://pypi.org/project/hospital-vuln-mcp)
[![License](https://img.shields.io/github/license/12211725-star/hospital-vuln-scanner-mcp-v1.1.0.svg)](https://github.com/12211725-star/hospital-vuln-scanner-mcp-v1.1.0/blob/main/LICENSE)

English | [中文](README_CN.md)

医院漏洞扫描 MCP 服务器，为 AI 助手提供医疗信息系统安全扫描能力。支持漏洞扫描、网络发现、医疗系统识别、合规报告生成等 14 个工具。

## ✨ 功能特性

- 🔍 **漏洞扫描** — 支持 quick/standard/deep 三种扫描模式
- 🏥 **医疗系统识别** — 自动识别 HIS/PACS/LIS/RIS 等医疗信息系统
- 🌐 **网络发现** — 网络资产发现和端口扫描
- 📊 **报告生成** — 支持 PDF/HTML/JSON/CSV 格式报告
- 🔐 **合规检查** — 符合等保 2.0 要求

## 🚀 快速开始

### 1. 安装

```bash
# 使用 uvx（推荐）
uvx hospital-vuln-mcp

# 或使用 pip
pip install hospital-vuln-mcp
```

### 2. 集成到 MCP 客户端

在 MCP 客户端配置文件中添加：

```json
{
  "mcpServers": {
    "hospital-vuln-mcp": {
      "command": "uvx",
      "args": ["hospital-vuln-mcp"]
    }
  }
}
```

### Docker 方式

```json
{
  "mcpServers": {
    "hospital-vuln-mcp": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "ghcr.io/12211725-star/hospital-vuln-mcp:latest"
      ]
    }
  }
}
```

### SSE / HTTP 远程部署

```bash
# SSE 模式
hospital-vuln-mcp --transport sse --port 8000

# Streamable HTTP 模式
hospital-vuln-mcp --transport http --port 8000
```

远程客户端配置：

```json
{
  "mcpServers": {
    "hospital-vuln-mcp": {
      "url": "http://127.0.0.1:8000/mcp/"
    }
  }
}
```

## 🛠️ 工具列表

### 扫描管理

| 工具 | 描述 |
|------|------|
| `start_scan` | 启动漏洞扫描，支持 quick/standard/deep 模式 |
| `get_scan_status` | 查询扫描任务状态和结果 |
| `list_scans` | 列出所有扫描任务 |
| `cancel_scan` | 取消正在进行的扫描 |

### 漏洞管理

| 工具 | 描述 |
|------|------|
| `list_vulnerabilities` | 列出漏洞，支持按严重程度和状态筛选 |
| `get_vulnerability` | 获取漏洞详细信息 |
| `update_vulnerability_status` | 更新漏洞处理状态 |

### 网络工具

| 工具 | 描述 |
|------|------|
| `discover_network` | 网络资产发现 |
| `scan_host_ports` | 端口扫描 |
| `identify_medical_systems` | 识别医疗信息系统类型 |

### 报告工具

| 工具 | 描述 |
|------|------|
| `generate_report` | 生成扫描报告（PDF/HTML/JSON/CSV） |
| `list_reports` | 列出历史报告 |

### 系统工具

| 工具 | 描述 |
|------|------|
| `get_vuln_stats` | 漏洞统计分析 |
| `get_system_status` | 获取系统运行状态 |

## 📖 配置说明

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `HOSPITAL_VULN_LOG_LEVEL` | 日志级别 | `INFO` |
| `HOSPITAL_VULN_DB_PATH` | 数据库路径 | `./data/vulns.db` |

### 传输模式

| 模式 | 用途 | 端点 |
|------|------|------|
| `stdio` | 本地桌面集成（默认） | 标准输入输出 |
| `sse` | Web 远程访问 | `GET /sse` + `POST /messages/` |
| `http` | Streamable HTTP（推荐） | `POST /mcp/` |

## 🔧 开发

```bash
# 克隆仓库
git clone https://github.com/12211725-star/hospital-vuln-scanner-mcp-v1.1.0.git
cd hospital-vuln-scanner-mcp-v1.1.0

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 本地运行
python -m hospital_vuln_mcp
```

## 📄 许可证

MIT License

## 🔗 链接

- **GitHub**: https://github.com/12211725-star/hospital-vuln-scanner-mcp-v1.1.0
- **Issues**: https://github.com/12211725-star/hospital-vuln-scanner-mcp-v1.1.0/issues
- **PyPI**: https://pypi.org/project/hospital-vuln-mcp/
