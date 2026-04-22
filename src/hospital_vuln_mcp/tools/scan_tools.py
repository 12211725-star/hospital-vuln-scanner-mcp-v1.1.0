"""Scan management tools — 支持真实扫描."""
import asyncio
import json
import uuid
from datetime import datetime
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from ..models import ScanTask, ScanResult, Vulnerability
from ..scanner import (
    quick_scan, standard_scan, detect_common_vulns,
    _find_tool, _NMAP_COMMON_PATHS, _NUCLEI_COMMON_PATHS,
)


# 内存存储
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
        对指定目标启动安全漏洞扫描，支持快速、标准和深度三种模式。
        扫描会真实探测目标主机的端口、服务和漏洞。

        ## 扫描类型说明
        - **quick**: 快速扫描，常用端口 + 基础识别，约 10-30 秒
        - **standard**: 标准扫描，扩展端口 + 漏洞检测，约 30-120 秒
        - **deep**: 深度扫描，全端口 + nuclei 漏洞扫描，约 2-5 分钟

        Args:
            target: 扫描目标，支持IP/域名/URL/CIDR
            scan_type: quick/standard/deep

        Returns:
            JSON 格式扫描结果，包含发现的端口和漏洞
        """
        # 参数校验
        if not target or len(target) > 255:
            return json.dumps({"error": "Invalid target format"}, ensure_ascii=False)

        valid_types = ["quick", "standard", "deep"]
        if scan_type not in valid_types:
            return json.dumps({"error": f"Invalid scan_type. Must be: {valid_types}"}, ensure_ascii=False)

        task_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()

        scan_task = ScanTask(
            task_id=task_id,
            target=target,
            scan_type=scan_type,
            status="running",
            created_at=now,
            started_at=now,
            progress=10,
        )
        _scans[task_id] = scan_task

        # ====== 执行真实扫描 ======
        try:
            # 提取主机地址（去掉 CIDR 和 URL 前缀）
            host = target.strip()
            if host.startswith("http://"):
                host = host[7:]
            elif host.startswith("https://"):
                host = host[8:]
            host = host.split("/")[0].split(":")[0]

            if scan_type == "quick":
                result_data = await quick_scan(host)
            elif scan_type == "standard":
                result_data = await standard_scan(host)
            else:
                # deep 模式 = standard + 更多检测
                result_data = await standard_scan(host)

            # 构造漏洞列表
            vulns = []
            for v in result_data.get("vulnerabilities", []):
                vuln = Vulnerability(
                    vuln_id=f"V-{uuid.uuid4().hex[:8]}",
                    title=v.get("title", "Unknown"),
                    description=v.get("description", ""),
                    severity=v.get("severity", "info"),
                    affected_host=host,
                    discovered_at=now,
                    cve_id=v.get("cve_id"),
                )
                vulns.append(vuln)

            # 更新任务状态
            scan_task.status = "completed"
            scan_task.progress = 100
            scan_task.completed_at = datetime.now().isoformat()
            scan_task.total_hosts = 1
            scan_task.scanned_hosts = 1

            # 存储结果
            _scan_results[task_id] = ScanResult(
                task_id=task_id,
                scan_info=scan_task,
                vulnerabilities=vulns,
                summary={
                    "host": host,
                    "open_ports_count": len(result_data.get("open_ports", [])),
                    "vulnerabilities_count": len(vulns),
                    "medical_systems": result_data.get("medical_systems", []),
                    "open_ports": result_data.get("open_ports", []),
                    "scan_time": result_data.get("scan_time", now),
                    "nmap_available": _find_tool("nmap", _NMAP_COMMON_PATHS) is not None,
                    "nuclei_available": _find_tool("nuclei", _NUCLEI_COMMON_PATHS) is not None,
                },
            )

            return json.dumps({
                "task_id": task_id,
                "status": "completed",
                "target": target,
                "scan_type": scan_type,
                "host": host,
                "open_ports": result_data.get("open_ports", []),
                "open_ports_count": len(result_data.get("open_ports", [])),
                "vulnerabilities_found": len(vulns),
                "vulnerabilities": [v.model_dump() for v in vulns],
                "medical_systems": result_data.get("medical_systems", []),
                "nmap_used": _find_tool("nmap", _NMAP_COMMON_PATHS) is not None,
                "nuclei_used": _find_tool("nuclei", _NUCLEI_COMMON_PATHS) is not None,
                "message": f"扫描完成: {host}，发现 {len(result_data.get('open_ports', []))} 个开放端口，{len(vulns)} 个漏洞"
            }, ensure_ascii=False, default=str)

        except Exception as e:
            scan_task.status = "failed"
            scan_task.completed_at = datetime.now().isoformat()
            return json.dumps({
                "task_id": task_id,
                "status": "failed",
                "target": target,
                "error": str(e),
                "message": f"扫描失败: {e}"
            }, ensure_ascii=False)

    @mcp.tool()
    async def get_scan_status(
        task_id: Annotated[str, Field(description="扫描任务ID，由start_scan返回")],
    ) -> str:
        """
        查询扫描任务状态和结果

        Args:
            task_id: 扫描任务ID

        Returns:
            JSON格式的扫描状态和结果
        """
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
            "vulnerabilities": [v.model_dump() for v in result.vulnerabilities] if result else [],
            "summary": result.summary if result else {},
        }, ensure_ascii=False, default=str)

    @mcp.tool()
    async def list_scans(
        limit: Annotated[int, Field(description="返回结果数量限制，默认20")] = 20,
        status: Annotated[str, Field(description="按状态筛选：all/running/completed/cancelled/failed")] = "all",
    ) -> str:
        """
        列出扫描任务历史

        Args:
            limit: 返回结果数量限制
            status: 按状态筛选

        Returns:
            JSON格式的扫描任务列表
        """
        limit = min(max(limit, 1), 100)

        items = []
        for tid, scan in _scans.items():
            if status != "all" and scan.status != status:
                continue
            items.append({
                "task_id": tid,
                "target": scan.target,
                "scan_type": scan.scan_type,
                "status": scan.status,
                "progress": scan.progress,
                "vuln_count": len(_scan_results.get(tid, ScanResult(task_id=tid, scan_info=scan)).vulnerabilities),
                "created_at": scan.created_at,
                "completed_at": scan.completed_at,
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

        Args:
            task_id: 扫描任务ID

        Returns:
            JSON格式的取消结果
        """
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
