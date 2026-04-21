"""Scan-related prompt templates."""
from fastmcp import FastMCP


def register_prompts(mcp: FastMCP) -> None:
    """Register prompt templates."""
    
    @mcp.prompt()
    def vulnerability_analysis(vuln_data: str) -> str:
        """
        漏洞分析报告提示词模板
        
        Args:
            vuln_data: 漏洞数据JSON
        
        Returns:
            格式化后的分析提示词
        """
        return f"""请作为医疗系统安全专家，分析以下漏洞数据并提供专业建议：

漏洞数据：
{vuln_data}

请提供以下分析：
1. 漏洞影响评估（对医疗业务的影响程度）
2. 修复优先级建议
3. 具体修复方案
4. 临时缓解措施
5. 修复验证方法

注意医疗系统的特殊性：
- 系统可用性要求高，修复需在维护窗口进行
- 需考虑数据安全和患者隐私保护
- 修复后需进行功能验证
"""
    
    @mcp.prompt()
    def scan_planning(scope: str, system_type: str = "HIS") -> str:
        """
        扫描规划提示词模板
        
        Args:
            scope: 扫描范围
            system_type: 系统类型
        
        Returns:
            扫描规划提示词
        """
        return f"""请制定针对{system_type}系统的安全扫描计划。

扫描范围：{scope}

请提供以下内容：
1. 扫描策略建议（快速/标准/深度）
2. 扫描时间安排建议（考虑业务低峰期）
3. 扫描前准备工作清单
4. 风险评估和应急预案
5. 扫描后验证计划

医疗系统扫描注意事项：
- 避免在诊疗高峰期进行深度扫描
- 准备回滚方案以防系统异常
- 与系统管理员保持沟通
- 遵守医院信息安全管理制度
"""
    
    @mcp.prompt()
    def compliance_check(system_type: str, regulations: str = "等保2.0") -> str:
        """
        合规性检查提示词模板
        
        Args:
            system_type: 系统类型
            regulations: 适用法规标准
        
        Returns:
            合规性检查提示词
        """
        return f"""请对{system_type}系统进行{regulations}合规性检查。

请重点检查以下方面：
1. 访问控制和身份认证
2. 数据安全和加密保护
3. 审计日志和监控
4. 漏洞管理和补丁更新
5. 备份和灾难恢复

输出要求：
- 列出检查项和当前状态
- 指出不符合项和风险等级
- 提供整改建议和时间表
- 引用相关法规条款
"""
    
    @mcp.prompt()
    def executive_summary(scan_results: str) -> str:
        """
        管理层摘要报告提示词模板
        
        Args:
            scan_results: 扫描结果数据
        
        Returns:
            管理层摘要提示词
        """
        return f"""请将以下技术扫描结果转换为管理层可理解的摘要报告：

扫描数据：
{scan_results}

报告要求：
1. 执行摘要（关键发现，3-5点）
2. 风险评级（高/中/低危漏洞数量）
3. 业务影响评估
4. 优先修复建议（Top 5）
5. 资源需求和预算估算
6. 后续行动计划

语言要求：
- 避免过多技术术语
- 突出业务风险
- 提供可操作的决策建议
- 使用图表和列表增强可读性
"""
