"""命令行入口。

用法::

    pip install mcp
    python -m industrial_ai.mcp_server

启动后以 stdio 传输运行 MCP Server，供 Claude Desktop / Cursor 等客户端连接。
"""

from .server import build_mcp_server


def main() -> None:
    mcp = build_mcp_server()
    mcp.run()


if __name__ == "__main__":
    main()
