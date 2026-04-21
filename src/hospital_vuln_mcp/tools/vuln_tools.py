"""Vulnerability management tools."""
from typing import Annotated, Optional
from datetime import datetime

from fastmcp import FastMCP
from pydantic import Field

from ..models import Vulnerability


# In-memory storage
_vulnerabilities: dict[str, Vulnerability] = {}


def register_vuln_tools(mcp: FastMCP) -> None:
    """Register vulnerability management tools."""
    
    @mcp.tool()
    async def list_vulnerabilities(
        severity: Annotated[Optional[str], Field(description="严重程度筛选: critical/high/medium/low/info")] = None,
        status: Annotated[Optional[str], Field(description="状态筛选: open/fixed/accepted/false_positive")] = None,
        limit: Annotated[int, Field(description="返回结果数量限制，默认50")] = 50,
    ) -> str:
        """
        列出发现的漏洞
        
        ## 功能说明
        获取漏洞列表，支持按严重程度和状态筛选。
        
        Args:
            severity: 严重程度筛选
            status: 状态筛选
            limit: 返回数量限制
        
        Returns:
            JSON格式的漏洞列表
        """
        import json
        
        vulns = list(_vulnerabilities.values())
        
        if severity:
            vulns = [v for v in vulns if v.severity == severity]
        if status:
            vulns = [v for v in vulns if v.status == status]
        
        return json.dumps({
            "total": len(vulns),
            "vulnerabilities": [v.model_dump() for v in vulns[:limit]]
        }, ensure_ascii=False, default=str)

    @mcp.tool()
    async def get_vulnerability(
        vuln_id: Annotated[str, Field(description="漏洞ID")],
    ) -> str:
        """
        获取漏洞详细信息
        
        Args:
            vuln_id: 漏洞ID
        
        Returns:
            JSON格式的漏洞详情
        """
        import json
        
        if vuln_id not in _vulnerabilities:
            return json.dumps({"error": "Vulnerability not found", "vuln_id": vuln_id}, ensure_ascii=False)
        
        return json.dumps(_vulnerabilities[vuln_id].model_dump(), ensure_ascii=False, default=str)

    @mcp.tool()
    async def update_vulnerability_status(
        vuln_id: Annotated[str, Field(description="漏洞ID")],
        status: Annotated[str, Field(description="新状态: open/fixed/accepted/false_positive")],
        comment: Annotated[str, Field(description="备注说明")] = "",
    ) -> str:
        """
        更新漏洞处理状态
        
        ## 功能说明
        更新漏洞的处理状态，用于漏洞修复跟踪。
        
        ## 状态说明
        - **open**: 未修复
        - **fixed**: 已修复
        - **accepted**: 已接受风险
        - **false_positive**: 误报
        
        Args:
            vuln_id: 漏洞ID
            status: 新状态
            comment: 备注说明
        
        Returns:
            JSON格式的更新结果
        """
        import json
        
        if vuln_id not in _vulnerabilities:
            return json.dumps({"error": "Vulnerability not found"}, ensure_ascii=False)
        
        valid_status = ["open", "fixed", "accepted", "false_positive"]
        if status not in valid_status:
            return json.dumps({"error": f"Invalid status. Must be one of: {valid_status}"}, ensure_ascii=False)
        
        vuln = _vulnerabilities[vuln_id]
        vuln.status = status
        if status == "fixed":
            vuln.fixed_at = datetime.now().isoformat()
        
        return json.dumps({
            "vuln_id": vuln_id,
            "status": status,
            "comment": comment,
            "updated_at": datetime.now().isoformat(),
            "message": "漏洞状态已更新"
        }, ensure_ascii=False)
