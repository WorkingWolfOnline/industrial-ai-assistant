"""MCP Server：将工业分析能力封装为 LLM 可调用的工具。

安全原则（对齐工业 Agent 最佳实践）：
- 默认只读，不提供任何写操作；
- 所有分析结果仅供建议，需人工确认；
- 不直接控制任何 DCS / PLC。
"""

from __future__ import annotations

from ..analyzers import PressureAnalyzer, LevelAnalyzer
from ..models import AnalysisResult


class IndustrialTools:
    """工业分析工具集（纯函数，不依赖 MCP SDK，可独立使用）。"""

    def __init__(self):
        self.pressure_analyzer = PressureAnalyzer()
        self.level_analyzer = LevelAnalyzer()

    def analyze_pressure_system(
        self,
        upstream_pressure: float,
        downstream_pressure: float,
        design_diff: float = 0.2,
    ) -> dict:
        """分析流体系统的压力平衡。"""
        return self.pressure_analyzer.analyze(
            upstream_pressure, downstream_pressure, design_diff
        ).to_dict()

    def analyze_level_system(
        self,
        level: float,
        inflow: float,
        outflow: float,
        level_setpoint: float = 50.0,
    ) -> dict:
        """分析容器液位的质量平衡。"""
        return self.level_analyzer.analyze(
            level, inflow, outflow, level_setpoint
        ).to_dict()


def build_mcp_server() -> "FastMCP":
    """构建 FastMCP 服务器（需要安装 ``mcp`` SDK）。

    通过 ``mcp`` 的 FastMCP 装饰器把分析函数暴露为 MCP 工具，
    供 Claude Desktop / Cursor 等客户端调用。
    """
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "MCP SDK not installed. Run `pip install mcp` to enable MCP server."
        ) from exc

    mcp = FastMCP("industrial-ai-assistant")
    tools = IndustrialTools()

    @mcp.tool()
    def analyze_pressure_system(
        upstream_pressure: float,
        downstream_pressure: float,
        design_diff: float = 0.2,
    ) -> dict:
        """Analyze pressure balance in a fluid system (read-only)."""
        return tools.analyze_pressure_system(
            upstream_pressure, downstream_pressure, design_diff
        )

    @mcp.tool()
    def analyze_level_system(
        level: float,
        inflow: float,
        outflow: float,
        level_setpoint: float = 50.0,
    ) -> dict:
        """Analyze vessel level mass balance (read-only)."""
        return tools.analyze_level_system(level, inflow, outflow, level_setpoint)

    return mcp
