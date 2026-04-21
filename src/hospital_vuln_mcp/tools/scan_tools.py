"""Scan management tools."""
import uuid
from datetime import datetime
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from ..models import ScanTask, ScanResult


# In-memory storage for scans
_scans: dict[str, ScanTask] = {}
_scan_results: dict[str, ScanResult] = {}


def register_scan_tools(mcp: FastMCP) -> None:
    """Register scan management tools."""
    
    @mcp.tool()
    async def start_scan(
        target: Annotated[str, Field(description="扫描目标，支持IP、域名、URL或CIDR格式，如：192.168.1.1 或 192.168.1.0/24")],
        scan_type: Annotated[str, Field(description="扫描类型：quick(快速)/standard(标准)/deep(深度)")] = "quick",
    ) -> str:
        """
        启动漏洞扫描任务
        
        ## 功能说明
        对指定的医疗系统目标启动安全漏洞扫描，支持快速、标准和深度三种扫描模式。
        
        ## 使用场景
        - 定期安全巡检
        - 新系统上线前安全检查
        - 漏洞修复后验证扫描
        - 合规性检查
        
        ## 扫描类型说明
        - **quick**: 快速扫描，扫描常见高危端口和已知漏洞，约5-10分钟
        - **standard**: 标准扫描，覆盖主要服务和常见漏洞，约30-60分钟
        - **deep**: 深度扫描，全面检测包括Web应用漏洞，约2-4小时
        
        Args:
            target: 扫描目标，支持IP、域名、URL或CIDR格式
            scan_type: 扫描类型，可选 quick/standard/deep，默认quick
        
        Returns:
            JSON格式的扫描任务信息，包含task_id用于后续查询
        
        Example:
            >>> start_scan(target="192.168.1.100", scan_type="standard")
            '{"task_id": "abc123", "status": "started", "target": "192.168.1.100"}'
        """
        # Validate target
        if not target or len(target) > 255:
            return '{"error": "Invalid target format"}'
        
        # Validate scan_type
        valid_types = ["quick", "standard", "deep"]
        if scan_type not in valid_types:
            return f'{{"error": "Invalid scan_type. Must be one of: {valid_types}"}}'
        
        task_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        
        scan_task = ScanTask(
            task_id=task_id,
            target=target,
            scan_type=scan_type,
            status="running",
            created_at=now,
            started_at=now,
            progress=0,
        )
        
        _scans[task_id] = scan_task
        _scan_results[task_id] = ScanResult(
            task_id=task_id,
            scan_info=scan_task,
            vulnerabilities=[],
            summary={"hosts_total": 0, "hosts_scanned": 0, "vulns_found": 0}
        )
        
        import json
        return json.dumps({
            "task_id": task_id,
            "status": "started",
            "target": target,
            "scan_type": scan_type,
            "message": f"扫描任务已启动，目标: {target}，类型: {scan_type}"
        }, ensure_ascii=False)

    @mcp.tool()
    async def get_scan_status(
        task_id: Annotated[str, Field(description="扫描任务ID，由start_scan返回")],
    ) -> str:
        """
        查询扫描任务状态和结果
        
        ## 功能说明
        获取指定扫描任务的当前状态、进度和已发现的漏洞信息。
        
        ## 使用场景
        - 检查扫描进度
        - 获取扫描结果
        - 监控长时间运行的扫描任务
        
        Args:
            task_id: 扫描任务ID
        
        Returns:
            JSON格式的扫描状态和结果详情
        """
        import json
        
        if task_id not in _scans:
            return json.dumps({"error": "Task not found", "task_id": task_id}, ensure_ascii=False)
        
        scan = _scans[task_id]
        result = _scan_results.get(task_id)
        
        return json.dumps({
            "task_id": task_id,
            "status": scan.status,
            "target": scan.target,
            "scan_type": scan.scan_type,
            "progress": scan.progress,
            "created_at": scan.created_at,
            "started_at": scan.started_at,
            "completed_at": scan.completed_at,
            "total_hosts": scan.total_hosts,
            "scanned_hosts": scan.scanned_hosts,
            "vulnerabilities_count": len(result.vulnerabilities) if result else 0,
            "vulnerabilities": [v.model_dump() for v in result.vulnerabilities] if result else []
        }, ensure_ascii=False, default=str)

    @mcp.tool()
    async def list_scans(
        limit: Annotated[int, Field(description="返回结果数量限制，默认20，最大100")] = 20,
        status: Annotated[str, Field(description="按状态筛选：all/running/completed/cancelled/pending")] = "all",
    ) -> str:
        """
        列出扫描任务历史
        
        ## 功能说明
        获取所有扫描任务的列表，支持按状态筛选和数量限制。
        
        ## 使用场景
        - 查看历史扫描记录
        - 监控进行中的扫描
        - 生成扫描统计报表
        
        Args:
            limit: 返回结果数量限制，默认20
            status: 按状态筛选，默认all显示全部
        
        Returns:
            JSON格式的扫描任务列表
        """
        import json
        
        # Validate limit
        limit = min(max(limit, 1), 100)
        
        items = []
        for task_id, scan in _scans.items():
            if status != "all" and scan.status != status:
                continue
            items.append({
                "task_id": task_id,
                "target": scan.target,
                "scan_type": scan.scan_type,
                "status": scan.status,
                "progress": scan.progress,
                "created_at": scan.created_at,
            })
        items = items[:limit]
        
        return json.dumps({
            "total": len(_scans),
            "returned": len(items),
            "scans": items
        }, ensure_ascii=False, default=str)

    @mcp.tool()
    async def cancel_scan(
        task_id: Annotated[str, Field(description="要取消的扫描任务ID")],
    ) -> str:
        """
        取消正在运行的扫描任务
        
        ## 功能说明
        停止指定的扫描任务，已扫描的结果会被保留。
        
        ## 使用场景
        - 误操作启动扫描
        - 扫描时间过长需要停止
        - 业务高峰期需要释放资源
        
        Args:
            task_id: 扫描任务ID
        
        Returns:
            JSON格式的取消结果
        """
        import json
        
        if task_id not in _scans:
            return json.dumps({"error": "Task not found", "task_id": task_id}, ensure_ascii=False)
        
        scan = _scans[task_id]
        if scan.status not in ["pending", "running"]:
            return json.dumps({
                "task_id": task_id,
                "status": scan.status,
                "message": "Task is not running, cannot cancel"
            }, ensure_ascii=False)
        
        scan.status = "cancelled"
        scan.completed_at = datetime.now().isoformat()
        
        return json.dumps({
            "task_id": task_id,
            "status": "cancelled",
            "message": "扫描任务已取消"
        }, ensure_ascii=False)
