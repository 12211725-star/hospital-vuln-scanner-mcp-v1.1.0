# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-04-22

### Changed

- 🔧 **API 改进**: `scan_host_ports` 的 `ports` 参数从 `str` 改为 `list[int]`
  - 旧: `ports='22,80,443'` (字符串)
  - 新: `ports=[22, 80, 443]` (数组，更符合 JSON 调用习惯)
- 🔧 **API 改进**: `identify_medical_systems` 新增可选 `ports` 参数
  - 支持 `identify_medical_systems(target='192.168.0.106', ports=[80, 443, 3306])`
  - 不填 `ports` 则自动扫描常见端口（向后兼容）

### Fixed

- 🐛 修复 AI 助手调用时参数名不匹配导致的验证错误
- 🐛 修复用户传入 `[80, 443]` 数组时工具期望字符串的问题

## [1.1.9] - 2026-04-22

### Fixed

- 🐛 **关键修复**: nmap/nuclei 路径检测改为延迟检测（每次扫描时检测）
  - 问题: uvx 环境中 import 时 PATH 未设置好，导致模块级变量 `NMAP_AVAILABLE` 永远为 `False`
  - 修复: 改为每次扫描时调用 `_find_tool()` 重新检测路径
  - 新增更多常见路径: `/opt/homebrew/bin`, `/home/linuxbrew/.linuxbrew/bin`

## [1.1.8] - 2026-04-22

### Fixed

- 🐛 修复 nmap/nuclei 路径检测，新增 `_find_tool()` 函数搜索多路径
- 🐛 支持环境变量 `NMAP_PATH` / `NUCLEI_PATH` 指定路径

## [1.1.7] - 2026-04-22

### Changed

- 🔧 按魔搭 MCP 开发规范修改 `pyproject.toml`:
  - 版本号改用 `dynamic = ['version']`（从 `_version.py` 读取）
  - 添加 `[tool.hatch.version] path` 指向 `_version.py`
  - 添加 `httpx[http2]>=0.27.0` 依赖（SSE/HTTP 传输需要）
  - `[project.scripts]` 键名改为 `hospital-vuln-mcp`（与包名一致）

### Added

- 📝 新增 `.env.example` 环境变量示例文件
- 🔧 `__init__.py` 添加 `create_mcp_server` 别名

## [1.1.6] - 2026-04-22

### Fixed

- 🐛 改回 stdio 协议（与魔搭官方一致）
- 🐛 README mcpServers 用 `command` + `args` 格式，不再用 `url`

## [1.1.5] - 2026-04-21

### Fixed

- 🐛 README mcpServers 添加 `env` 字段
- 🐛 mcp.json name 改为 `hospital-vuln-mcp`（与 PyPI 包名一致）
- 🐛 统一所有文件版本号为 1.1.5

## [1.1.4] - 2026-04-21

### Fixed

- 🐛 修复魔搭 README 格式：单一 mcpServers JSON 块
- 🐛 添加 LICENSE 文件

## [1.1.3] - 2026-04-21

### Fixed

- 🐛 修复 README 中 PyPI 包名错误（hospital-vuln-scanner-mcp → hospital-vuln-mcp）
- 🐛 修复魔搭不可部署问题（包名与 PyPI 不一致）

## [1.1.2] - 2026-04-22

### Changed

- 🔧 GitHub 仓库名改为 `hospital-vuln-scanner-mcp`（更规范）
- 🔧 更新所有文档中的 GitHub 链接

## [1.1.1] - 2026-04-22

### Added

- 📝 完善使用方法文档，添加场景化示例
- 📝 新增提示词指南（安全评估、定期巡检、等保合规、应急响应、资产盘点）
- 📝 新增扫描引擎说明（nmap/nuclei 自动检测机制）
- 📝 新增内置漏洞检测规则文档
- 📝 新增医疗系统指纹识别说明

### Changed

- 📝 README.md 重构为更完整的使用指南
- 📝 README_CN.md 中文版同步更新

## [1.1.0] - 2026-04-21

### Added

- ✨ 新增 `scanner.py` 真实扫描引擎
- ✨ 新增 nmap/nuclei 自动检测，有则用，没有自动回退到 Python
- ✨ 新增 Python 原生端口扫描（socket 多线程）
- ✨ 新增内置漏洞检测规则（MySQL/Redis/MongoDB/RDP 暴露检测）
- ✨ 新增医疗系统指纹识别（HIS/PACS/LIS/RIS/EMR）
- ✨ 新增 HTTP Banner 识别和厂商检测

### Changed

- 🔧 `start_scan` 现在返回真实扫描结果而非 Mock 数据
- 🔧 `scan_host_ports` 支持真实端口探测
- 🔧 `identify_medical_systems` 支持基于 Banner 的系统识别
- 🔧 `get_system_status` 显示 nmap/nuclei 可用状态

### Fixed

- 🐛 修复扫描任务创建后永远卡在 `running 0%` 的问题
- 🐛 修复扫描不执行任何实际检测的问题

## [1.0.0] - 2026-04-21

### Added

- 🎉 初始发布
- ✨ 14 个 MCP 工具（扫描管理、漏洞管理、网络工具、报告工具、系统工具）
- ✨ FastMCP 框架集成
- ✨ 支持 stdio/sse/http 三种传输模式
- ✨ 魔搭 MCP 广场上架
- ✨ PyPI 发布

---

## 版本说明

### 版本号格式

- **主版本号 (Major)**: 重大架构变更或不兼容更新
- **次版本号 (Minor)**: 新增功能，保持向下兼容
- **修订号 (Patch)**: Bug 修复和小改进

### 变更类型图标

| 图标 | 类型 | 说明 |
|------|------|------|
| ✨ | Added | 新增功能 |
| 🔧 | Changed | 功能变更 |
| 🐛 | Fixed | Bug 修复 |
| 📝 | Docs | 文档更新 |
| 🔒 | Security | 安全相关 |
| ⚠️ | Deprecated | 即将废弃 |
| 🗑️ | Removed | 已移除 |
