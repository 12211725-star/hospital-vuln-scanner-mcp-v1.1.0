"""
Real scanning engine for hospital vulnerability scanner.
支持 nmap/nuclei（如果安装）或 Python 回退实现。
"""
import asyncio
import json
import os
import socket
import subprocess
import re
import uuid
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List, Dict, Any
from pathlib import Path

# 检查外部工具是否可用（支持自定义路径）
def _find_tool(name: str) -> Optional[str]:
    """查找工具路径，支持环境变量指定"""
    # 1. 先检查环境变量
    env_path = os.environ.get(f"{name.upper()}_PATH", "")
    if env_path and os.path.isfile(env_path):
        return env_path
    # 2. 常见路径
    common_paths = [
        f"/usr/local/bin/{name}",
        f"/usr/bin/{name}",
        f"{os.path.expanduser('~/.local/bin/')}{name}",
    ]
    for p in common_paths:
        if os.path.isfile(p):
            return p
    # 3. shutil.which
    import shutil
    return shutil.which(name)

NMAP_PATH = _find_tool("nmap")
NUCLEI_PATH = _find_tool("nuclei")
NMAP_AVAILABLE = NMAP_PATH is not None
NUCLEI_AVAILABLE = NUCLEI_PATH is not None

# 常用端口映射
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    1433: "MSSQL",
    1521: "Oracle",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    9000: "PHP-FPM",
    27017: "MongoDB",
}

# 医疗系统特征
MEDICAL_SIGNATURES = {
    "HIS": [
        "his", "医院信息系统", "hospital information", "门诊", "住院", "挂号",
        "处方", "医嘱", "电子病历", "emr", "his_system"
    ],
    "PACS": [
        "pacs", "影像", "dicom", "影像归档", "radiology", "医学影像",
        "影像系统", "pacs_server"
    ],
    "LIS": [
        "lis", "检验", "实验室", "laboratory", "实验室信息", "检验系统",
        "lis_system", "生化", "免疫"
    ],
    "RIS": [
        "ris", "放射", "radiology information", "放射系统", "ris_system",
        "放射科", "影像诊断"
    ],
    "EMR": [
        "emr", "电子病历", "electronic medical", "病历系统", "emr_system",
        "电子病历系统", "病程记录"
    ],
}


def check_port(host: str, port: int, timeout: float = 2.0) -> Optional[Dict[str, Any]]:
    """检查单个端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            service = COMMON_PORTS.get(port, "unknown")
            return {"port": port, "service": service, "state": "open"}
    except Exception:
        pass
    return None


def scan_ports_socket(host: str, ports: List[int], timeout: float = 1.0, max_workers: int = 50) -> List[Dict]:
    """使用 socket 多线程扫描端口"""
    open_ports = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(lambda p: check_port(host, p, timeout), ports)
        for r in results:
            if r:
                open_ports.append(r)
    return open_ports


def scan_ports_nmap(host: str, ports: List[int]) -> List[Dict]:
    """使用 nmap 扫描端口（如果可用）"""
    if not NMAP_AVAILABLE or not NMAP_PATH:
        return scan_ports_socket(host, ports)
    
    ports_str = ",".join(str(p) for p in ports[:100])  # nmap 限制
    try:
        result = subprocess.run(
            [NMAP_PATH, "-Pn", "-sT", "-p", ports_str, "--open", "-T4", host],
            capture_output=True, text=True, timeout=60
        )
        open_ports = []
        for line in result.stdout.split("\n"):
            match = re.match(r"(\d+)/(tcp|udp)\s+open\s+(\S+)?", line.strip())
            if match:
                port = int(match.group(1))
                service = match.group(3) if match.group(3) else COMMON_PORTS.get(port, "unknown")
                open_ports.append({"port": port, "service": service, "state": "open"})
        return open_ports
    except Exception:
        return scan_ports_socket(host, ports)


def identify_service_banner(host: str, port: int, timeout: float = 2.0) -> Optional[str]:
    """尝试获取服务 banner"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        # 发送 HTTP 请求或等待 banner
        if port in [80, 8080, 443, 8443]:
            sock.send(b"HEAD / HTTP/1.0\r\nHost: localhost\r\n\r\n")
        response = sock.recv(1024)
        sock.close()
        return response.decode("utf-8", errors="ignore")
    except Exception:
        return None


def detect_medical_system(host: str, port: int, banner: Optional[str]) -> Dict[str, Any]:
    """根据 banner 检测医疗系统类型"""
    if not banner:
        return {"system_type": "UNKNOWN", "confidence": 0.0, "vendor": None}
    
    banner_lower = banner.lower()
    
    for system_type, keywords in MEDICAL_SIGNATURES.items():
        for kw in keywords:
            if kw.lower() in banner_lower:
                return {
                    "system_type": system_type,
                    "confidence": 0.8,
                    "vendor": detect_vendor(banner)
                }
    
    return {"system_type": "UNKNOWN", "confidence": 0.0, "vendor": None}


def detect_vendor(banner: str) -> Optional[str]:
    """从 banner 中识别厂商"""
    vendors = {
        "东软": ["neusoft", "东软"],
        "卫宁健康": ["winning", "卫宁"],
        "用友医疗": ["yonyou", "用友"],
        "华为": ["huawei"],
        "汇健": ["huijian"],
        "万达信息": ["wondernet"],
    }
    banner_lower = banner.lower()
    for vendor, patterns in vendors.items():
        for p in patterns:
            if p.lower() in banner_lower:
                return vendor
    return None


async def quick_scan(host: str) -> Dict[str, Any]:
    """
    快速扫描：常用端口 + 基础识别
    
    Returns:
        包含 open_ports, services, medical_systems 的字典
    """
    # 常用端口
    ports = [21, 22, 23, 25, 80, 110, 143, 443, 445, 1433, 1521, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 9000, 27017]
    
    # 扫描端口
    if NMAP_AVAILABLE:
        open_ports = scan_ports_nmap(host, ports)
    else:
        open_ports = scan_ports_socket(host, ports, timeout=1.5)
    
    # 尝试识别服务
    medical_systems = []
    for port_info in open_ports[:10]:  # 限制并发
        port = port_info["port"]
        banner = identify_service_banner(host, port)
        if banner:
            port_info["banner"] = banner[:200]  # 截断
            med_info = detect_medical_system(host, port, banner)
            if med_info["system_type"] != "UNKNOWN":
                medical_systems.append(med_info)
    
    return {
        "host": host,
        "open_ports": open_ports,
        "medical_systems": medical_systems,
        "scan_time": datetime.now().isoformat(),
    }


async def standard_scan(host: str) -> Dict[str, Any]:
    """
    标准扫描：扩展端口 + 漏洞检测
    
    Returns:
        包含 open_ports, vulnerabilities, medical_systems
    """
    # 扩展端口范围
    ports = list(COMMON_PORTS.keys()) + list(range(8000, 8100))
    
    # 端口扫描
    if NMAP_AVAILABLE:
        open_ports = scan_ports_nmap(host, ports[:100])
    else:
        open_ports = scan_ports_socket(host, ports, timeout=1.0)
    
    # 漏洞检测（如果 nuclei 可用）
    vulnerabilities = []
    if NUCLEI_AVAILABLE and NUCLEI_PATH:
        try:
            result = subprocess.run(
                [NUCLEI_PATH, "-u", host, "-silent", "-json"],
                capture_output=True, text=True, timeout=120
            )
            for line in result.stdout.strip().split("\n"):
                if line:
                    try:
                        vuln = json.loads(line)
                        vulnerabilities.append({
                            "title": vuln.get("info", {}).get("name", "Unknown"),
                            "severity": vuln.get("info", {}).get("severity", "info"),
                            "description": vuln.get("info", {}).get("description", ""),
                            "matched_at": vuln.get("matched", ""),
                        })
                    except json.JSONDecodeError:
                        pass
        except Exception:
            pass
    
    # 如果 nuclei 不可用，使用内置规则检测常见漏洞
    if not NUCLEI_AVAILABLE:
        vulnerabilities = await detect_common_vulns(host, open_ports)
    
    # 医疗系统识别
    medical_systems = []
    for port_info in open_ports[:10]:
        port = port_info["port"]
        banner = identify_service_banner(host, port)
        if banner:
            port_info["banner"] = banner[:200]
            med_info = detect_medical_system(host, port, banner)
            if med_info["system_type"] != "UNKNOWN":
                medical_systems.append(med_info)
    
    return {
        "host": host,
        "open_ports": open_ports,
        "vulnerabilities": vulnerabilities,
        "medical_systems": medical_systems,
        "scan_time": datetime.now().isoformat(),
    }


async def detect_common_vulns(host: str, open_ports: List[Dict]) -> List[Dict]:
    """内置规则：检测常见漏洞"""
    vulns = []
    
    for port_info in open_ports:
        port = port_info["port"]
        
        # 检测弱口令/默认配置风险
        if port == 3306:
            vulns.append({
                "title": "MySQL 服务暴露",
                "severity": "medium",
                "description": "MySQL 数据库服务端口对外开放，可能存在未授权访问风险",
                "matched_at": f"{host}:{port}",
            })
        
        if port == 3389:
            vulns.append({
                "title": "RDP 远程桌面暴露",
                "severity": "high",
                "description": "Windows 远程桌面服务对外开放，建议启用网络级别身份验证(NLA)",
                "matched_at": f"{host}:{port}",
            })
        
        if port == 6379:
            vulns.append({
                "title": "Redis 未授权访问风险",
                "severity": "high",
                "description": "Redis 服务端口暴露，若未设置密码可能导致未授权访问",
                "matched_at": f"{host}:{port}",
            })
        
        if port == 27017:
            vulns.append({
                "title": "MongoDB 未授权访问风险",
                "severity": "high",
                "description": "MongoDB 服务端口暴露，默认配置可能无认证",
                "matched_at": f"{host}:{port}",
            })
        
        # HTTP 服务检测
        if port in [80, 8080, 443, 8443]:
            banner = identify_service_banner(host, port)
            if banner:
                # 检测敏感路径泄露
                if "phpinfo" in banner.lower():
                    vulns.append({
                        "title": "PHPInfo 信息泄露",
                        "severity": "medium",
                        "description": "检测到 PHPInfo 页面，可能泄露服务器敏感信息",
                        "matched_at": f"{host}:{port}",
                    })
                
                # 检测目录遍历
                if "index of" in banner.lower():
                    vulns.append({
                        "title": "目录遍历风险",
                        "severity": "medium",
                        "description": "检测到目录列表功能，可能泄露敏感文件",
                        "matched_at": f"{host}:{port}",
                    })
    
    return vulns


def expand_cidr(cidr: str) -> List[str]:
    """展开 CIDR 为 IP 列表（限制 /28 以内）"""
    import ipaddress
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        # 限制扫描范围
        if network.num_addresses > 16:
            return [str(ip) for ip in list(network.hosts())[:16]]
        return [str(ip) for ip in network.hosts()]
    except Exception:
        return []


def generate_mock_vulnerabilities(host: str, count: int = 5) -> List[Dict]:
    """
    生成模拟漏洞数据（仅用于演示模式或回退）
    
    ⚠️ 这些是假数据，真实扫描请使用 nuclei 或完整扫描引擎
    """
    import random
    
    vuln_templates = [
        {"title": "SSH 弱加密算法", "severity": "medium", "cve": "CVE-2020-15778"},
        {"title": "HTTP 安全头缺失", "severity": "low", "cve": None},
        {"title": "SSL 证书过期", "severity": "medium", "cve": None},
        {"title": "NTP 放大攻击风险", "severity": "medium", "cve": "CVE-2013-5211"},
        {"title": "SMBv1 协议启用", "severity": "high", "cve": "CVE-2017-0144"},
        {"title": "弱密码策略", "severity": "medium", "cve": None},
        {"title": "默认凭证未修改", "severity": "critical", "cve": None},
    ]
    
    selected = random.sample(vuln_templates, min(count, len(vuln_templates)))
    
    return [
        {
            "vuln_id": f"MV-{uuid.uuid4().hex[:8]}",
            "title": v["title"],
            "severity": v["severity"],
            "cve_id": v["cve"],
            "affected_host": host,
            "description": f"{v['title']} - 影响主机 {host}",
            "discovered_at": datetime.now().isoformat(),
        }
        for v in selected
    ]
