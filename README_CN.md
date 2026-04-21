# 医院漏洞扫描 MCP 服务器 🏥🔒

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Protocol-green.svg)](https://modelcontextprotocol.io/)

为 AI 助手提供医院/医疗系统安全扫描能力的 MCP 服务器。

## ✨ 功能特性

- 🔍 **漏洞扫描** - 全面的医疗系统漏洞检测
- 🌐 **网络发现** - 自动发现网络中的医疗设备和系统
- 📊 **报告生成** - 专业的安全扫描报告
- 🏥 **医疗系统识别** - 识别 HIS、PACS、RIS 等医疗系统
- 📈 **统计分析** - 漏洞统计和趋势分析

## 🚀 快速开始

### 安装

```bash
# 包已发布到 PyPI 后可用：
# uvx hospital-vuln-mcp
# pip install hospital-vuln-mcp

# 当前 PyPI 尚无本包，请从源码安装：
pip install -e .
python -m hospital_vuln_mcp
```

### 在 Claude Desktop 中使用

编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`（将 `cwd` 换成本机项目绝对路径）：

```json
{
  "mcpServers": {
    "hospital-vuln": {
      "command": "python",
      "args": ["-m", "hospital_vuln_mcp"],
      "cwd": "/你的绝对路径/hospital-vuln-mcp-v2"
    }
  }
}
```

### SSE 模式（本地）

```bash
hospital-vuln-mcp --transport sse --port 8000
```

默认绑定 `127.0.0.1`。容器或需公网反代时使用：

```bash
hospital-vuln-mcp --transport sse --host 0.0.0.0 --port 8000
```

### Streamable HTTP（与魔搭官方 MCP 文档中的 HTTP 传输同类）

```bash
hospital-vuln-mcp --transport http --port 8000
```

本服务基于当前 `mcp` 自带 FastMCP，Streamable HTTP 默认路径一般为 **`/mcp`**（请以运行日志或 MCP Inspector 为准）。SSE 默认路径一般为 **`GET /sse`**，消息 **`POST /messages/`**。

### 远程 SSE / HTTP（魔搭「托管 / 公网」类场景）

若平台要求提供 **StreamableHTTP** 或 **SSE** 的公网地址，你需要：

1. 将服务以 `--host 0.0.0.0` 暴露端口（Docker 镜像默认已如此）。
2. 在具备合法备案与 TLS 的域名上配置 **HTTPS 反向代理**（如 Nginx/Caddy），转发到容器内 `8000`。
3. 在魔搭 MCP 配置中填写对外 URL（示例：`https://your-domain.com/sse` 或 `https://your-domain.com/mcp`，须与实际路径一致）。

### Cursor / VS Code（URL 连接远程 MCP 时）

在 `~/.cursor/mcp.json` 或工作区 `.vscode/mcp.json` 中可使用（将 URL 换成你的公网地址）：

```json
{
  "mcpServers": {
    "hospital-vuln-remote": {
      "url": "https://YOUR_PUBLIC_HOST/sse"
    }
  }
}
```

---

## 📤 魔搭 MCP 广场上架检查（上传失败时逐项核对）

对照魔搭当前常见要求，建议按下表自检：

| 要求 | 说明 | 本项目状态 |
|------|------|--------------|
| 完成 MCP 代码 | 工具/资源/提示词可用 | 已实现（14 工具 + 3 资源 + 4 提示词） |
| **PyPI** | 使用 `uvx hospital-vuln-mcp` 时包须在 PyPI 可查 | **已检测**：`https://pypi.org/pypi/hospital-vuln-mcp/json` 返回 **404**，包尚未发布；`mcp_config.json` 与 `modelscope.yaml` 已改为 **`python -m hospital_vuln_mcp`**。发布 PyPI 后可再改回 `uvx` |
| GitHub | `repository` / `homepage` 可访问 | 已改为当前仓库：`https://github.com/12211725-star/hospital-vuln-scanner-mcp-v1.1.0` |
| **STDIO 配置** | 提供可执行的 `command` + `args` | `mcp_config.json` 为 **`python` + `-m hospital_vuln_mcp`**（与魔搭从仓库构建安装后的运行方式一致） |
| SSE / StreamableHTTP（可选） | 若声明远程类型，需 **公网 HTTPS** 与可达路径 | 需自行部署；见上文「远程 SSE / HTTP」 |
| 使用指引 | README + 客户端示例 | 见本文与 `README.md` |

**仍上传失败时（第 3 步）**：请到 [GitHub Issues](https://github.com/12211725-star/hospital-vuln-scanner-mcp-v1.1.0/issues) 新建工单，并粘贴魔搭返回的**完整错误原文**（或含错误码、请求 ID 的截图说明），便于对照平台校验规则排查。

**本地 Claude / Cursor 客户端示例**（与 `mcp_config.json` 一致，需已 `pip install -e .` 且 `python` 能找到包）：

```json
{
  "mcpServers": {
    "hospital-vuln": {
      "command": "python",
      "args": ["-m", "hospital_vuln_mcp"],
      "cwd": "/你的绝对路径/hospital-vuln-mcp-v2"
    }
  }
}
```

## 🛠️ 工具列表

### 扫描管理
| 工具 | 描述 |
|------|------|
| `start_scan` | 启动漏洞扫描任务 |
| `get_scan_status` | 查询扫描状态和结果 |
| `list_scans` | 列出扫描任务历史 |
| `cancel_scan` | 取消正在进行的扫描 |

### 漏洞管理
| 工具 | 描述 |
|------|------|
| `list_vulnerabilities` | 列出发现的漏洞 |
| `get_vulnerability` | 获取漏洞详细信息 |
| `update_vulnerability_status` | 更新漏洞处理状态 |
| `get_vuln_stats` | 漏洞统计信息 |

### 网络工具
| 工具 | 描述 |
|------|------|
| `discover_network` | 网络发现和设备识别 |
| `scan_host_ports` | 主机端口扫描 |
| `identify_medical_systems` | 识别医疗系统类型 |

### 报告工具
| 工具 | 描述 |
|------|------|
| `generate_report` | 生成扫描报告 |
| `list_reports` | 列出历史报告 |
| `get_system_status` | 获取系统整体状态 |

## 💡 使用示例

### 示例 1: 扫描医院内网

```
请帮我扫描医院 192.168.10.0/24 网段的设备漏洞
```

AI 助手将执行：
1. `discover_network` - 发现网络设备
2. `identify_medical_systems` - 识别医疗系统
3. `start_scan` - 对发现的系统进行漏洞扫描
4. `generate_report` - 生成安全报告

### 示例 2: 查看漏洞统计

```
查看本月发现的严重漏洞
```

AI 助手将执行：
1. `get_vuln_stats` - 获取统计数据
2. `list_vulnerabilities` - 列出严重漏洞

### 示例 3: 端口扫描

```
扫描 192.168.1.100 的开放端口
```

AI 助手将执行：
1. `scan_host_ports` - 端口扫描
2. `identify_medical_systems` - 识别系统类型

## 📁 项目结构

```
hospital-vuln-mcp/
├── src/
│   └── hospital_vuln_mcp/
│       ├── __init__.py
│       ├── server.py       # MCP 服务器实现
│       ├── cli.py          # 命令行接口
│       ├── settings.py     # 配置管理
│       └── _version.py     # 版本信息
├── pyproject.toml          # Python 项目配置
├── README.md               # 英文文档
├── README_CN.md            # 中文文档
├── LICENSE                 # MIT 许可证
└── .gitignore             # Git 忽略配置
```

## 🔧 开发

```bash
# 克隆仓库
git clone https://github.com/12211725-star/hospital-vuln-scanner-mcp-v1.1.0.git
cd hospital-vuln-scanner-mcp-v1.1.0

# 安装依赖
pip install -e ".[dev]"

# 运行开发服务器
python -m hospital_vuln_mcp --transport stdio
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系我们

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 发送邮件至: security@example.com

---

**注意**: 本工具仅用于授权的安全测试和漏洞评估，请勿用于非法用途。
