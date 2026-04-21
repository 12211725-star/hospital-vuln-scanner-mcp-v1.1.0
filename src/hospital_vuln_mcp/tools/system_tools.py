"""System status tools."""
import json
import platform
import sys
from datetime import datetime
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from .._version import __version__
from ..scanner import NMAP_AVAILABLE, NUCLEI_AVAILABLE
from ..tools.scan_tools import _scans, _scan_results
from ..tools.vuln_tools import _vulnerabilities
from ..tools.report_tools import _reports


def register_system_tools(mcp: FastMCP) -> None:
    """Register system status tools."""

    @mcp.tool()
    async def get_vuln_stats(
        period: Annotated[str, Field(description="统计周期：today/week/month/all")] = "all",
    ) -> str:
        """
        漏洞统计分析

        ## 功能说明
        统计漏洞数量、按严重程度和状态分布。

        Args:
            period: 统计周期

        Returns:
            JSON格式的漏洞统计信息
        """
        vulns = list(_vulnerabilities.values())

        by_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        by_status = {"open": 0, "fixed": 0, "accepted": 0, "false_positive": 0}

        for v in vulns:
            by_severity[v.severity] = by_severity.get(v.severity, 0) + 1
            by_status[v.status] = by_status.get(v.status, 0) + 1

        return json.dumps({
            "total": len(vulns),
            "by_severity": by_severity,
            "by_status": by_status,
            "total_scans": len(_scans),
            "completed_scans": len([s for s in _scans.values() if s.status == "completed"]),
            "total_reports": len(_reports),
            "period": period,
        }, ensure_ascii=False, default=str)

    @mcp.tool()
    async def get_system_status() -> str:
        """
        获取系统运行状态和扫描引擎信息

        ## 功能说明
        返回 MCP 服务器状态、扫描引擎可用性和运行环境信息。

        Returns:
            JSON格式的系统状态
        """
        active_scans = len([s for s in _scans.values() if s.status == "running"])
        queued_scans = len([s for s in _scans.values() if s.status == "pending"])

        return json.dumps({
            "server": "hospital-vuln-mcp",
            "version": __version__,
            "status": "ok",
            "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform": platform.system(),
            "machine": platform.machine(),
            "scan_engines": {
                "nmap": {"available": NMAP_AVAILABLE, "status": "✅ 已安装" if NMAP_AVAILABLE else "❌ 未安装（将使用 socket 回退）"},
                "nuclei": {"available": NUCLEI_AVAILABLE, "status": "✅ 已安装" if NUCLEI_AVAILABLE else "❌ 未安装（将使用内置规则回退）"},
            },
            "scan_stats": {
                "total_scans": len(_scans),
                "active_scans": active_scans,
                "queued_scans": queued_scans,
                "completed_scans": len([s for s in _scans.values() if s.status == "completed"]),
                "failed_scans": len([s for s in _scans.values() if s.status == "failed"]),
            },
            "vuln_stats": {
                "total_vulnerabilities": len(_vulnerabilities),
                "total_reports": len(_reports),
            },
            "tip": "安装 nmap 和 nuclei 可获得更强大的扫描能力" if not (NMAP_AVAILABLE and NUCLEI_AVAILABLE) else "所有扫描引擎已就绪",
        }, ensure_ascii=False, default=str)
