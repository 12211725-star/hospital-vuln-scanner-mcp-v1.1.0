"""
Pydantic models for type definitions.
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class Vulnerability(BaseModel):
    """漏洞模型"""
    vuln_id: str = Field(description="漏洞ID")
    title: str = Field(description="漏洞标题")
    description: str = Field(description="漏洞描述")
    severity: Literal["critical", "high", "medium", "low", "info"] = Field(description="严重程度")
    cvss_score: Optional[float] = Field(default=None, description="CVSS评分")
    cve_id: Optional[str] = Field(default=None, description="CVE编号")
    status: Literal["open", "fixed", "accepted", "false_positive"] = Field(default="open", description="处理状态")
    affected_host: str = Field(description="受影响主机")
    discovered_at: str = Field(description="发现时间")
    fixed_at: Optional[str] = Field(default=None, description="修复时间")


class ScanTask(BaseModel):
    """扫描任务模型"""
    task_id: str = Field(description="任务ID")
    target: str = Field(description="扫描目标")
    scan_type: Literal["quick", "standard", "deep"] = Field(description="扫描类型")
    status: Literal["pending", "running", "completed", "cancelled", "failed"] = Field(description="任务状态")
    created_at: str = Field(description="创建时间")
    started_at: Optional[str] = Field(default=None, description="开始时间")
    completed_at: Optional[str] = Field(default=None, description="完成时间")
    progress: int = Field(default=0, ge=0, le=100, description="进度百分比")
    total_hosts: int = Field(default=0, description="总主机数")
    scanned_hosts: int = Field(default=0, description="已扫描主机数")


class ScanResult(BaseModel):
    """扫描结果模型"""
    task_id: str = Field(description="任务ID")
    scan_info: ScanTask = Field(description="扫描信息")
    vulnerabilities: List[Vulnerability] = Field(default=[], description="发现的漏洞列表")
    summary: dict = Field(default={}, description="扫描摘要")


class MedicalSystem(BaseModel):
    """医疗系统识别结果"""
    system_type: Literal["HIS", "PACS", "LIS", "RIS", "EMR", "CIS", "NIS", "ORIS", "UNKNOWN"] = Field(description="系统类型")
    confidence: float = Field(ge=0, le=1, description="识别置信度")
    vendor: Optional[str] = Field(default=None, description="厂商信息")
    version: Optional[str] = Field(default=None, description="版本信息")
    open_ports: List[int] = Field(default=[], description="开放端口")
    services: List[dict] = Field(default=[], description="运行服务")


class PortScanResult(BaseModel):
    """端口扫描结果"""
    host: str = Field(description="目标主机")
    open_ports: List[dict] = Field(description="开放端口列表")
    scan_time: str = Field(description="扫描时间")


class Report(BaseModel):
    """扫描报告"""
    report_id: str = Field(description="报告ID")
    scan_id: str = Field(description="关联扫描ID")
    report_type: Literal["vulnerability", "compliance", "executive"] = Field(description="报告类型")
    created_at: str = Field(description="创建时间")
    format: Literal["pdf", "html", "json", "csv"] = Field(description="报告格式")
    download_url: Optional[str] = Field(default=None, description="下载链接")


class VulnerabilityStats(BaseModel):
    """漏洞统计"""
    total: int = Field(description="漏洞总数")
    by_severity: dict = Field(description="按严重程度统计")
    by_status: dict = Field(description="按状态统计")
    by_system_type: dict = Field(description="按系统类型统计")
    trend: List[dict] = Field(default=[], description="趋势数据")
    period: str = Field(description="统计周期")


class SystemStatus(BaseModel):
    """系统状态"""
    server: str = Field(description="服务器名称")
    version: str = Field(description="版本号")
    status: Literal["ok", "degraded", "error"] = Field(description="状态")
    uptime: Optional[str] = Field(default=None, description="运行时间")
    total_scans: int = Field(description="总扫描次数")
    active_scans: int = Field(description="活跃扫描数")
    queued_scans: int = Field(description="排队扫描数")
