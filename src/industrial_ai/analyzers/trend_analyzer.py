"""趋势分析引擎。

专家启发式：关注参数的变化率，而非仅关注瞬时值。
"""

from __future__ import annotations

from typing import List, Optional

from ..models import AlertLevel, AnalysisResult, utcnow


class TrendAnalyzer:
    """检测参数变化趋势（斜率）是否异常。"""

    def analyze(
        self,
        parameter: str,
        history: List[float],
        max_slope: Optional[float] = None,
        unit: str = "",
    ) -> AnalysisResult:
        """分析历史序列的变化趋势。

        Args:
            parameter: 参数名。
            history: 时间上等间隔的采样序列（至少 2 个点）。
            max_slope: 允许的最大斜率（单位：值/采样间隔），缺省按历史推算。
        """
        if len(history) < 2:
            return AnalysisResult(
                timestamp=utcnow(),
                parameter=parameter,
                status=AlertLevel.NORMAL,
                value=history[-1] if history else 0.0,
                recommendation="Insufficient history for trend analysis",
            )

        slope = history[-1] - history[0]

        # 缺省阈值：按历史绝对变化量的 3 倍作为异常斜率
        if max_slope is None:
            max_abs = max(abs(history[-1] - history[0]), 1e-6)
            max_slope = max_abs * 3.0

        value = history[-1]
        if abs(slope) > abs(max_slope):
            direction = "rising" if slope > 0 else "falling"
            return AnalysisResult(
                timestamp=utcnow(),
                parameter=parameter,
                status=AlertLevel.WARNING,
                value=value,
                issue=f"Abnormal trend: {parameter} {direction} rapidly",
                recommendation=(
                    f"Slope {slope:.2f} exceeds threshold {max_slope:.2f}. "
                    "Verify process stability and upstream conditions."
                ),
                causal_chain=[
                    f"{parameter} moved from {history[0]:.2f} to {history[-1]:.2f}",
                    f"Slope {slope:.2f} exceeds limit {max_slope:.2f}",
                    "Recommended: Check for process disturbance or sensor drift",
                ],
            )

        return AnalysisResult(
            timestamp=utcnow(),
            parameter=parameter,
            status=AlertLevel.NORMAL,
            value=value,
            recommendation="Trend is within normal bounds",
        )
