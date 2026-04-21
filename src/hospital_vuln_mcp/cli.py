"""Command line interface."""

import argparse
import sys

from ._version import __version__


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Hospital Vulnerability Scanner MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                        # stdio transport (default)
  %(prog)s --transport sse        # SSE on port 8000
  %(prog)s --transport http       # Streamable HTTP (MCP) on port 8000
  %(prog)s --transport sse --port 9000
  %(prog)s --transport sse --host 0.0.0.0 --port 8000   # Docker / 公网暴露
        """,
    )

    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "http"],
        default="stdio",
        help="Transport type",
    )

    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Bind address for SSE / Streamable HTTP (use 0.0.0.0 in container or behind reverse proxy)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for SSE/HTTP transport",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args()

    try:
        from .server import create_server

        if args.transport == "stdio":
            server = create_server()
            server.run(transport="stdio")
        else:
            # FastMCP 在构造时绑定 host/port；run() 不接受 port 参数
            server = create_server(host=args.host, port=args.port)
            if args.transport == "http":
                server.run(transport="streamable-http")
            else:
                server.run(transport="sse")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
