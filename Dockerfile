# Hospital Vulnerability Scanner MCP Server Docker Image
FROM python:3.11-slim

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY pyproject.toml .
COPY README.md .
COPY LICENSE .
COPY src/ ./src/

# 安装Python依赖
RUN pip install --no-cache-dir -e .

# 清理
RUN apt-get purge -y --auto-remove gcc

# 暴露端口（SSE模式）
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from hospital_vuln_mcp.server import create_server; print('OK')" || exit 1

# 与 modelscope.yaml deploy 一致：SSE + 监听所有网卡（便于端口映射 / 反代）
# 仅需 stdio 时：docker run ... python -m hospital_vuln_mcp
CMD ["python", "-m", "hospital_vuln_mcp", "--transport", "sse", "--port", "8000", "--host", "0.0.0.0"]
