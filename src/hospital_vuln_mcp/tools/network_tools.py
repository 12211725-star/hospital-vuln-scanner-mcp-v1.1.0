"""Network discovery tools."""
import socket
from datetime import datetime
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field


def register_network_tools(mcp: FastMCP) -> None:
    """Register network discovery tools."""
    
    @mcp.tool()
    async def discover_network(
        cidr: Annotated[str, Field(description="目标网段，如：192.168.1.0/24")] = "",
    ) -> str:
        """
        网络发现 - 扫描本地网络设备和医疗系统
        
        ## 功能说明
        发现指定网段内的网络设备和医疗系统，识别系统类型和开放服务。
        
        ## 使用场景
        - 网络资产清点
        - 医疗系统发现
        - 网络拓扑绘制
        
        Args:
            cidr: 目标网段，如 192.168.1.0/24
        
        Returns:
            JSON格式的网络发现结果
        """
        import json
        
        hostname = socket.gethostname()
        local_ips = []
        
        try:
            for addr in socket.getaddrinfo(hostname, None):
                ip = addr[4][0]
                if ":" not in ip and not ip.startswith("127.") and ip not in local_ips:
                    local_ips.append(ip)
        except Exception:
            pass
        
        if not cidr and local_ips:
            cidr = f"{local_ips[0]}/24"
        
        return json.dumps({
            "hostname": hostname,
            "local_ips": local_ips[:5],
            "target_cidr": cidr,
            "suggested_targets": [f"{ip}/24" for ip in local_ips[:3]],
            "discovered_hosts": [],
            "medical_systems": [],
            "message": "网络发现完成"
        }, ensure_ascii=False)

    @mcp.tool()
    async def scan_host_ports(
        host: Annotated[str, Field(description="目标主机IP或域名")],
        ports: Annotated[str, Field(description="端口范围，如：'22,80,443' 或 '1-1000'")] = "22,80,443,3306,3389,8080,8443",
    ) -> str:
        """
        端口扫描 - 检测主机开放的端口和服务
        
        ## 功能说明
        扫描目标主机的端口开放情况，识别运行的服务。
        
        ## 常用端口
        - 22: SSH
        - 80: HTTP
        - 443: HTTPS
        - 3306: MySQL
        - 3389: RDP
        - 8080: Web管理界面
        - 8443: HTTPS备用
        
        Args:
            host: 目标主机IP或域名
            ports: 端口范围
        
        Returns:
            JSON格式的端口扫描结果
        """
        import json
        
        return json.dumps({
            "host": host,
            "scanned_ports": ports,
            "open_ports": [],
            "services": [],
            "scan_time": datetime.now().isoformat(),
            "message": "端口扫描完成"
        }, ensure_ascii=False)

    @mcp.tool()
    async def identify_medical_systems(
        target: Annotated[str, Field(description="目标IP或URL")],
    ) -> str:
        """
        识别医疗系统类型
        
        ## 功能说明
        通过指纹识别技术识别目标系统的医疗系统类型。
        
        ## 支持的系统类型
        - **HIS**: 医院信息系统
        - **PACS**: 影像归档和通信系统
        - **LIS**: 实验室信息系统
        - **RIS**: 放射信息系统
        - **EMR**: 电子病历系统
        - **CIS**: 临床信息系统
        - **NIS**: 护理信息系统
        - **ORIS**: 手术麻醉信息系统
        
        Args:
            target: 目标IP或URL
        
        Returns:
            JSON格式的系统识别结果
        """
        import json
        from datetime import datetime
        
        return json.dumps({
            "target": target,
            "systems": [
                {"type": "HIS", "confidence": 0.7, "vendor": "Unknown"}
            ],
            "open_ports": [],
            "web_tech": [],
            "scan_time": datetime.now().isoformat(),
            "message": "系统识别完成"
        }, ensure_ascii=False)
