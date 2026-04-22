# Hospital Vulnerability Scanner MCP Server

[![PyPI Version](https://img.shields.io/pypi/v/hospital-vuln-mcp.svg)](https://pypi.org/project/hospital-vuln-mcp)
[![Python](https://img.shields.io/pypi/pyversions/hospital-vuln-mcp.svg)](https://pypi.org/project/hospital-vuln-mcp)
[![License](https://img.shields.io/github/license/12211725-star/hospital-vuln-mcp.svg)](https://github.com/12211725-star/hospital-vuln-mcp/blob/main/LICENSE)

English | [中文](README_CN.md)

医院漏洞扫描 MCP 服务器，为 AI 助手提供医疗信息系统**真实安全扫描**能力。支持端口扫描、漏洞检测、医疗系统识别、合规报告生成等 14 个工具。

## ✨ 功能特性

- 🔍 **真实漏洞扫描** — 支持 quick/standard/deep 三种模式，自动调用 nmap/nuclei 或 Python 回退
- 🏥 **医疗系统识别** — 自动识别 HIS/PACS/LIS/RIS/EMR 等医疗信息系统
- 🌐 **网络发现** — 网络资产发现和端口扫描
- 📊 **报告生成** — 支持 PDF/HTML/JSON/CSV 格式报告
- 🔐 **合规检查** — 符合等保 2.0 要求
- ⚡ **零依赖运行** — 无需安装 nmap/nuclei，Python 原生扫描也能用

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
      "args": ["hospital-vuln-mcp"],
      "env": {
        "HOSPITAL_VULN_MCP_LOG_LEVEL": "INFO"
      }
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
      "args": ["run", "--rm", "-i", "hospital-vuln-mcp"],
      "env": {
        "HOSPITAL_VULN_MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Streamable HTTP 远程部署

```bash
hospital-vuln-mcp --transport http --host 0.0.0.0 --port 8000
```

### 3. 可选：安装扫描引擎增强

```bash
# 安装 nmap（端口扫描增强）
# macOS
brew install nmap

# Ubuntu/Debian
sudo apt install nmap

# Windows
choco install nmap

# 安装 nuclei（漏洞扫描增强）
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

> 💡 **提示**：不安装也能用，会自动降级到 Python 原生扫描。

## 📖 使用方法

### 基础扫描

在 Claude / Cursor / 其他 MCP 客户端中：

```
请帮我扫描 192.168.1.100 这台服务器
```

AI 会调用 `start_scan` 工具，返回：

```json
{
  "task_id": "abc123",
  "status": "completed",
  "open_ports": [
    {"port": 22, "service": "SSH"},
    {"port": 3306, "service": "MySQL"},
    {"port": 8080, "service": "HTTP-Alt"}
  ],
  "vulnerabilities": [
    {"title": "MySQL 服务暴露", "severity": "medium"}
  ]
}
```

### 指定扫描类型

```
对 10.0.0.50 进行深度扫描
```

```
快速扫描 www.example.com
```

### 端口扫描

```
扫描 192.168.1.1 的 22,80,443,3306 端口
```

### 医疗系统识别

```
识别 192.168.1.100 运行的医疗系统类型
```

### 网络发现

```
发现 192.168.1.0/24 网段的活跃主机
```

## 🎯 提示词指南

### 安全评估场景

```
我需要对一台新上线的 HIS 系统进行安全评估，
目标 IP 是 192.168.1.200，请帮我进行标准扫描并生成报告。
```

### 定期巡检场景

```
请帮我巡检内网 10.0.0.0/24 网段的医疗系统安全状况。
```

### 合规检查场景

```
我需要为等保测评准备安全扫描报告，
请对目标系统进行深度扫描并导出合规报告。
```

### 应急响应场景

```
发现 192.168.1.50 可能有安全风险，
请立即进行快速扫描帮我排查问题。
```

### 资产盘点场景

```
帮我盘点医院网络中的所有医疗信息系统，
识别系统类型和开放端口。
```

## 🛠️ 工具列表

### 扫描管理

| 工具 | 描述 | 参数 |
|------|------|------|
| `start_scan` | 启动漏洞扫描 | `target`: IP/域名/URL, `scan_type`: quick/standard/deep |
| `get_scan_status` | 查询扫描状态 | `task_id`: 任务ID |
| `list_scans` | 列出扫描历史 | `limit`: 数量, `status`: 状态筛选 |
| `cancel_scan` | 取消扫描 | `task_id`: 任务ID |

### 漏洞管理

| 工具 | 描述 | 参数 |
|------|------|------|
| `list_vulnerabilities` | 列出漏洞 | `severity`: 严重程度, `status`: 状态 |
| `get_vulnerability` | 获取漏洞详情 | `vuln_id`: 漏洞ID |
| `update_vulnerability_status` | 更新漏洞状态 | `vuln_id`, `status`, `comment` |

### 网络工具

| 工具 | 描述 | 参数 |
|------|------|------|
| `discover_network` | 网络发现 | `cidr`: 网段 |
| `scan_host_ports` | 端口扫描 | `host`: 主机, `ports`: 端口列表（可选） |
| `identify_medical_systems` | 医疗系统识别 | `target`: 目标, `ports`: 端口列表（可选） |

### 报告工具

| 工具 | 描述 | 参数 |
|------|------|------|
| `generate_report` | 生成报告 | `scan_id`, `report_type`, `format` |
| `list_reports` | 列出报告 | `limit`: 数量 |

### 系统工具

| 工具 | 描述 |
|------|------|
| `get_vuln_stats` | 漏洞统计分析 |
| `get_system_status` | 系统状态（含 nmap/nuclei 可用性） |

## ⚙️ 扫描引擎

### 自动检测机制

```
start_scan()
    │
    ├── 检测 nmap → 有则用于端口扫描
    │   └── 无 → Python socket 多线程扫描
    │
    ├── 检测 nuclei → 有则用于漏洞扫描
    │   └── 无 → 内置规则检测常见漏洞
    │
    └── 返回结果
```

### 内置漏洞检测规则

即使没有 nuclei，也能检测以下常见风险：

| 风险类型 | 严重程度 | 检测条件 |
|---------|---------|---------|
| MySQL 服务暴露 | Medium | 3306 端口开放 |
| Redis 未授权访问 | High | 6379 端口开放 |
| MongoDB 未授权访问 | High | 27017 端口开放 |
| RDP 远程桌面暴露 | High | 3389 端口开放 |
| SMBv1 协议风险 | High | 445 端口开放 |
| PHPInfo 信息泄露 | Medium | HTTP 响应含 phpinfo |
| 目录遍历风险 | Medium | HTTP 响应含 "Index of" |

### 医疗系统指纹识别

通过 HTTP Banner 和页面特征识别：

| 系统类型 | 关键词 |
|---------|--------|
| HIS | 医院信息系统、门诊、住院、挂号、处方 |
| PACS | 影像、DICOM、放射、PACS |
| LIS | 检验、实验室、生化、免疫 |
| RIS | 放射信息系统、影像诊断 |
| EMR | 电子病历、病程记录 |

## 📖 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `HOSPITAL_VULN_MCP_LOG_LEVEL` | 日志级别 | `INFO` |
| `HOSPITAL_VULN_MCP_SCAN_TIMEOUT` | 扫描超时（秒） | `300` |
| `HOSPITAL_VULN_MCP_MAX_CONCURRENT_SCANS` | 最大并发扫描数 | `10` |

## 🔧 开发

```bash
git clone https://github.com/12211725-star/hospital-vuln-mcp.git
cd hospital-vuln-mcp
pip install -e ".[dev]"

# 运行测试
pytest

# 本地运行
python -m hospital_vuln_mcp
```

## 📋 更新日志

### v1.1.1 (2026-04-22)

- 📝 更新 README，添加使用方法和提示词指南
- 📝 添加扫描引擎说明和内置规则文档
- 📝 添加医疗系统指纹识别说明

### v1.1.0 (2026-04-21)

- ✨ 新增真实扫描能力（nmap/nuclei 自动检测）
- ✨ 新增 Python 原生端口扫描回退
- ✨ 新增医疗系统指纹识别
- ✨ 新增内置漏洞检测规则
- 🐛 修复扫描任务永远卡在 running 的问题

### v1.0.0 (2026-04-21)

- 🎉 初始版本
- ✨ 14 个 MCP 工具
- ✨ 魔搭 MCP 广场上架

## 📄 许可证

MIT License

## 🔗 链接

- **GitHub**: https://github.com/12211725-star/hospital-vuln-mcp
- **Issues**: https://github.com/12211725-star/hospital-vuln-mcp/issues
- **PyPI**: https://pypi.org/project/hospital-vuln-mcp/
- **魔搭 MCP 广场**: https://modelscope.cn/mcp/servers
