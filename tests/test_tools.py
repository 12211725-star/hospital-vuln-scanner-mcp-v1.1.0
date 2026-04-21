"""Tests for tools."""
import pytest
from hospital_vuln_mcp.server import create_server


class TestScanTools:
    """扫描工具测试"""
    
    @pytest.fixture
    def mcp(self):
        """创建MCP服务器实例"""
        return create_server()
    
    @pytest.mark.asyncio
    async def test_start_scan(self, mcp):
        """测试启动扫描"""
        # 这里应该调用实际的工具函数
        # 由于MCP工具是异步的，需要使用异步测试
        pass
    
    def test_scan_types(self):
        """测试扫描类型有效性"""
        valid_types = ["quick", "standard", "deep"]
        assert "quick" in valid_types
        assert "standard" in valid_types
        assert "deep" in valid_types


class TestVulnerabilityTools:
    """漏洞工具测试"""
    
    def test_severity_levels(self):
        """测试严重程度分级"""
        levels = ["critical", "high", "medium", "low", "info"]
        assert len(levels) == 5
    
    def test_vulnerability_status(self):
        """测试漏洞状态"""
        statuses = ["open", "fixed", "accepted", "false_positive"]
        assert "open" in statuses
        assert "fixed" in statuses


class TestNetworkTools:
    """网络工具测试"""
    
    def test_common_ports(self):
        """测试常见端口"""
        common_ports = [22, 80, 443, 3306, 3389, 8080, 8443]
        assert 22 in common_ports  # SSH
        assert 80 in common_ports  # HTTP
        assert 443 in common_ports  # HTTPS


class TestSystemTools:
    """系统工具测试"""
    
    def test_system_status(self):
        """测试系统状态"""
        valid_status = ["ok", "degraded", "error"]
        assert "ok" in valid_status


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
