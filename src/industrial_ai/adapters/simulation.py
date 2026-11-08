"""仿真适配器：无真实设备时用于开发与测试。

对应工业界「协议仿真 / 设备仿真」的实践——在没有 PLC / DCS 时，
用模拟数据跑通整个分析链路，并可注入故障场景验证异常检测。
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from ..models import ProcessParameter
from .base import DataAdapter


class SimulationAdapter(DataAdapter):
    """基于内存模拟数据的只读适配器，支持故障场景切换。

    所有数值均为**通用示例**，不代表任何真实工艺参数。
    """

    # 预定义场景（通用示例点位，非真实工艺数据）
    _SCENARIOS: Dict[str, Dict[str, Dict]] = {
        "normal": {
            "REACTOR_PRESSURE_IN": {"value": 5.2, "normal": (4.5, 5.5), "high": 5.8, "low": 4.2, "unit": "MPa"},
            "REACTOR_PRESSURE_OUT": {"value": 5.0, "normal": (4.3, 5.3), "high": 5.6, "low": 4.0, "unit": "MPa"},
            "VESSEL_LEVEL": {"value": 55.0, "normal": (30.0, 70.0), "high": 80.0, "low": 20.0, "unit": "%"},
            "INLET_FLOW": {"value": 100.0, "normal": (80.0, 120.0), "high": 130.0, "low": 70.0, "unit": "m3/h"},
            "OUTLET_FLOW": {"value": 100.0, "normal": (80.0, 120.0), "high": 130.0, "low": 70.0, "unit": "m3/h"},
            "TEMPERATURE": {"value": 250.0, "normal": (200.0, 300.0), "high": 320.0, "low": 180.0, "unit": "celsius"},
        },
        # 压力异常：出口压力高于入口（负压差 → 严重）
        "pressure_fault": {
            "REACTOR_PRESSURE_IN": {"value": 4.6, "normal": (4.5, 5.5), "high": 5.8, "low": 4.2, "unit": "MPa"},
            "REACTOR_PRESSURE_OUT": {"value": 5.4, "normal": (4.3, 5.3), "high": 5.6, "low": 4.0, "unit": "MPa"},
            "VESSEL_LEVEL": {"value": 55.0, "normal": (30.0, 70.0), "high": 80.0, "low": 20.0, "unit": "%"},
            "INLET_FLOW": {"value": 100.0, "normal": (80.0, 120.0), "high": 130.0, "low": 70.0, "unit": "m3/h"},
            "OUTLET_FLOW": {"value": 100.0, "normal": (80.0, 120.0), "high": 130.0, "low": 70.0, "unit": "m3/h"},
            "TEMPERATURE": {"value": 250.0, "normal": (200.0, 300.0), "high": 320.0, "low": 180.0, "unit": "celsius"},
        },
        # 液位异常：进大于出且液位偏高（→ 预警）
        "level_fault": {
            "REACTOR_PRESSURE_IN": {"value": 5.2, "normal": (4.5, 5.5), "high": 5.8, "low": 4.2, "unit": "MPa"},
            "REACTOR_PRESSURE_OUT": {"value": 5.0, "normal": (4.3, 5.3), "high": 5.6, "low": 4.0, "unit": "MPa"},
            "VESSEL_LEVEL": {"value": 68.0, "normal": (30.0, 70.0), "high": 80.0, "low": 20.0, "unit": "%"},
            "INLET_FLOW": {"value": 118.0, "normal": (80.0, 120.0), "high": 130.0, "low": 70.0, "unit": "m3/h"},
            "OUTLET_FLOW": {"value": 90.0, "normal": (80.0, 120.0), "high": 130.0, "low": 70.0, "unit": "m3/h"},
            "TEMPERATURE": {"value": 250.0, "normal": (200.0, 300.0), "high": 320.0, "low": 180.0, "unit": "celsius"},
        },
    }

    def __init__(self, read_only: bool = True, scenario: str = "normal"):
        self.read_only = read_only
        self.scenario = scenario
        self._tags: Dict[str, Dict] = {
            k: dict(v) for k, v in self._SCENARIOS[scenario].items()
        }

    @property
    def available_scenarios(self) -> List[str]:
        return list(self._SCENARIOS.keys())

    def set_scenario(self, name: str) -> bool:
        """切换到预定义场景（故障注入）。"""
        if name not in self._SCENARIOS:
            return False
        self.scenario = name
        self._tags = {k: dict(v) for k, v in self._SCENARIOS[name].items()}
        return True

    def set_value(self, tag_name: str, value: float) -> None:
        """手动更新单个点位值（用于测试任意场景）。"""
        if tag_name in self._tags:
            self._tags[tag_name]["value"] = value

    def read_parameter(self, tag_name: str) -> Optional[ProcessParameter]:
        cfg = self._tags.get(tag_name)
        if cfg is None:
            return None
        return ProcessParameter(
            name=tag_name,
            value=cfg["value"],
            unit=cfg.get("unit", "GENERIC"),
            timestamp=datetime.now(),
            normal_range=cfg["normal"],
            alarm_high=cfg.get("high"),
            alarm_low=cfg.get("low"),
        )

    def history(self, tag_name: str, n: int = 10, step_seconds: int = 5) -> List[float]:
        """生成一段历史序列（当前值附近轻微波动），供趋势分析使用。

        这是**仿真数据**，仅用于演示趋势分析的输入形态。
        """
        cfg = self._tags.get(tag_name)
        if cfg is None:
            return []
        base = cfg["value"]
        lo, hi = cfg["normal"]
        span = (hi - lo) * 0.02  # 波动幅度为量程的 2%
        rng = random.Random(hash(tag_name) & 0xFFFF)
        return [
            round(max(lo, min(hi, base + rng.uniform(-span, span))), 3)
            for _ in range(n)
        ]
