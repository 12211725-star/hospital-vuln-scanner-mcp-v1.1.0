# Hospital Vuln MCP 改造说明

## 基于魔搭 MCP 开发规范的改造

### 改造时间
2026-04-21

---

## 主要改造内容

### 1. 项目结构规范化

```
hospital-vuln-mcp-v2/
├── mcp_config.json              ✅ 新增：魔搭MCP配置文件
├── modelscope.yaml              ✅ 更新：符合规范的部署配置
├── pyproject.toml               ✅ 更新：完善项目元数据
├── Dockerfile                   ✅ 更新：添加健康检查
├── README.md / README_CN.md     ✅ 已有：保持不动
├── src/
│   └── hospital_vuln_mcp/
│       ├── __init__.py          ✅ 更新：完善文档
│       ├── server.py            ✅ 重写：简洁主入口
│       ├── _version.py          ✅ 已有：版本信息
│       ├── models.py            ✅ 新增：Pydantic模型定义
│       ├── tools/               ✅ 新增：工具模块目录
│       │   ├── __init__.py
│       │   ├── scan_tools.py    ✅ 扫描管理工具（4个）
│       │   ├── vuln_tools.py    ✅ 漏洞管理工具（3个）
│       │   ├── network_tools.py ✅ 网络工具（3个）
│       │   ├── report_tools.py  ✅ 报告工具（2个）
│       │   └── system_tools.py  ✅ 系统工具（2个）
│       ├── resources/           ✅ 新增：资源模块目录
│       │   ├── __init__.py
│       │   └── app_resources.py ✅ 应用资源（3个）
│       └── prompts/             ✅ 新增：提示词模块目录
│           ├── __init__.py
│           └── scan_prompts.py  ✅ 提示词模板（4个）
└── tests/                       ✅ 新增：测试目录
    ├── __init__.py
    └── test_tools.py            ✅ 基础测试用例
```

---

## 符合规范的关键点

### ✅ 1. mcp_config.json
- 符合规范的服务配置格式
- 包含中英文名称和描述
- 定义服务类型为 stdio

### ✅ 2. 工具命名规范
- 使用 snake_case 命名
- 符合 `verb_noun` 格式
- 如：`start_scan`, `list_vulnerabilities`

### ✅ 3. 工具描述规范
- 详细的文档字符串
- 包含功能说明、使用场景、参数说明
- 提供使用示例

### ✅ 4. Pydantic 类型定义
- 所有输入输出使用 Pydantic 模型
- 明确定义字段类型和描述
- 支持复杂的嵌套结构

### ✅ 5. 资源和提示词模板
- 新增 Resource 功能（config://app-info 等）
- 新增 Prompt 模板（vulnerability_analysis 等）
- 符合 MCP 协议完整功能

### ✅ 6. 安全考虑
- 输入参数验证
- 状态值有效性检查
- 错误信息脱敏

### ✅ 7. 测试规范
- 创建 tests/ 目录
- 添加基础测试用例
- 符合 pytest 规范

### ✅ 8. Docker 部署
- 完善 Dockerfile
- 添加健康检查
- 优化镜像大小

---

## 工具列表（14个）

### 扫描管理（4个）
1. `start_scan` - 启动漏洞扫描
2. `get_scan_status` - 查询扫描状态
3. `list_scans` - 列出扫描任务
4. `cancel_scan` - 取消扫描

### 漏洞管理（3个）
5. `list_vulnerabilities` - 列出漏洞
6. `get_vulnerability` - 获取漏洞详情
7. `update_vulnerability_status` - 更新漏洞状态

### 网络工具（3个）
8. `discover_network` - 网络发现
9. `scan_host_ports` - 端口扫描
10. `identify_medical_systems` - 识别医疗系统

### 报告工具（2个）
11. `generate_report` - 生成报告
12. `list_reports` - 列出报告

### 系统工具（2个）
13. `get_vuln_stats` - 漏洞统计
14. `get_system_status` - 系统状态

---

## 资源列表（3个）

1. `config://app-info` - 应用信息
2. `config://scan-profiles` - 扫描配置说明
3. `docs://severity-levels` - 严重程度分级

---

## 提示词模板（4个）

1. `vulnerability_analysis` - 漏洞分析
2. `scan_planning` - 扫描规划
3. `compliance_check` - 合规性检查
4. `executive_summary` - 管理层摘要

---

## 部署方式

### 方式1：Docker 部署（推荐）
```bash
docker build -t hospital-vuln-mcp .
docker run -p 8000:8000 hospital-vuln-mcp
```

### 方式2：Python 直接运行
```bash
pip install -e .
python -m hospital_vuln_mcp
```

### 方式3：uvx 运行
```bash
uvx hospital-vuln-mcp
```

---

## 文件大小

最终打包：`hospital-vuln-mcp-final.zip` (28.29 KB)

---

## 后续建议

1. **发布到 PyPI**：便于用户通过 pip/uvx 安装
2. **完善测试**：添加更多单元测试和集成测试
3. **CI/CD**：添加 GitHub Actions 自动测试和发布
4. **文档完善**：添加 API 文档和使用教程
5. **实际漏洞库**：接入真实的漏洞检测能力

---

**改造完成！** ✅
