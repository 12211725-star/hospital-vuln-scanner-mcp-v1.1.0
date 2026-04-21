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
# 使用 uvx（推荐）
uvx hospital-vuln-mcp

# 或使用 pip
pip install hospital-vuln-mcp
```

### 在 Claude Desktop 中使用

编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hospital-vuln": {
      "command": "uvx",
      "args": ["hospital-vuln-mcp"]
    }
  }
}
```

### SSE 模式

```bash
hospital-vuln-mcp --transport sse --port 8000
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
git clone https://github.com/yourusername/hospital-vuln-mcp.git
cd hospital-vuln-mcp

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
