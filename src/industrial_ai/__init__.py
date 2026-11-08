"""Industrial AI Assistant Framework.

面向工业自动化（ICS/DCS）的 AI 助手开源框架，通过 MCP 协议与
协议适配器（OPC UA / 仿真）集成，并嵌入领域专家知识。

安全原则：默认只读，所有建议需人工确认，绝不直接控制 DCS/PLC。
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .models import AlertLevel, AnalysisResult, ProcessParameter
from .analyzers import PressureAnalyzer, LevelAnalyzer, TrendAnalyzer, CausalAnalyzer
from .adapters import DataAdapter, SimulationAdapter
from .knowledge_base import ExpertPatterns, EquipmentTemplate
from .mcp_server import IndustrialTools, build_mcp_server

__version__ = "0.1.0"

__all__ = [
    "AlertLevel",
    "AnalysisResult",
    "ProcessParameter",
    "PressureAnalyzer",
    "LevelAnalyzer",
    "TrendAnalyzer",
    "CausalAnalyzer",
    "DataAdapter",
    "SimulationAdapter",
    "ExpertPatterns",
    "EquipmentTemplate",
    "IndustrialTools",
    "build_mcp_server",
    "MCPClient",
    "ExpertAnalyzer",
]


class MCPClient:
    """工业数据客户端，封装底层协议适配器。

    默认使用仿真适配器（无真实设备时也可运行）；
    传入 ``adapter`` 可接入真实 OPC UA 等协议。
    """

    def __init__(
        self,
        server_url: Optional[str] = None,
        adapter: Optional[DataAdapter] = None,
        read_only: bool = True,
    ):
        self.read_only = read_only
        if adapter is not None:
            self.adapter = adapter
        else:
            # 缺省使用仿真适配器；真实环境可传入 OPCUAAdapter
            self.adapter = SimulationAdapter(read_only=read_only)

    def read_process_data(self, tags: List[str]) -> Dict[str, ProcessParameter]:
        """读取多个过程点位，返回 ``{tag: ProcessParameter}``。"""
        return self.adapter.read_multiple(tags)


class ExpertAnalyzer:
    """高级分析器，聚合各领域专家分析引擎。"""

    def __init__(self):
        self.pressure = PressureAnalyzer()
        self.level = LevelAnalyzer()
        self.trend = TrendAnalyzer()
        self.causal = CausalAnalyzer()

    @classmethod
    def load_knowledge_base(cls, path: Optional[str] = None) -> "ExpertAnalyzer":
        """加载知识库（当前为内置领域无关模板）。

        Args:
            path: 预留参数，未来可指向自定义 YAML 知识库。
        """
        return cls()

    def analyze_pressure(self, upstream: float, downstream: float, design_diff: float = 0.2) -> AnalysisResult:
        return self.pressure.analyze(upstream, downstream, design_diff)

    def analyze_level(self, level: float, inflow: float, outflow: float, setpoint: float = 50.0) -> AnalysisResult:
        return self.level.analyze(level, inflow, outflow, setpoint)
