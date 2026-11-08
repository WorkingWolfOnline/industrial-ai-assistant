"""MCP Server：将工业分析能力封装为 LLM 可调用的工具。

安全原则（对齐工业 Agent 最佳实践）：
- 默认只读，不提供任何写操作工具；
- 所有分析结果仅供建议，需人工确认；
- 不直接控制任何 DCS / PLC。
"""

from __future__ import annotations

from typing import List

from ..adapters import SimulationAdapter
from ..analyzers import PressureAnalyzer, LevelAnalyzer, TrendAnalyzer, CausalAnalyzer
from ..knowledge_base import EquipmentTemplate, ExpertPatterns


class IndustrialTools:
    """工业分析工具集（纯函数，不依赖 MCP SDK，可独立使用）。

    基于仿真适配器提供数据读取与分析，全部只读。
    """

    def __init__(self, adapter: SimulationAdapter | None = None):
        self.adapter = adapter or SimulationAdapter(read_only=True)
        self.pressure = PressureAnalyzer()
        self.level = LevelAnalyzer()
        self.trend = TrendAnalyzer()
        self.causal = CausalAnalyzer()

    # --- 数据读取 ---

    def read_parameter(self, tag_name: str) -> dict:
        """读取单个仿真点位（只读）。"""
        p = self.adapter.read_parameter(tag_name)
        if p is None:
            return {"error": f"Unknown tag: {tag_name}"}
        return {
            "name": p.name,
            "value": p.value,
            "unit": p.unit,
            "status": p.status.value,
            "quality": p.quality.value,
        }

    # --- 场景（仿真故障注入） ---

    def list_scenarios(self) -> dict:
        """列出可用的仿真场景。"""
        return {"scenarios": self.adapter.available_scenarios}

    def set_scenario(self, name: str) -> dict:
        """切换仿真场景（模拟不同工况）。"""
        ok = self.adapter.set_scenario(name)
        return {"ok": ok, "scenario": self.adapter.scenario}

    # --- 分析 ---

    def analyze_pressure_system(
        self,
        upstream_pressure: float,
        downstream_pressure: float,
        design_diff: float = 0.2,
    ) -> dict:
        """分析流体系统的压力平衡（只读建议）。"""
        return self.pressure.analyze(upstream_pressure, downstream_pressure, design_diff).to_dict()

    def analyze_level_system(
        self,
        level: float,
        inflow: float,
        outflow: float,
        level_setpoint: float = 50.0,
    ) -> dict:
        """分析容器液位的质量平衡（只读建议）。"""
        return self.level.analyze(level, inflow, outflow, level_setpoint).to_dict()

    def analyze_trend(self, tag_name: str, n: int = 10) -> dict:
        """分析某点位的历史趋势（基于仿真序列）。"""
        history = self.adapter.history(tag_name, n)
        return self.trend.analyze(tag_name, history).to_dict()

    def derive_causal_chain(self, symptom: str) -> dict:
        """根据症状推导可能的因果链。"""
        return self.causal.derive(symptom).to_dict()

    # --- 知识查询 ---

    def get_equipment_template(self, equipment_type: str) -> dict:
        """查询通用设备模板（reactor / pump / vessel）。"""
        return EquipmentTemplate.get(equipment_type)

    def list_expert_patterns(self) -> dict:
        """列出内置的启发式模式（教学示例）。"""
        return ExpertPatterns.all_patterns()


def build_mcp_server() -> "FastMCP":
    """构建 FastMCP 服务器（需要安装 ``mcp`` SDK）。"""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "MCP SDK not installed. Run `pip install mcp` to enable MCP server."
        ) from exc

    mcp = FastMCP("industrial-ai-assistant")
    tools = IndustrialTools()

    @mcp.tool()
    def read_parameter(tag_name: str) -> dict:
        """Read a single simulated process tag (read-only)."""
        return tools.read_parameter(tag_name)

    @mcp.tool()
    def list_scenarios() -> dict:
        """List available simulation scenarios."""
        return tools.list_scenarios()

    @mcp.tool()
    def set_scenario(name: str) -> dict:
        """Switch simulation scenario to inject a fault (simulation only)."""
        return tools.set_scenario(name)

    @mcp.tool()
    def analyze_pressure_system(
        upstream_pressure: float,
        downstream_pressure: float,
        design_diff: float = 0.2,
    ) -> dict:
        """Analyze pressure balance in a fluid system (read-only advice)."""
        return tools.analyze_pressure_system(upstream_pressure, downstream_pressure, design_diff)

    @mcp.tool()
    def analyze_level_system(
        level: float,
        inflow: float,
        outflow: float,
        level_setpoint: float = 50.0,
    ) -> dict:
        """Analyze vessel level mass balance (read-only advice)."""
        return tools.analyze_level_system(level, inflow, outflow, level_setpoint)

    @mcp.tool()
    def analyze_trend(tag_name: str, n: int = 10) -> dict:
        """Analyze the trend of a simulated tag's history (read-only)."""
        return tools.analyze_trend(tag_name, n)

    @mcp.tool()
    def derive_causal_chain(symptom: str) -> dict:
        """Derive possible causal chain from a symptom (read-only)."""
        return tools.derive_causal_chain(symptom)

    @mcp.tool()
    def get_equipment_template(equipment_type: str) -> dict:
        """Get a generic equipment template (reactor/pump/vessel)."""
        return tools.get_equipment_template(equipment_type)

    @mcp.tool()
    def list_expert_patterns() -> dict:
        """List built-in expert thinking patterns (educational)."""
        return tools.list_expert_patterns()

    return mcp
