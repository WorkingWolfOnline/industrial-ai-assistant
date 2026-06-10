# Industrial AI Assistant Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Protocol-green.svg)](https://modelcontextprotocol.io/)

> An open-source framework for integrating LLM-based AI assistants with Industrial Control Systems (ICS/DCS) via MCP protocol and Composio, featuring domain expert knowledge embedding.

[English](#english) | [中文](#中文)

---

## <a name="english"></a>English

### Overview

This project provides a **reference architecture** and **implementation framework** for building AI-powered assistant systems that can:

- Monitor real-time industrial process data from DCS/SCADA systems
- Apply domain expert knowledge for intelligent anomaly detection
- Generate actionable recommendations for control room operators
- Provide field operation guidance through mobile interfaces

**Key Innovation**: The framework demonstrates how to embed domain expert thinking patterns (like pressure balance analysis, causal chain reasoning) into LLM-based AI systems for industrial applications.

### ⚠️ Important Disclaimer

This is a **reference implementation** and **research framework** only:
- ✅ Suitable for: Learning, research, proof-of-concept development
- ✅ Contains: Generic architecture patterns, integration methodologies
- ❌ Does NOT contain: Production-ready code, specific device configurations, proprietary industrial data
- ⚠️ **WARNING**: Direct connection to production DCS systems requires thorough security assessment and should only be done by qualified industrial automation professionals

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Assistant Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Domain Expert │  │  Knowledge   │  │  Decision    │          │
│  │   Persona    │  │   Retrieval  │  │   Engine     │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         └─────────────────┼─────────────────┘                   │
│                           ▼                                     │
│                ┌─────────────────────┐                         │
│                │     MCP Server      │                         │
│                │  (Model Context     │                         │
│                │   Protocol)         │                         │
│                └──────────┬──────────┘                         │
└───────────────────────────┼─────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────────┐
│                    Integration Layer (Composio)                  │
│                           ▼                                      │
│                ┌─────────────────────┐                          │
│                │   Protocol Adapters │                          │
│                │  (OPC UA/Modbus/API)│                          │
│                └──────────┬──────────┘                          │
└───────────────────────────┼─────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────────┐
│              Industrial Control System (Read-Only)               │
│                           ▼                                      │
│              ┌─────────────────────────┐                        │
│              │  DCS/SCADA/PLC Systems  │                        │
│              │    (Via OPC UA/etc)     │                        │
│              └─────────────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

### Core Concepts

#### 1. Domain Expert Knowledge Embedding

The framework demonstrates how to structure and embed industrial domain knowledge:

```python
# Example: Expert reasoning pattern
class ExpertAnalyzer:
    """
    Implements expert thinking patterns for industrial process analysis:
    - Pressure balance analysis
    - Causal chain derivation
    - Design intent understanding
    """

    def analyze_pressure_system(self, upstream_pressure, downstream_pressure):
        """
        Expert heuristic: All fluid systems are pressure balance problems
        """
        pressure_diff = upstream_pressure - downstream_pressure

        if pressure_diff < 0:
            return {
                "issue": "Pressure mismatch",
                "reason": "Low pressure cannot feed high pressure system",
                "recommendation": "Check pump status or upstream blockages"
            }

        return {"status": "normal", "pressure_diff": pressure_diff}
```

#### 2. Safety-First Architecture

```
Security Zones:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Level 3   │ ←→  │   Level 2   │ ←→  │   Level 1   │
│  (AI Layer) │     │ (Data Layer)│     │ (DCS Layer) │
│             │     │             │     │  READ-ONLY  │
└─────────────┘     └─────────────┘     └─────────────┘
       ↑                                    ↑
   Unidirectional                      Control Network
   Data Diode                         (Isolated)
```

**Key Safety Principles:**
- ✅ Read-only by default - AI never writes to DCS directly
- ✅ Human-in-the-loop - All recommendations require operator confirmation
- ✅ Fail-safe design - AI failure does not affect DCS operation
- ✅ Physical isolation - Network segmentation with data diodes

### Project Structure

```
industrial-ai-assistant/
├── docs/
│   ├── architecture.md           # System architecture documentation
│   ├── security.md               # Security guidelines
│   ├── mcp-integration.md        # MCP protocol integration guide
│   └── expert-knowledge.md       # How to embed domain expertise
├── src/
│   ├── mcp_server/               # MCP server implementation
│   │   ├── server.py
│   │   └── tools/
│   ├── knowledge_base/           # Knowledge base structures
│   │   ├── equipment.py
│   │   ├── process.py
│   │   └── expert_patterns.py
│   ├── analyzers/                # Analysis engines
│   │   ├── pressure_analyzer.py
│   │   ├── trend_analyzer.py
│   │   └── causal_analyzer.py
│   └── interfaces/               # User interfaces
│       ├── control_room.py
│       └── field_assistant.py
├── examples/
│   ├── chemical_process/         # Chemical industry example
│   ├── power_plant/              # Power generation example
│   └── oil_gas/                  # Oil & gas example
├── tests/
└── README.md
```

### Quick Start

#### Prerequisites

```bash
Python 3.9+
Node.js 18+ (for MCP components)
```

#### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/industrial-ai-assistant.git
cd industrial-ai-assistant

# Install dependencies
pip install -r requirements.txt

# Install MCP SDK
npm install @modelcontextprotocol/sdk
```

#### Basic Usage

```python
from industrial_ai import MCPClient, ExpertAnalyzer

# Initialize MCP client
client = MCPClient(
    server_url="opc.tcp://your-dcs-server:4840",
    read_only=True  # Safety: enforce read-only mode
)

# Connect to knowledge base
knowledge_base = ExpertAnalyzer.load_knowledge_base("examples/chemical_process")

# Analyze real-time data
while True:
    data = client.read_process_data(tags=["TEMP_001", "PRESS_001", "FLOW_001"])

    # Apply expert analysis
    result = knowledge_base.analyze(data)

    if result.has_anomaly:
        print(f"⚠️ Anomaly detected: {result.description}")
        print(f"💡 Recommendation: {result.recommendation}")

    time.sleep(5)
```

### Integration Examples

#### OPC UA Integration

```python
from industrial_ai.adapters import OPCUAAdapter

adapter = OPCUAAdapter(
    endpoint="opc.tcp://dcs-server:4840",
    security_policy="Basic256Sha256"
)

# Read process variables
values = adapter.read_values([
    "ns=2;s=Reactor.Temperature",
    "ns=2;s=Reactor.Pressure"
])
```

#### MCP Server Configuration

```json
{
  "mcpServers": {
    "industrial-dcs": {
      "command": "python",
      "args": ["-m", "industrial_ai.mcp_server"],
      "env": {
        "DCS_ENDPOINT": "opc.tcp://localhost:4840",
        "READ_ONLY_MODE": "true"
      }
    }
  }
}
```

### Knowledge Base Template

Create your own domain knowledge base:

```yaml
# knowledge_base/equipment_template.yaml
equipment:
  - id: REACTOR_001
    name: Gasification Reactor
    type: reactor
    parameters:
      - name: temperature
        tag: TI_001
        normal_range: [1400, 1700]
        unit: celsius
        alarms:
          high: 1750
          high_high: 1800

      - name: pressure
        tag: PI_001
        normal_range: [4.5, 5.5]
        unit: mpa

    expert_rules:
      - name: pressure_balance_check
        description: "Verify pressure differential across reactor"
        condition: "inlet_pressure - outlet_pressure < 0.1"
        action: "alert_operator"

      - name: temperature_trend
        description: "Monitor temperature change rate"
        condition: "temperature_slope > 50"
        action: "predictive_alert"
```

---

## <a name="中文"></a>中文

### 项目概述

本项目提供了一个**参考架构**和**实现框架**，用于构建能够执行以下功能的AI辅助工业控制系统：

- 从DCS/SCADA系统监控实时工业过程数据
- 应用领域专家知识进行智能异常检测
- 为控制室操作员生成可执行的建议
- 通过移动界面提供现场操作指导

**核心创新**：该框架展示了如何将领域专家思维模式（如压力平衡分析、因果链推导）嵌入到基于LLM的工业AI系统中。

### ⚠️ 重要声明

这只是一个**参考实现**和**研究框架**：
- ✅ 适用于：学习、研究、概念验证开发
- ✅ 包含：通用架构模式、集成方法论
- ❌ 不包含：生产就绪代码、特定设备配置、专有工业数据
- ⚠️ **警告**：直接连接生产DCS系统需要全面的安全评估，且只能由合格的工业自动化专业人员执行

### 核心概念

#### 1. 领域专家知识嵌入

框架展示了如何结构化和嵌入工业领域知识：

```python
# 示例：专家推理模式
class ExpertAnalyzer:
    """
    实现工业过程分析的专家思维模式：
    - 压力平衡分析
    - 因果链推导
    - 设计意图理解
    """

    def analyze_pressure_system(self, upstream_pressure, downstream_pressure):
        """
        专家启发式：所有流体系统都是压力平衡问题
        """
        pressure_diff = upstream_pressure - downstream_pressure

        if pressure_diff < 0:
            return {
                "issue": "压力不匹配",
                "reason": "低压无法向高压系统输送",
                "recommendation": "检查泵状态或上游堵塞"
            }

        return {"status": "正常", "pressure_diff": pressure_diff}
```

#### 2. 安全第一架构

**关键安全原则：**
- ✅ 默认只读 - AI绝不直接向DCS写入
- ✅ 人机协同 - 所有建议需要操作员确认
- ✅ 故障安全设计 - AI故障不影响DCS运行
- ✅ 物理隔离 - 通过网络分段和数据隔离实现

### 快速开始

```bash
# 克隆仓库
git clone https://github.com/yourusername/industrial-ai-assistant.git
cd industrial-ai-assistant

# 安装依赖
pip install -r requirements.txt

# 运行示例
python examples/chemical_process/demo.py
```

### 文档

- [架构设计](docs/architecture.md)
- [安全指南](docs/security.md)
- [MCP集成](docs/mcp-integration.md)
- [专家知识嵌入](docs/expert-knowledge.md)

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) - Anthropic's open protocol
- [Composio](https://composio.dev/) - Integration framework
- Industrial automation community for domain knowledge patterns

## Contact

- Issues: [GitHub Issues](https://github.com/yourusername/industrial-ai-assistant/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/industrial-ai-assistant/discussions)

---

**Disclaimer**: This is an open-source research project. Use in production environments at your own risk and only after thorough security assessment.
