"""压力平衡分析引擎（启发式规则，非专家系统）。

启发式：所有流体系统本质都是压力平衡问题。
"""

from __future__ import annotations

from typing import Optional

from ..models import AlertLevel, AnalysisResult, utcnow


class PressureAnalyzer:
    """实现压力系统的启发式分析规则（教育示例）。"""

    def analyze(
        self,
        upstream_pressure: float,
        downstream_pressure: float,
        design_diff: float = 0.2,
    ) -> AnalysisResult:
        """分析压力平衡。

        Args:
            upstream_pressure: 系统入口压力（MPa）。
            downstream_pressure: 系统出口压力（MPa）。
            design_diff: 设计压差（MPa）。
        """
        pressure_diff = upstream_pressure - downstream_pressure

        # 规则 1：出现负压差 → 严重异常
        if pressure_diff < 0:
            return AnalysisResult(
                timestamp=utcnow(),
                parameter="pressure_differential",
                status=AlertLevel.CRITICAL,
                value=pressure_diff,
                issue="Negative pressure differential detected",
                recommendation=(
                    "Check pump operation and upstream blockages. "
                    "Verify pressure transmitter calibration."
                ),
                causal_chain=[
                    "Negative pressure differential observed",
                    "Possible causes: Pump failure, upstream blockage, or transmitter error",
                    "Immediate action: Verify pump status and inlet conditions",
                ],
            )

        # 规则 2：偏离设计压差 → 预警
        deviation = abs(pressure_diff - design_diff)
        if deviation > 0.1:
            return AnalysisResult(
                timestamp=utcnow(),
                parameter="pressure_differential",
                status=AlertLevel.WARNING,
                value=pressure_diff,
                issue=f"Pressure differential deviation: {deviation:.2f} MPa",
                recommendation=(
                    f"Expected {design_diff} MPa, actual {pressure_diff:.2f} MPa. "
                    "Check for fouling, valve position, or flow changes."
                ),
                causal_chain=[
                    f"Pressure differential {pressure_diff:.2f} MPa vs design {design_diff} MPa",
                    "Possible causes: Fouling, partial blockage, or valve malfunction",
                    "Recommended: Inspect filters and valve positions",
                ],
            )

        return AnalysisResult(
            timestamp=utcnow(),
            parameter="pressure_differential",
            status=AlertLevel.NORMAL,
            value=pressure_diff,
            recommendation="Pressure system operating normally",
        )
