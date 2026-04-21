"""Application resources."""
import json
from fastmcp import FastMCP

from .._version import __version__


def register_resources(mcp: FastMCP) -> None:
    """Register application resources."""
    
    @mcp.resource("config://app-info")
    def get_app_info() -> str:
        """获取应用配置信息"""
        return json.dumps({
            "name": "医院漏洞扫描MCP",
            "name_en": "Hospital Vulnerability Scanner MCP",
            "version": __version__,
            "description": "为AI助手提供医疗系统安全扫描能力的MCP服务器",
            "features": [
                "漏洞扫描",
                "网络发现",
                "医疗系统识别",
                "报告生成",
                "漏洞统计"
            ],
            "supported_systems": [
                "HIS", "PACS", "LIS", "RIS", "EMR", "CIS", "NIS", "ORIS"
            ],
            "author": "Hospital Security Team",
            "license": "MIT"
        }, ensure_ascii=False)
    
    @mcp.resource("config://scan-profiles")
    def get_scan_profiles() -> str:
        """获取扫描配置配置"""
        return json.dumps({
            "profiles": {
                "quick": {
                    "name": "快速扫描",
                    "description": "扫描常见高危端口和已知漏洞",
                    "duration": "5-10分钟",
                    "ports": "top-100",
                    "checks": ["common_vulns", "open_ports"]
                },
                "standard": {
                    "name": "标准扫描",
                    "description": "覆盖主要服务和常见漏洞",
                    "duration": "30-60分钟",
                    "ports": "top-1000",
                    "checks": ["common_vulns", "service_detection", "version_detection"]
                },
                "deep": {
                    "name": "深度扫描",
                    "description": "全面检测包括Web应用漏洞",
                    "duration": "2-4小时",
                    "ports": "all",
                    "checks": ["all_vulns", "web_app", "api_tests", "configuration_audit"]
                }
            }
        }, ensure_ascii=False)
    
    @mcp.resource("docs://severity-levels")
    def get_severity_docs() -> str:
        """获取严重程度分级说明"""
        return json.dumps({
            "severity_levels": {
                "critical": {
                    "level": "严重",
                    "cvss_range": "9.0-10.0",
                    "description": "可被远程攻击者利用，无需认证即可获取系统完全控制权",
                    "action": "立即修复",
                    "sla": "24小时内"
                },
                "high": {
                    "level": "高危",
                    "cvss_range": "7.0-8.9",
                    "description": "攻击难度较低，可能导致敏感信息泄露或系统部分功能失控",
                    "action": "尽快修复",
                    "sla": "7天内"
                },
                "medium": {
                    "level": "中危",
                    "cvss_range": "4.0-6.9",
                    "description": "需要一定条件才能利用，影响有限",
                    "action": "计划修复",
                    "sla": "30天内"
                },
                "low": {
                    "level": "低危",
                    "cvss_range": "0.1-3.9",
                    "description": "影响较小，难以利用",
                    "action": "酌情修复",
                    "sla": "90天内"
                },
                "info": {
                    "level": "信息",
                    "cvss_range": "0.0",
                    "description": "非安全问题，仅信息收集",
                    "action": "参考",
                    "sla": "无需修复"
                }
            }
        }, ensure_ascii=False)
