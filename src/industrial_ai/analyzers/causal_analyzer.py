"""因果链推导引擎。

专家启发式：症状是结果，要追溯根因。提供从症状到根因的推导方法。
"""

from __future__ import annotations

from typing import Dict, List

from ..models import AnalysisResult, AlertLevel, utcnow


class CausalAnalyzer:
    """根据症状与已知依赖关系推导因果链。"""

    # 通用症状 → 可能原因 映射（领域无关的启发式）
    _symptom_causes: Dict[str, List[str]] = {
        "pressure_decreasing": ["Downstream blockage", "Leak in system", "Pump degradation"],
        "pressure_increasing": ["Upstream valve opening", "Pump overspeed", "Blockage downstream"],
        "level_rising": ["Inflow exceeds outflow", "Outlet valve closed", "Pump failure downstream"],
        "level_falling": ["Outflow exceeds inflow", "Inlet valve closed", "Leak in vessel"],
        "temperature_rising": ["Cooling failure", "Feed rate increase", "Reaction acceleration"],
    }

    def derive(self, symptom: str) -> AnalysisResult:
        """从单个症状推导可能的因果链。

        Args:
            symptom: 症状描述键（见 ``_symptom_causes``）。
        """
        causes = self._symptom_causes.get(
            symptom, ["Unknown cause - manual investigation required"]
        )
        chain = [
            f"Symptom: {symptom}",
            "Possible causes: " + ", ".join(causes),
            "Recommended: Verify with additional data points and trends",
        ]
        return AnalysisResult(
            timestamp=utcnow(),
            parameter=symptom,
            status=AlertLevel.WARNING,
            value=0.0,
            issue=f"Root cause investigation for {symptom}",
            recommendation="Trace upstream dependencies and verify with trends",
            causal_chain=chain,
            source="causal",
        )
