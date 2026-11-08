# 系统架构（当前实现）

> 本文档描述的是**本仓库实际包含的代码结构**，不是愿景架构。未实现的部分在文末明确列出。

## 概述

本仓库是一个**只读的工业监控分析参考实现**，代码结构如下：

```
MCP 工具服务（9 个工具）
        │
        ▼
分析引擎（压力 / 液位 / 趋势 / 因果，启发式规则）
        │
        ▼
数据适配器（仿真 / OPC UA，只读）
```

---

## 实际组件

### 1. 数据模型（`models.py`）

统一数据结构，贯穿「采集 → 分析 → 建议」全链路：

- `ProcessParameter`：过程参数读数（值、单位、正常区间、报警限、数据质量）
- `AnalysisResult`：分析结果（状态、问题、建议、因果链、置信度）
- `AlertLevel`：告警级别（normal / warning / critical）
- `DataQuality`：数据质量码（GOOD / BAD / UNCERTAIN）

### 2. 分析引擎（`analyzers/`）

四个**启发式规则**分析器（不是专家系统、不是机器学习模型）：

| 分析器 | 规则逻辑（示例） |
| --- | --- |
| `PressureAnalyzer` | 压差为负 → 严重；偏离设计压差 → 预警 |
| `LevelAnalyzer` | 液位偏离且进出流量不平衡 → 预警 |
| `TrendAnalyzer` | 历史序列斜率超阈值 → 预警 |
| `CausalAnalyzer` | 症状 → 可能原因映射 |

> 这些规则是**通用示例**，用于说明「领域知识可以怎样被编码」，不代表真实工艺准确性。

### 3. 知识库（`knowledge_base/`）

- `ExpertPatterns`：几条启发式模式（压力平衡、因果链、设计意图）的**文字描述**
- `EquipmentTemplate`：通用设备模板（reactor / pump / vessel），均为**示例数据**

### 4. 协议适配器（`adapters/`）

- `DataAdapter`：统一只读接口
- `SimulationAdapter`：仿真数据（默认，支持场景切换与故障注入）
- `OPCUAAdapter`：OPC UA 异步接口（可选依赖 `asyncua`，仅骨架）

### 5. MCP 工具服务（`mcp_server/`）

把分析能力封装为 MCP 工具（共 9 个），供 LLM 客户端调用：数据读取、场景切换、压力/液位/趋势/因果分析、设备模板查询、专家模式查询。

---

## 数据流（实际）

```
SimulationAdapter / OPCUAAdapter（只读）
        │  ProcessParameter
        ▼
Analyzers（启发式规则）
        │  AnalysisResult
        ▼
MCP Tools（暴露给 LLM，仅建议）
```

---

## 安全原则

- **只读**：不提供任何写操作工具。
- **人在回路**：所有分析结果仅供建议，需人工确认。
- **安全在硬件**：本仓库不涉及安全仪表系统，AI 不替代安全功能。

---

## 明确未包含的部分

以下内容**不在此仓库中**（可能在早期文档里被描述过，但从未实现）：

- ❌ Composio 集成
- ❌ Modbus / 自定义 API 适配器
- ❌ 数据二极管 / 网关（网络隔离设备）
- ❌ 控制室界面 / 现场端 / Web 仪表盘
- ❌ Redis 缓存、负载均衡、水平扩展
- ❌ LLM 推理接入（本仓库只暴露 MCP 工具，不含 LLM 调用）
- ❌ 真实 DCS/PLC 连接配置

---

## 下一步

1. 阅读 [安全指南](security.md)
2. 阅读 [部署前安全清单](safety-checklist.md)
3. 阅读 [MCP 集成](mcp-integration.md)
4. 阅读 [规则扩展](expert-knowledge.md)
