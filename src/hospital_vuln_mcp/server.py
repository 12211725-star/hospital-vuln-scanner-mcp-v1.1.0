"""
Hospital Vulnerability Scanner MCP Server

基于魔搭 MCP 开发规范实现，提供医疗系统安全扫描能力。
"""
from typing import Any

from mcp.server.fastmcp import FastMCP

from ._version import __version__
from .tools import (
    register_scan_tools,
    register_vuln_tools,
    register_network_tools,
    register_report_tools,
    register_system_tools,
)
from .resources import register_resources
from .prompts import register_prompts


def create_server(
    *,
    host: str | None = None,
    port: int | None = None,
) -> FastMCP:
    """
    创建并配置 MCP 服务器。

    Args:
        host: SSE / Streamable HTTP 监听地址（默认由 FastMCP 决定，一般为 127.0.0.1）
        port: SSE / Streamable HTTP 监听端口（默认 8000）

    Returns:
        配置好的 FastMCP 实例
    """
    bind: dict[str, Any] = {}
    if host is not None:
        bind["host"] = host
    if port is not None:
        bind["port"] = port

    mcp = FastMCP(
        name="hospital-vuln-mcp",
        instructions="""
医院漏洞扫描MCP服务器 — 为 AI 助手提供医疗系统安全扫描能力。

医院漏洞扫描MCP服务器使用说明：

本服务提供14个工具用于医疗系统安全扫描：

【扫描管理】
- start_scan: 启动漏洞扫描（支持quick/standard/deep三种模式）
- get_scan_status: 查询扫描状态和结果
- list_scans: 列出历史扫描任务
- cancel_scan: 取消正在进行的扫描

【漏洞管理】
- list_vulnerabilities: 列出发现的漏洞（支持按严重程度和状态筛选）
- get_vulnerability: 获取漏洞详细信息
- update_vulnerability_status: 更新漏洞处理状态

【网络工具】
- discover_network: 网络发现和医疗系统识别
- scan_host_ports: 端口扫描
- identify_medical_systems: 识别HIS/PACS/LIS/RIS等医疗系统

【报告工具】
- generate_report: 生成扫描报告（PDF/HTML/JSON/CSV）
- list_reports: 列出历史报告

【系统工具】
- get_vuln_stats: 漏洞统计分析
- get_system_status: 获取系统状态

【资源】
- config://app-info: 应用信息
- config://scan-profiles: 扫描配置说明
- docs://severity-levels: 严重程度分级

【提示词模板】
- vulnerability_analysis: 漏洞分析报告
- scan_planning: 扫描规划
- compliance_check: 合规性检查
- executive_summary: 管理层摘要
        """,
        **bind,
    )

    # 注册工具
    register_scan_tools(mcp)
    register_vuln_tools(mcp)
    register_network_tools(mcp)
    register_report_tools(mcp)
    register_system_tools(mcp)
    
    # 注册资源
    register_resources(mcp)
    
    # 注册提示词模板
    register_prompts(mcp)

    return mcp


if __name__ == "__main__":
    from .cli import main as cli_main

    cli_main()
