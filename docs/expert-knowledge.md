# 专家知识嵌入指南

本框架的核心创新是把**领域专家的思维模式**（而非仅数据）结构化为可复用的分析逻辑。本文档说明如何扩展这些知识。

## 专家思维模式

框架内置三类专家思维模式（见 `src/industrial_ai/knowledge_base/expert_patterns.py`）：

1. **压力平衡分析** —— 所有流体系统都是压力平衡问题
2. **因果链推导** —— 症状是结果，要追溯根因
3. **设计意图理解** —— 理解「为什么」，而不只是「是什么」

## 如何扩展分析器

在 `src/industrial_ai/analyzers/` 下新增分析器，实现一个返回 `AnalysisResult` 的方法：

```python
from industrial_ai.models import AnalysisResult, AlertLevel, utcnow

class TemperatureAnalyzer:
    def analyze(self, temperature: float, design_high: float) -> AnalysisResult:
        if temperature > design_high:
            return AnalysisResult(
                timestamp=utcnow(),
                parameter="temperature",
                status=AlertLevel.WARNING,
                value=temperature,
                issue="Temperature exceeds design limit",
                recommendation="Check cooling system",
            )
        return AnalysisResult(
            timestamp=utcnow(),
            parameter="temperature",
            status=AlertLevel.NORMAL,
            value=temperature,
        )
```

然后在 `src/industrial_ai/__init__.py` 与 `analyzers/__init__.py` 中导出。

## 如何扩展知识库

在 `src/industrial_ai/knowledge_base/equipment.py` 的 `EquipmentTemplate` 中新增设备模板：

```python
@staticmethod
def heat_exchanger() -> dict:
    return {
        "common_parameters": [
            {"name": "hot_out_temp", "typical_range": [40, 80], "unit": "celsius"},
        ],
        "common_failure_modes": [
            {"name": "fouling", "symptoms": ["heat_transfer_decline"]},
        ],
    }
```

## 扩展原则

- 只添加**领域无关的通用知识**，不放入专有工业数据（见 README 声明）。
- 分析结果必须携带 `recommendation`（建议）与 `causal_chain`（因果链），便于操作员理解。
