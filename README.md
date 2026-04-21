# Hospital Vulnerability Scanner MCP Server

医院漏洞扫描 MCP 服务器，为 AI 助手提供安全扫描能力。

## 安装

```bash
# After publishing to PyPI:
uvx hospital-vuln-mcp
# or:
pip install hospital-vuln-mcp
```

As of last check, `hospital-vuln-mcp` is **not** on PyPI (404). Use a local / ModelScope-built install:

```bash
pip install -e .
python -m hospital_vuln_mcp
```

## 使用

### Claude Desktop

```json
{
  "mcpServers": {
    "hospital-vuln": {
      "command": "python",
      "args": ["-m", "hospital_vuln_mcp"],
      "cwd": "/absolute/path/to/hospital-vuln-mcp-v2"
    }
  }
}
```

After the package is published to PyPI, you can switch back to `uvx` / `pip install hospital-vuln-mcp` without `cwd`.

### SSE (local)

```bash
hospital-vuln-mcp --transport sse --port 8000
```

Bind address defaults to `127.0.0.1`. For Docker or public reverse proxy:

```bash
hospital-vuln-mcp --transport sse --host 0.0.0.0 --port 8000
```

### Streamable HTTP

```bash
hospital-vuln-mcp --transport http --port 8000
```

With the bundled FastMCP, Streamable HTTP is typically served under **`/mcp`**. SSE is usually **`GET /sse`** with messages under **`POST /messages/`** (confirm with logs or MCP Inspector).

### ModelScope / hosted SSE or HTTP

If the marketplace requires a **public HTTPS** endpoint: run the server with `--host 0.0.0.0`, put TLS termination on Nginx/Caddy, and register the external URL (for example `https://your-domain.com/sse` or `https://your-domain.com/mcp`).

### Cursor / VS Code (remote URL)

```json
{
  "mcpServers": {
    "hospital-vuln-remote": {
      "url": "https://YOUR_PUBLIC_HOST/sse"
    }
  }
}
```

### Upload checklist (when submission fails)

| Item | Notes |
|------|--------|
| **PyPI** | Verified: project JSON on PyPI returns **404** (not published). `mcp_config.json` and `modelscope.yaml` now use **`python -m hospital_vuln_mcp`**. After publishing, you may switch back to `uvx`. |
| **GitHub URLs** | `homepage` / `repository` point to `https://github.com/12211725-star/hospital-vuln-scanner-mcp-v1.1.0`. |
| **STDIO** | `mcp_config.json` uses `command` + `args` for `python -m hospital_vuln_mcp`. |
| **Remote transports** | Provide a reachable **HTTPS** URL if you advertise SSE/HTTP. |
| **Still failing** | Open an [Issue](https://github.com/12211725-star/hospital-vuln-scanner-mcp-v1.1.0/issues) and paste the full ModelScope error text. |

## 工具列表

| 工具 | 描述 |
|------|------|
| start_scan | 启动漏洞扫描 |
| get_scan_status | 查询扫描状态 |
| list_scans | 列出扫描任务 |
| cancel_scan | 取消扫描 |
| list_vulnerabilities | 列出漏洞 |
| get_vulnerability | 漏洞详情 |
| update_vulnerability_status | 更新漏洞状态 |
| discover_network | 网络发现 |
| scan_host_ports | 端口扫描 |
| identify_medical_systems | 医疗系统识别 |
| generate_report | 生成报告 |
| list_reports | 列出报告 |
| get_vuln_stats | 漏洞统计 |
| get_system_status | 系统状态 |

## License

MIT