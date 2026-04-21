"""Report generation tools."""
from typing import Annotated
from datetime import datetime

from fastmcp import FastMCP
from pydantic import Field

from ..models import Report


# In-memory storage
_reports: dict[str, Report] = {}


def register_report_tools(mcp: FastMCP) -> None:
    """Register report generation tools."""
    
    @mcp.tool()
    async def generate_report(
        scan_id: Annotated[str, Field(description="扫描任务ID")],
        report_type: Annotated[str, Field(description="报告类型: vulnerability/compliance/executive")] = "vulnerability",
        format: Annotated[str, Field(description="报告格式: pdf/html/json/csv")] = "pdf",
    ) -> str:
        """
        生成扫描报告
        
        ## 功能说明
        根据扫描结果生成专业的安全扫描报告。
        
        ## 报告类型
        - **vulnerability**: 漏洞详情报告
        - **compliance**: 合规性检查报告
        - **executive**: 管理层摘要报告
        
        ## 报告格式
        - **pdf**: PDF文档（推荐）
        - **html**: 网页格式
        - **json**: JSON数据
        - **csv**: CSV表格
        
        Args:
            scan_id: 扫描任务ID
            report_type: 报告类型
            format: 报告格式
        
        Returns:
            JSON格式的报告信息
        """
        import json
        import uuid

        valid_types = ["vulnerability", "compliance", "executive"]
        valid_formats = ["pdf", "html", "json", "csv"]
        if report_type not in valid_types:
            return json.dumps(
                {"error": f"Invalid report_type. Must be one of: {valid_types}"},
                ensure_ascii=False,
            )
        if format not in valid_formats:
            return json.dumps(
                {"error": f"Invalid format. Must be one of: {valid_formats}"},
                ensure_ascii=False,
            )

        report_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()

        report = Report(
            report_id=report_id,
            scan_id=scan_id,
            report_type=report_type,
            created_at=now,
            format=format,
        )
        _reports[report_id] = report
        
        return json.dumps({
            "report_id": report_id,
            "scan_id": scan_id,
            "report_type": report_type,
            "format": format,
            "status": "generated",
            "created_at": now,
            "message": "报告生成完成"
        }, ensure_ascii=False)

    @mcp.tool()
    async def list_reports(
        limit: Annotated[int, Field(description="返回结果数量限制")] = 20,
    ) -> str:
        """
        列出生成的报告
        
        Args:
            limit: 返回数量限制
        
        Returns:
            JSON格式的报告列表
        """
        import json
        
        items = [{"report_id": k, **v.model_dump()} for k, v in list(_reports.items())[:limit]]
        
        return json.dumps({
            "total": len(_reports),
            "reports": items
        }, ensure_ascii=False, default=str)
