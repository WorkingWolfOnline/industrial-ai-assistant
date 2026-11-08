"""启发式模式：将几条通用推理规则结构化为可复用的模式（非专家系统）。"""

from __future__ import annotations

from typing import Any, Dict


class ExpertPatterns:
    """通用启发式模式库（类名沿用历史，内容为示例规则）。

    提供压力平衡、因果链、设计意图三类启发式描述，
    均为通用示例，不代表真实工艺准确性。
    """

    @staticmethod
    def pressure_analysis() -> Dict[str, Any]:
        """压力平衡分析模式。"""
        return {
            "description": "All fluid systems are pressure balance problems",
            "rules": [
                "Low pressure cannot feed high pressure systems",
                "Pressure differential indicates flow resistance",
                "Sudden pressure drops indicate blockages",
            ],
        }

    @staticmethod
    def causal_chain() -> Dict[str, Any]:
        """因果链推导模式。"""
        return {
            "description": "Derive root causes from symptoms",
            "methodology": [
                "Identify observable symptoms",
                "Trace upstream dependencies",
                "Identify common cause factors",
                "Verify with multiple data points",
            ],
        }

    @staticmethod
    def design_intent() -> Dict[str, Any]:
        """设计意图理解模式：理解「为什么」，而不只是「是什么」。"""
        return {
            "description": "Understand WHY, not just WHAT",
            "example": {
                "component": "Pressure Vessel",
                "design_intent": {
                    "purpose": "Maintain pressure boundary between systems",
                    "key_parameters": {
                        "design_pressure": (
                            "Determined by maximum expected operating pressure "
                            "+ safety margin"
                        ),
                        "relief_valve_setpoint": "Set at 110% of design pressure",
                    },
                    "safety_considerations": [
                        "Never exceed MAWP (Maximum Allowable Working Pressure)",
                        "Regular inspection of pressure relief devices",
                        "Monitor for corrosion and erosion",
                    ],
                },
            },
        }

    @classmethod
    def all_patterns(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "pressure_analysis": cls.pressure_analysis(),
            "causal_chain": cls.causal_chain(),
            "design_intent": cls.design_intent(),
        }
