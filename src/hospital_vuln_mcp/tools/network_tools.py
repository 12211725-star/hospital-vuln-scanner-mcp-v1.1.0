"""Network discovery tools — 支持真实端口扫描和系统识别."""
import json
import socket
from datetime import datetime
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from ..scanner import (
    scan_ports_nmap, scan_ports_socket, identify_service_banner,
    detect_medical_system, expand_cidr, _find_tool,
    _NMAP_COMMON_PATHS, _NUCLEI_COMMON_PATHS,
)


def register_network_tools(mcp: FastMCP) -> None:
    """Register network discovery tools."""

    @mcp.tool()
    async def discover_network(
        cidr: Annotated[str, Field(description="目标网段，如：192.168.1.0/24")] = "",
    ) -> str:
        """
        网络发现 - 扫描本地网络设备和医疗系统

        ## 功能说明
        发现指定网段内的网络设备，识别开放端口和医疗系统类型。

        Args:
            cidr: 目标网段，如 192.168.1.0/24

        Returns:
            JSON格式的网络发现结果
        """
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

        # 对网段内的主机进行快速端口探测
        discovered_hosts = []
        if cidr:
            hosts = expand_cidr(cidr)
            for host in hosts[:8]:  # 限制最多8台
                open_ports = scan_ports_socket(
                    host,
                    [22, 80, 443, 3306, 3389, 8080, 8443],
                    timeout=0.5,
                )
                if open_ports:
                    discovered_hosts.append({
                        "host": host,
                        "open_ports": open_ports,
                        "ports_count": len(open_ports),
                    })

        return json.dumps({
            "hostname": hostname,
            "local_ips": local_ips[:5],
            "target_cidr": cidr,
            "discovered_hosts": discovered_hosts,
            "hosts_found": len(discovered_hosts),
            "nmap_available": _find_tool("nmap", _NMAP_COMMON_PATHS) is not None,
            "message": f"网络发现完成，发现 {len(discovered_hosts)} 台活跃主机"
        }, ensure_ascii=False)

    @mcp.tool()
    async def scan_host_ports(
        host: Annotated[str, Field(description="目标主机IP或域名")],
        ports: Annotated[str, Field(description="端口范围，如：'22,80,443' 或 '1-1000'")] = "22,80,443,3306,3389,8080,8443",
    ) -> str:
        """
        端口扫描 - 真实检测主机开放的端口和服务

        ## 功能说明
        对目标主机进行端口扫描，识别开放的端口和运行的服务。
        如果系统安装了 nmap 会自动使用，否则使用 Python socket 扫描。

        Args:
            host: 目标主机IP或域名
            ports: 端口范围，如 '22,80,443'

        Returns:
            JSON格式的端口扫描结果，包含开放端口和服务信息
        """
        # 解析端口参数
        port_list = []
        for part in ports.split(","):
            part = part.strip()
            if "-" in part:
                try:
                    start, end = part.split("-", 1)
                    port_list.extend(range(int(start), int(end) + 1))
                except ValueError:
                    pass
            else:
                try:
                    port_list.append(int(part))
                except ValueError:
                    pass

        # 限制端口数量
        port_list = list(set(port_list))[:500]

        if not port_list:
            port_list = [22, 80, 443, 3306, 3389, 8080, 8443]

        # 执行扫描
        if _find_tool("nmap", _NMAP_COMMON_PATHS) is not None and len(port_list) <= 100:
            open_ports = scan_ports_nmap(host, port_list)
        else:
            open_ports = scan_ports_socket(host, port_list, timeout=1.5)

        # 尝试获取 banner
        for port_info in open_ports[:15]:
            banner = identify_service_banner(host, port_info["port"])
            if banner:
                port_info["banner"] = banner[:200]

        return json.dumps({
            "host": host,
            "scanned_ports": len(port_list),
            "open_ports": open_ports,
            "open_count": len(open_ports),
            "scan_method": "nmap" if _find_tool("nmap", _NMAP_COMMON_PATHS) is not None else "socket",
            "scan_time": datetime.now().isoformat(),
            "message": f"端口扫描完成: 扫描 {len(port_list)} 个端口，发现 {len(open_ports)} 个开放端口"
        }, ensure_ascii=False)

    @mcp.tool()
    async def identify_medical_systems(
        target: Annotated[str, Field(description="目标IP或URL")],
    ) -> str:
        """
        识别医疗系统类型

        ## 功能说明
        通过端口扫描、服务指纹和 HTTP 响应特征识别目标系统的医疗系统类型。

        ## 支持的系统类型
        - HIS: 医院信息系统
        - PACS: 影像归档和通信系统
        - LIS: 实验室信息系统
        - RIS: 放射信息系统
        - EMR: 电子病历系统

        Args:
            target: 目标IP或URL

        Returns:
            JSON格式的系统识别结果
        """
        host = target.strip()
        if host.startswith("http://"):
            host = host[7:]
        elif host.startswith("https://"):
            host = host[8:]
        host = host.split("/")[0].split(":")[0]

        # 扫描常见端口
        ports = [22, 80, 443, 3306, 3389, 8080, 8443]
        open_ports = scan_ports_socket(host, ports, timeout=1.5)

        # 识别系统和 banner
        systems = []
        web_tech = []

        for port_info in open_ports:
            port = port_info["port"]
            banner = identify_service_banner(host, port)

            if banner:
                port_info["banner"] = banner[:200]

                # 医疗系统识别
                med_info = detect_medical_system(host, port, banner)
                if med_info["system_type"] != "UNKNOWN":
                    systems.append(med_info)

                # Web 技术识别
                banner_lower = banner.lower()
                tech_map = {
                    "Apache": "apache",
                    "nginx": "nginx",
                    "IIS": "microsoft-iis",
                    "PHP": "php",
                    "ASP.NET": "asp.net",
                    "Tomcat": "tomcat",
                }
                for tech, sig in tech_map.items():
                    if sig.lower() in banner_lower:
                        web_tech.append({"name": tech, "port": port})

        # 如果没有识别到医疗系统，但发现了 Web 端口
        if not systems and any(p["port"] in [80, 443, 8080, 8443] for p in open_ports):
            systems.append({
                "system_type": "UNKNOWN",
                "confidence": 0.3,
                "vendor": None,
                "note": "发现 Web 服务但未能确定系统类型，建议通过 HTTP 路径进一步识别"
            })

        return json.dumps({
            "target": target,
            "host": host,
            "open_ports": open_ports,
            "systems": systems,
            "web_tech": web_tech,
            "scan_time": datetime.now().isoformat(),
            "message": f"系统识别完成: 发现 {len(open_ports)} 个开放端口，识别出 {len(systems)} 个系统"
        }, ensure_ascii=False)
