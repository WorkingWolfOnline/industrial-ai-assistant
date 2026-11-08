"""设备模板：通用设备参数与常见故障模式（不含专有数据）。"""

from __future__ import annotations

from typing import Any, Dict


class EquipmentTemplate:
    """通用设备模板库。"""

    @staticmethod
    def reactor() -> Dict[str, Any]:
        return {
            "common_parameters": [
                {"name": "temperature", "typical_range": [200, 500], "unit": "celsius"},
                {"name": "pressure", "typical_range": [1.0, 10.0], "unit": "bar"},
            ],
            "common_failure_modes": [
                {
                    "name": "temperature_runaway",
                    "symptoms": ["temperature_increasing", "pressure_increasing"],
                    "possible_causes": [
                        "Cooling system failure",
                        "Feed rate increase",
                        "Reaction acceleration",
                    ],
                },
                {
                    "name": "pressure_loss",
                    "symptoms": ["pressure_decreasing", "flow_decreasing"],
                    "possible_causes": [
                        "Downstream blockage",
                        "Leak in system",
                        "Pump performance degradation",
                    ],
                },
            ],
        }

    @staticmethod
    def pump() -> Dict[str, Any]:
        return {
            "common_parameters": [
                {"name": "discharge_pressure", "typical_range": [0.1, 10.0], "unit": "bar"},
                {"name": "flow", "typical_range": [0.0, 100.0], "unit": "m3/h"},
                {"name": "vibration", "typical_range": [0.0, 4.5], "unit": "mm/s"},
            ],
            "common_failure_modes": [
                {
                    "name": "cavitation",
                    "symptoms": ["vibration_high", "noise", "flow_fluctuation"],
                    "possible_causes": ["Low suction pressure", "High fluid temperature", "Blocked suction line"],
                }
            ],
        }

    @staticmethod
    def vessel() -> Dict[str, Any]:
        return {
            "common_parameters": [
                {"name": "level", "typical_range": [20.0, 80.0], "unit": "percent"},
                {"name": "pressure", "typical_range": [0.0, 5.0], "unit": "bar"},
            ],
            "common_failure_modes": [
                {
                    "name": "level_drift",
                    "symptoms": ["level_deviating", "flow_imbalance"],
                    "possible_causes": ["Valve malfunction", "Level transmitter error", "Feed disturbance"],
                }
            ],
        }

    @classmethod
    def get(cls, equipment_type: str) -> Dict[str, Any]:
        """按类型名获取模板（reactor/pump/vessel）。"""
        registry = {
            "reactor": cls.reactor,
            "pump": cls.pump,
            "vessel": cls.vessel,
        }
        factory = registry.get(equipment_type.lower())
        return factory() if factory else {}
