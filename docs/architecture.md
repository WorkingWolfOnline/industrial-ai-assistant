# System Architecture

## Overview

This document describes the architecture of the Industrial AI Assistant Framework, designed for integrating LLM-based AI systems with industrial control systems in a safe, read-only manner.

## Design Principles

### 1. Safety First
- **Read-Only Default**: AI systems never write to DCS directly
- **Human-in-the-Loop**: All control recommendations require operator confirmation
- **Fail-Safe**: AI failures must not affect DCS operation
- **Defense in Depth**: Multiple layers of security controls

### 2. Domain Expertise Embedding
- **Knowledge Representation**: Structured storage of expert thinking patterns
- **Reasoning Engine**: Implementation of domain-specific analysis logic
- **Continuous Learning**: Feedback loop for knowledge refinement

### 3. Open Standards
- **MCP Protocol**: Model Context Protocol for AI-tool integration
- **OPC UA**: Industry standard for industrial communication
- **Modular Design**: Pluggable components for different environments

## System Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION LAYER                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │  Control Room    │  │  Field Assistant │  │  Web Dashboard   │          │
│  │  Interface       │  │  (Mobile)        │  │                  │          │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘          │
└───────────┼─────────────────────┼─────────────────────┼────────────────────┘
            │                     │                     │
            └─────────────────────┼─────────────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI ASSISTANT LAYER                                   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     LLM Core (Claude/GPT/etc)                        │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │   Natural    │  │   Context    │  │   Response   │              │   │
│  │  │   Language   │  │   Awareness  │  │   Generation │              │   │
│  │  │   Understanding│ │              │  │              │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  └────────────────────────────────────┬────────────────────────────────┘   │
│                                       │                                      │
│  ┌────────────────────────────────────┼────────────────────────────────┐   │
│  │                         MCP SERVER                                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │   Tool       │  │   Resource   │  │   Prompt     │              │   │
│  │  │   Registry   │  │   Registry   │  │   Registry   │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  └────────────────────────────────────┬────────────────────────────────┘   │
└───────────────────────────────────────┼────────────────────────────────────┘
                                        │
┌───────────────────────────────────────┼────────────────────────────────────┐
│                         INTEGRATION LAYER                                    │
│                                       │                                      │
│  ┌────────────────────────────────────┼────────────────────────────────┐   │
│  │                      COMPOSIO AGENT                                 │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │   Action     │  │   Trigger    │  │   Workflow   │              │   │
│  │  │   Executor   │  │   Handler    │  │   Engine     │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  └────────────────────────────────────┬────────────────────────────────┘   │
│                                       │                                      │
│  ┌────────────────────────────────────┼────────────────────────────────┐   │
│  │                    PROTOCOL ADAPTERS                                │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │   OPC UA     │  │   Modbus     │  │   Custom     │              │   │
│  │  │   Adapter    │  │   Adapter    │  │   API        │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  └────────────────────────────────────┬────────────────────────────────┘   │
└───────────────────────────────────────┼────────────────────────────────────┘
                                        │
┌───────────────────────────────────────┼────────────────────────────────────┐
│                    DATA ACCESS LAYER (READ-ONLY)                             │
│                                       │                                      │
│  ┌────────────────────────────────────┼────────────────────────────────┐   │
│  │                      DATA DIODE / GATEWAY                           │   │
│  │                    (Unidirectional Data Flow)                       │   │
│  │                         READ-ONLY ACCESS                            │   │
│  └────────────────────────────────────┬────────────────────────────────┘   │
└───────────────────────────────────────┼────────────────────────────────────┘
                                        │
┌───────────────────────────────────────┼────────────────────────────────────┐
│                    INDUSTRIAL CONTROL SYSTEM                                 │
│                                       │                                      │
│  ┌────────────────────────────────────┼────────────────────────────────┐   │
│  │                         DCS/SCADA                                   │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │   Process    │  │   Historical │  │   Alarm      │              │   │
│  │  │   Database   │  │   Database   │  │   Server     │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  └────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. MCP Server

The Model Context Protocol (MCP) server exposes industrial data and analysis capabilities to the LLM.

#### Tools

```python
# Example tool definition
@mcp.tool()
def analyze_pressure_system(
    upstream_pressure: float,
    downstream_pressure: float,
    design_pressure_diff: float = 0.2
) -> dict:
    """
    Analyze pressure balance in a fluid system.

    Args:
        upstream_pressure: Pressure at system inlet (MPa)
        downstream_pressure: Pressure at system outlet (MPa)
        design_pressure_diff: Expected pressure differential (MPa)

    Returns:
        Analysis result with status and recommendations
    """
    pressure_diff = upstream_pressure - downstream_pressure

    if pressure_diff < 0:
        return {
            "status": "critical",
            "issue": "Negative pressure differential",
            "recommendation": "Check pump operation and upstream blockages"
        }

    if abs(pressure_diff - design_pressure_diff) > 0.1:
        return {
            "status": "warning",
            "issue": "Pressure differential deviation",
            "actual_diff": pressure_diff,
            "expected_diff": design_pressure_diff
        }

    return {"status": "normal", "pressure_diff": pressure_diff}
```

#### Resources

```python
@mcp.resource("knowledge_base://equipment/{equipment_id}")
def get_equipment_knowledge(equipment_id: str) -> str:
    """Retrieve equipment documentation and expert knowledge."""
    return knowledge_base.get_equipment_info(equipment_id)
```

### 2. Knowledge Base

Structured storage of domain expertise:

```yaml
# knowledge_base/structure.yaml
expert_patterns:
  pressure_analysis:
    description: "Analyze pressure relationships in fluid systems"
    rules:
      - "Low pressure cannot feed high pressure systems"
      - "Pressure differential indicates flow resistance"
      - "Sudden pressure drops indicate blockages"

  causal_chain:
    description: "Derive root causes from symptoms"
    methodology:
      - "Identify observable symptoms"
      - "Trace upstream dependencies"
      - "Identify common cause factors"
      - "Verify with multiple data points"

equipment_templates:
  reactor:
    common_parameters:
      - temperature
      - pressure
      - level
    common_issues:
      - name: "temperature_runaway"
        symptoms: ["temp_rising", "pressure_rising"]
        causes: ["cooling_failure", "feed_increase", "reaction_acceleration"]
```

### 3. Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY ZONES                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐ │
│  │   Zone 3    │      │   Zone 2    │      │   Zone 1    │ │
│  │  (Corporate)│ ←──→ │   (DMZ)     │ ←──→ │  (Control)  │ │
│  │             │      │             │      │             │ │
│  │  AI Layer   │      │ Data Gateway│      │   DCS       │ │
│  │  Web Apps   │      │  Historian  │      │   PLC       │ │
│  └─────────────┘      └─────────────┘      └─────────────┘ │
│        ↑                                          ↑         │
│        │         ┌─────────────────┐             │         │
│        └────────→│   DATA DIODE    │←────────────┘         │
│                  │ (Unidirectional)│                       │
│                  └─────────────────┘                       │
│                                                             │
│  Security Controls:                                         │
│  • Firewall between each zone                               │
│  • Data diode ensures unidirectional flow                   │
│  • No direct network path from Zone 3 to Zone 1             │
│  • All connections use encrypted protocols                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Real-Time Monitoring Flow

```
DCS → OPC UA Server → Data Gateway → Composio → MCP Server → LLM → UI
  │          │              │              │            │       │
  │          │              │              │            │       └─→ Display
  │          │              │              │            └─→ Analysis
  │          │              │              └─→ Data Normalization
  │          │              └─→ Security Filter
  │          └─→ Protocol Translation
  └─→ Raw Process Data
```

### 2. Analysis Request Flow

```
User Query → LLM → MCP Tool Call → Composio Action → DCS Read → Response
    │          │         │              │              │          │
    │          │         │              │              │          └─→ Natural Language
    │          │         │              │              └─→ Raw Data
    │          │         │              └─→ Protocol Adapter
    │          │         └─→ Tool Selection
    │          └─→ Intent Understanding
    └─→ Natural Language Input
```

## Deployment Patterns

### Pattern 1: On-Premise Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                    FACTORY NETWORK                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              INDUSTRIAL DMZ                          │   │
│  │  ┌──────────────┐  ┌──────────────┐                │   │
│  │  │  AI Server   │  │  Data Gateway│                │   │
│  │  │  (Docker)    │  │  (Read-Only) │                │   │
│  │  └──────────────┘  └──────────────┘                │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│  ┌──────────────────────┼──────────────────────────────┐   │
│  │              CONTROL NETWORK (Isolated)              │   │
│  │  ┌──────────────┐  ┌──────────────┐                │   │
│  │  │     DCS      │  │     PLC      │                │   │
│  │  └──────────────┘  └──────────────┘                │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Pattern 2: Cloud-Edge Hybrid

```
┌─────────────────────────────────────────────────────────────┐
│                      CLOUD (AWS/Azure/GCP)                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ┌──────────────┐  ┌──────────────┐                │   │
│  │  │   LLM API    │  │  Web Dashboard│                │   │
│  │  │  (Claude/etc)│  │  (React/Vue) │                │   │
│  │  └──────────────┘  └──────────────┘                │   │
│  └─────────────────────────────────────────────────────┘   │
│                         ↑ VPN/Private Link                  │
└─────────────────────────┼───────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────┐
│                    FACTORY EDGE                              │
│  ┌──────────────────────┼──────────────────────────────┐   │
│  │              ┌───────┴───────┐                      │   │
│  │              │  Edge Gateway │                      │   │
│  │              │  (MCP Server) │                      │   │
│  │              └───────┬───────┘                      │   │
│  │                      │                               │   │
│  │  ┌───────────────────┼──────────────────────────┐   │   │
│  │  │              CONTROL NETWORK                  │   │   │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │   │
│  │  │  │   DCS    │  │   PLC    │  │  Sensors │   │   │   │
│  │  │  └──────────┘  └──────────┘  └──────────┘   │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Performance Considerations

| Metric | Target | Implementation |
|:---|:---:|:---|
| Data Latency | < 5 seconds | Edge caching + WebSocket |
| Query Response | < 3 seconds | LLM streaming + caching |
| System Availability | 99.9% | Redundant gateways |
| Data Throughput | 1000 tags/second | Optimized OPC UA batching |

## Scalability

### Horizontal Scaling

```
┌─────────────────────────────────────────────────────────────┐
│                    LOAD BALANCER                             │
│                         │                                    │
│         ┌───────────────┼───────────────┐                   │
│         ▼               ▼               ▼                   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │  MCP Server  │ │  MCP Server  │ │  MCP Server  │        │
│  │     #1       │ │     #2       │ │     #N       │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│         │               │               │                   │
│         └───────────────┼───────────────┘                   │
│                         ▼                                   │
│              ┌─────────────────────┐                        │
│              │   Shared Cache      │                        │
│              │   (Redis)           │                        │
│              └─────────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## Next Steps

1. Review [Security Guidelines](security.md)
2. Explore [MCP Integration](mcp-integration.md)
3. Learn about [Expert Knowledge Embedding](expert-knowledge.md)
