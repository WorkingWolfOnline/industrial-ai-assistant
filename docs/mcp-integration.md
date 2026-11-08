# MCP 集成指南

本文档说明如何将工业分析能力通过 **MCP（Model Context Protocol）** 暴露给 LLM 客户端（Claude Desktop / Cursor / Codex 等）。

## 什么是 MCP

MCP 相当于给 AI Agent 用的「USB 接口标准」：桥接器把应用的真实能力封装成标准工具，供 LLM 发现并调用。本框架把工业分析函数封装为 MCP 工具，让 AI 能对过程数据进行压力平衡、液位平衡等分析。

## 安装

```bash
pip install mcp
# 或安装本包的可选依赖
pip install -e ".[mcp]"
```

## 启动 MCP Server

```python
from industrial_ai import build_mcp_server

mcp = build_mcp_server()
mcp.run()  # 默认 stdio 传输，供本地 MCP 客户端连接
```

也可通过命令行方式（若已配置 entry point）启动。

## 配置客户端

以 Claude Desktop 为例，在配置文件中加入：

```json
{
  "mcpServers": {
    "industrial-ai": {
      "command": "python",
      "args": ["-c", "from industrial_ai import build_mcp_server; build_mcp_server().run()"],
      "env": {
        "PYTHONPATH": "/path/to/industrial-ai-assistant/src"
      }
    }
  }
}
```

## 暴露的工具

| 工具 | 说明 | 只读 |
| --- | --- | --- |
| `analyze_pressure_system` | 分析流体系统压力平衡 | ✅ |
| `analyze_level_system` | 分析容器液位质量平衡 | ✅ |

## 安全原则

- **默认只读**：本框架不提供任何写操作工具，AI 无法直接控制 DCS/PLC。
- **人在回路**：所有分析结果仅供建议，需操作员确认后才可执行。
- **审计**：接入生产系统前，务必开启完整操作日志与审计。
