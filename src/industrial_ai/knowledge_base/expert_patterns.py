"""专家思维模式：将领域专家的推理方式结构化为可复用的模式。"""

from __future__ import annotations

from typing import Any, Dict


class ExpertPatterns:
    """领域专家思维模式库。

    与 ``feasibility-study.md`` 中描述的专家模式保持一致：
    压力平衡分析、因果链推导、设计意图理解。
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
