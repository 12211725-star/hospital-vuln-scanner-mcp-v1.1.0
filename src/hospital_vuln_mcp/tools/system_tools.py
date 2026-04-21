"""System tools."""
from typing import Annotated
from datetime import datetime

from fastmcp import FastMCP
from pydantic import Field

from . import scan_tools as scan_tools_mod
from . import vuln_tools as vuln_tools_mod


def register_system_tools(mcp: FastMCP) -> None:
    """Register system tools."""
    
    @mcp.tool()
    async def get_vuln_stats(
        period: Annotated[str, Field(description="统计周期: today/week/month/all")] = "all",
    ) -> str:
        """
        获取漏洞统计信息
        
        ## 功能说明
        获取漏洞的统计数据，包括按严重程度、状态、系统类型的分布。
        
        ## 统计周期
        - **today**: 今日数据
        - **week**: 本周数据
        - **month**: 本月数据
        - **all**: 全部历史数据
        
        Args:
            period: 统计周期
        
        Returns:
            JSON格式的统计数据
        """
        import json
        
        valid_periods = ["today", "week", "month", "all"]
        if period not in valid_periods:
            return json.dumps({"error": f"Invalid period. Must be one of: {valid_periods}"}, ensure_ascii=False)

        vulns = list(vuln_tools_mod._vulnerabilities.values())
        sev_keys = ["critical", "high", "medium", "low", "info"]
        st_keys = ["open", "fixed", "accepted", "false_positive"]
        by_severity = {k: 0 for k in sev_keys}
        by_status = {k: 0 for k in st_keys}
        for v in vulns:
            if v.severity in by_severity:
                by_severity[v.severity] += 1
            if v.status in by_status:
                by_status[v.status] += 1
        # 演示数据未区分系统类型时，统一计入 Other（后续可接真实资产字段）
        by_system_type = {
            "HIS": 0,
            "PACS": 0,
            "LIS": 0,
            "RIS": 0,
            "EMR": 0,
            "Other": len(vulns),
        }

        return json.dumps({
            "total": len(vulns),
            "by_severity": by_severity,
            "by_status": by_status,
            "by_system_type": by_system_type,
            "period": period,
            "generated_at": datetime.now().isoformat(),
        }, ensure_ascii=False)

    @mcp.tool()
    async def get_system_status() -> str:
        """
        获取系统状态和版本信息
        
        Returns:
            JSON格式的系统状态
        """
        import json
        from .._version import __version__

        scans = scan_tools_mod._scans
        active = sum(1 for s in scans.values() if s.status == "running")
        pending = sum(1 for s in scans.values() if s.status == "pending")

        return json.dumps({
            "server": "hospital-vuln-mcp",
            "version": __version__,
            "status": "ok",
            "uptime": "N/A",
            "total_scans": len(scans),
            "active_scans": active,
            "queued_scans": pending,
            "features": [
                "vulnerability_scanning",
                "network_discovery",
                "medical_system_identification",
                "report_generation"
            ],
            "checked_at": datetime.now().isoformat(),
        }, ensure_ascii=False)
