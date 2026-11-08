"""液位/质量平衡分析引擎。

专家启发式：容器液位由进出流量平衡决定。
"""

from __future__ import annotations

from ..models import AlertLevel, AnalysisResult, utcnow


class LevelAnalyzer:
    """实现液位系统的质量平衡分析模式。"""

    def analyze(
        self,
        level: float,
        inflow: float,
        outflow: float,
        level_setpoint: float = 50.0,
    ) -> AnalysisResult:
        """分析液位平衡。

        Args:
            level: 当前液位百分比。
            inflow: 入口流量。
            outflow: 出口流量。
            level_setpoint: 目标液位。
        """
        flow_balance = inflow - outflow
        level_deviation = abs(level - level_setpoint)

        # 液位偏离且流量不平衡 → 预警
        if level_deviation > 10 and abs(flow_balance) > 5:
            if flow_balance > 0:
                issue = "Level rising: Inflow exceeds outflow"
                recommendation = "Increase outflow or reduce inflow to maintain level"
            else:
                issue = "Level falling: Outflow exceeds inflow"
                recommendation = "Reduce outflow or increase inflow to maintain level"

            return AnalysisResult(
                timestamp=utcnow(),
                parameter="vessel_level",
                status=AlertLevel.WARNING,
                value=level,
                issue=issue,
                recommendation=recommendation,
                causal_chain=[
                    f"Level at {level:.1f}% (setpoint {level_setpoint}%)",
                    f"Flow imbalance: In {inflow}, Out {outflow}",
                    "Control action required to restore balance",
                ],
            )

        return AnalysisResult(
            timestamp=utcnow(),
            parameter="vessel_level",
            status=AlertLevel.NORMAL,
            value=level,
            recommendation="Level system operating normally",
        )
