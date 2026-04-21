"""
Hospital Vulnerability Scanner MCP Server

基于魔搭 MCP 开发规范的医院漏洞扫描服务器。

Example:
    >>> from hospital_vuln_mcp import create_server
    >>> server = create_server()
    >>> server.run()
"""
from .server import create_server
from .cli import main
from ._version import __version__

__all__ = ["create_server", "main", "__version__"]
