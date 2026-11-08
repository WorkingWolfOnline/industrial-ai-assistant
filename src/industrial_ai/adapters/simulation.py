"""仿真适配器：无真实设备时用于开发与测试。

对应工业界「协议仿真 / 设备仿真」的实践——在没有 PLC / DCS 时，
用模拟数据跑通整个分析链路。
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from ..models import ProcessParameter
from .base import DataAdapter


class SimulationAdapter(DataAdapter):
    """基于内存模拟数据的只读适配器。"""

    def __init__(
        self,
        tags: Optional[Dict[str, Dict]] = None,
        read_only: bool = True,
    ):
        self.read_only = read_only
        # 缺省模拟点位（通用示例，非专有数据）
        self._tags: Dict[str, Dict] = tags or {
            "REACTOR_PRESSURE_IN": {"value": 5.2, "normal": (4.5, 5.5), "high": 5.8, "low": 4.2, "unit": "MPa"},
            "REACTOR_PRESSURE_OUT": {"value": 5.0, "normal": (4.3, 5.3), "high": 5.6, "low": 4.0, "unit": "MPa"},
            "VESSEL_LEVEL": {"value": 55.0, "normal": (30.0, 70.0), "high": 80.0, "low": 20.0, "unit": "%"},
            "INLET_FLOW": {"value": 100.0, "normal": (80.0, 120.0), "high": 130.0, "low": 70.0, "unit": "m3/h"},
            "OUTLET_FLOW": {"value": 95.0, "normal": (80.0, 120.0), "high": 130.0, "low": 70.0, "unit": "m3/h"},
            "TEMPERATURE": {"value": 250.0, "normal": (200.0, 300.0), "high": 320.0, "low": 180.0, "unit": "celsius"},
        }

    def set_value(self, tag_name: str, value: float) -> None:
        """更新模拟值（用于测试不同场景）。"""
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
