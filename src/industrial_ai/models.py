"""统一数据模型。

所有分析模块、协议适配器与 MCP 工具都使用这里定义的结构，
保证数据在「采集 → 分析 → 建议 → 上报」链路中保持一致的形态。
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class AlertLevel(str, Enum):
    """告警级别。"""

    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"


class DataQuality(str, Enum):
    """数据质量码（对应工业数据质量标识）。"""

    GOOD = "GOOD"
    BAD = "BAD"
    UNCERTAIN = "UNCERTAIN"


def utcnow() -> datetime:
    """返回带时区信息的当前时间，便于日志与审计。"""
    return datetime.now(timezone.utc)


@dataclass
class ProcessParameter:
    """一个过程参数的实时读数。

    Attributes:
        name: 参数名（如 ``REACTOR_PRESSURE_IN``）。
        value: 当前值。
        unit: 单位（如 ``MPa``、``°C``）。
        timestamp: 采样时间。
        normal_range: ``(min, max)`` 正常区间。
        alarm_high / alarm_low: 高高/低低报警限。
        quality: 数据质量（``GOOD`` / ``BAD``），对应工业数据质量码。
        writable: 该点位是否可写。框架默认只读，此字段仅用于标识。
    """

    name: str
    value: float
    unit: str
    timestamp: datetime
    normal_range: tuple = (0.0, 100.0)
    alarm_high: Optional[float] = None
    alarm_low: Optional[float] = None
    quality: DataQuality = DataQuality.GOOD
    writable: bool = False

    @property
    def status(self) -> AlertLevel:
        """根据数值与报警限判定状态。"""
        if self.quality == DataQuality.BAD:
            return AlertLevel.CRITICAL
        if self.alarm_high is not None and self.value > self.alarm_high:
            return AlertLevel.CRITICAL
        if self.alarm_low is not None and self.value < self.alarm_low:
            return AlertLevel.CRITICAL
        lo, hi = self.normal_range
        if not (lo <= self.value <= hi):
            return AlertLevel.WARNING
        return AlertLevel.NORMAL


@dataclass
class AnalysisResult:
    """分析结果，供控制室与现场端展示。"""

    timestamp: datetime
    parameter: str
    status: AlertLevel
    value: float
    issue: Optional[str] = None
    recommendation: Optional[str] = None
    causal_chain: Optional[List[str]] = None
    confidence: float = 1.0
    source: str = "expert"

    @property
    def has_anomaly(self) -> bool:
        return self.status != AlertLevel.NORMAL

    def to_dict(self) -> Dict[str, Any]:
        """序列化为可 JSON 化的字典（供 MCP / 上报使用）。"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "parameter": self.parameter,
            "status": self.status.value,
            "value": self.value,
            "issue": self.issue,
            "recommendation": self.recommendation,
            "causal_chain": self.causal_chain or [],
            "confidence": self.confidence,
            "source": self.source,
        }
