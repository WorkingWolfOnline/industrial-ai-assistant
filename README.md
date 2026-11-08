# Industrial AI Assistant Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

> 一个**研究 / 概念验证**框架，探索如何通过 MCP 协议把「AI 辅助」引入工业监控场景。

> ⚠️ **这是一个教学级参考实现，不是生产系统。**

[English](#english) | [中文](#中文)

---

## <a name="english"></a>English

### ⚠️ Safety Statement (Read First)

This project is a **learning and research** effort. It does **not**:

- ❌ Control any DCS / PLC / industrial process
- ❌ Contain production-ready code, real tag lists, or real process data
- ❌ Replace safety instrumented systems, operators, or engineering judgment

It **only** demonstrates, in a simulated environment:

- ✅ Read-only monitoring and rule-based analysis
- ✅ How to expose analysis tools to an LLM over MCP
- ✅ How a "read-only + human-in-the-loop" boundary should look

> **AI must never directly control industrial processes.** Safety functions belong in hardware (safety relays / safety PLCs). Every AI output is a suggestion, not an authority.

### What This Project Is

A minimal reference implementation showing how to structure an LLM-based assistant for industrial monitoring:

1. **Rule-based analysis** (not a real "expert system") — a few heuristic rules for pressure balance and level balance, meant to illustrate *how* domain knowledge could be encoded, not to be accurate.
2. **Protocol adapters** — a unified read interface, with a simulation adapter (no hardware needed) and an optional OPC UA adapter.
3. **MCP tool server** — exposes the analysis functions as MCP tools so an LLM client can call them.
4. **Simulated fault scenarios** — to demonstrate anomaly detection in a safe, offline way.

### What "Domain Expert Digital Human" Means Here

The original idea was an "engineer-experienced digital human" that assists plant operators in real time. This repository implements only the **smallest, honest slice** of that vision: a set of hard-coded heuristic rules. A real implementation would require much more (knowledge graphs, RAG over verified notes, validated process models) — none of which are included here.

### Architecture (Actual, Not Aspirational)

```
┌───────────────────────────────────────────┐
│            MCP Tool Server                 │
│  (exposes analyzers to an LLM, read-only)  │
└──────────────────┬────────────────────────┘
                   │
┌──────────────────▼────────────────────────┐
│           Analysis Engines                 │
│  pressure / level / trend / causal         │
│  (heuristic rules, educational only)       │
└──────────────────┬────────────────────────┘
                   │
┌──────────────────▼────────────────────────┐
│           Data Adapters                    │
│  SimulationAdapter (default)               │
│  OPCUAAdapter (optional, async, read-only) │
└───────────────────────────────────────────┘
```

### Quick Start

```bash
git clone https://github.com/WorkingWolfOnline/industrial-ai-assistant.git
cd industrial-ai-assistant

# 核心框架基于 Python 标准库，无需第三方依赖即可运行
python examples/chemical_process/demo.py --report
```

See [docs/](docs/) for details:

- [architecture.md](docs/architecture.md) — system architecture
- [feasibility-study.md](docs/feasibility-study.md) — feasibility analysis
- [security.md](docs/security.md) — security principles
- [safety-checklist.md](docs/safety-checklist.md) — pre-deployment checklist
- [mcp-integration.md](docs/mcp-integration.md) — MCP integration
- [expert-knowledge.md](docs/expert-knowledge.md) — how to extend the rules

### Project Structure

```
industrial-ai-assistant/
├── docs/                       # Documentation
├── src/industrial_ai/          # Main package
│   ├── models.py               # Unified data models
│   ├── analyzers/              # Heuristic analysis engines
│   ├── knowledge_base/         # Example equipment templates
│   ├── adapters/               # Simulation + OPC UA adapters
│   └── mcp_server/             # MCP tool server
├── examples/chemical_process/  # Runnable demo
├── pyproject.toml
└── requirements.txt
```

### License

MIT License. See [LICENSE](LICENSE).

---

## <a name="中文"></a>中文

### ⚠️ 安全声明（务必先读）

这是一个**学习与研究**项目，**不**包含：

- ❌ 对任何 DCS / PLC / 工业过程的控制
- ❌ 生产就绪代码、真实点位表、真实工艺数据
- ❌ 替代安全仪表系统、操作员或工程判断

它只在**仿真环境**中演示：

- ✅ 只读监控与基于规则的分析
- ✅ 如何把分析工具通过 MCP 暴露给大模型
- ✅ 「只读 + 人在回路」的边界应该长什么样

> **AI 绝不能直接控制工业过程。** 安全功能属于硬件（安全继电器 / 安全 PLC）。任何 AI 输出都只是建议，不是权威。

### 这个项目是什么

一个最小化的参考实现，展示如何为工业监控构建基于 LLM 的助手：

1. **基于规则的分析**（不是真正的「专家系统」）—— 几条压力平衡 / 液位平衡的启发式规则，用于说明领域知识「可以怎样被编码」，而不是保证准确。
2. **协议适配器** —— 统一只读接口，含仿真适配器（无需硬件）与可选的 OPC UA 适配器。
3. **MCP 工具服务** —— 把分析函数暴露为 MCP 工具，供大模型客户端调用。
4. **仿真故障场景** —— 以安全、离线的方式演示异常检测。

### 这里说的「工程师数字人」是什么

最初的想法是做一个「有工程师经验的数字人」实时辅助工厂操作员。本仓库只实现了这个愿景里**最小、最诚实的一块**：几条硬编码的启发式规则。真正的实现需要更多（知识图谱、基于验证笔记的检索增强、经过校验的工艺模型）——这些**都不包含在这里**。

### 架构（实际实现，非愿景）

```
┌───────────────────────────────────────────┐
│            MCP 工具服务                    │
│  （把分析器暴露给大模型，只读）            │
└──────────────────┬────────────────────────┘
                   │
┌──────────────────▼────────────────────────┐
│           分析引擎                         │
│  压力 / 液位 / 趋势 / 因果                 │
│  （启发式规则，仅用于教学）                │
└──────────────────┬────────────────────────┘
                   │
┌──────────────────▼────────────────────────┐
│           数据适配器                       │
│  SimulationAdapter（默认）                 │
│  OPCUAAdapter（可选，异步，只读）          │
└───────────────────────────────────────────┘
```

### 快速开始

```bash
git clone https://github.com/WorkingWolfOnline/industrial-ai-assistant.git
cd industrial-ai-assistant

# 核心框架基于 Python 标准库，无需第三方依赖即可运行
python examples/chemical_process/demo.py --report
```

### 文档

- [架构设计](docs/architecture.md)
- [可行性分析](docs/feasibility-study.md)
- [安全指南](docs/security.md)
- [部署前安全清单](docs/safety-checklist.md)
- [MCP 集成](docs/mcp-integration.md)
- [扩展规则](docs/expert-knowledge.md)

### 许可证

MIT License，详见 [LICENSE](LICENSE)。
