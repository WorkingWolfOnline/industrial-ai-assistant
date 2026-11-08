#!/usr/bin/env python3
"""
Industrial AI Assistant - Chemical Process Demo

演示 Industrial AI Assistant Framework 的核心用法：
1. 通过 MCPClient 读取过程数据（默认仿真适配器，无真实设备可运行）
2. 通过 ExpertAnalyzer 应用领域专家知识进行分析
3. 输出结构化分析结果

⚠️ WARNING: 这是仿真/演示。连接生产系统前必须完成安全评估，
且只能由合格的工业自动化专业人员操作。
"""

import asyncio
import json
import sys

# 允许直接从源码目录运行（未 pip install 时也能导入包）
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from industrial_ai import ExpertAnalyzer, MCPClient  # noqa: E402
from industrial_ai.models import AnalysisResult  # noqa: E402


def _print_analysis(result: AnalysisResult) -> None:
    """格式化打印分析结果。"""
    status_icon = {
        "normal": "✅",
        "warning": "⚠️ ",
        "critical": "🚨",
    }.get(result.status.value, "❓")

    print(f"\n{status_icon} {result.parameter.upper()}")
    print(f"   Status: {result.status.value.upper()}")
    print(f"   Value: {result.value:.2f}")

    if result.issue:
        print(f"   Issue: {result.issue}")
    if result.recommendation:
        print(f"   Recommendation: {result.recommendation}")
    if result.causal_chain:
        print("   Causal Chain:")
        for i, step in enumerate(result.causal_chain, 1):
            print(f"      {i}. {step}")


async def monitor_loop(interval: int = 5) -> None:
    """持续监控循环（仿真数据）。"""
    client = MCPClient()  # 默认仿真适配器，read_only=True
    analyzer = ExpertAnalyzer()

    print("=" * 60)
    print("Industrial AI Assistant - Demo Mode")
    print("=" * 60)
    print("\n⚠️  SIMULATION MODE - No actual DCS connection\n")

    while True:
        try:
            data = client.read_process_data(
                [
                    "REACTOR_PRESSURE_IN",
                    "REACTOR_PRESSURE_OUT",
                    "VESSEL_LEVEL",
                    "INLET_FLOW",
                    "OUTLET_FLOW",
                ]
            )

            # 压力平衡分析
            if "REACTOR_PRESSURE_IN" in data and "REACTOR_PRESSURE_OUT" in data:
                _print_analysis(
                    analyzer.analyze_pressure(
                        data["REACTOR_PRESSURE_IN"].value,
                        data["REACTOR_PRESSURE_OUT"].value,
                    )
                )

            # 液位平衡分析
            if {"VESSEL_LEVEL", "INLET_FLOW", "OUTLET_FLOW"} <= data.keys():
                _print_analysis(
                    analyzer.analyze_level(
                        data["VESSEL_LEVEL"].value,
                        data["INLET_FLOW"].value,
                        data["OUTLET_FLOW"].value,
                    )
                )

            await asyncio.sleep(interval)

        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user.")
            break
        except Exception as e:  # pragma: no cover
            print(f"\nError: {e}")
            await asyncio.sleep(interval)


def generate_report() -> list:
    """生成一份覆盖多场景的样例分析报告。"""
    analyzer = ExpertAnalyzer()
    scenarios = [
        {"name": "Normal Operation", "up": 5.2, "down": 5.0, "level": 52.0, "in": 100.0, "out": 100.0},
        {"name": "Pressure Deviation", "up": 5.2, "down": 4.5, "level": 55.0, "in": 100.0, "out": 100.0},
        {"name": "Level Imbalance", "up": 5.2, "down": 5.0, "level": 65.0, "in": 120.0, "out": 95.0},
    ]
    report = []
    for s in scenarios:
        p = analyzer.analyze_pressure(s["up"], s["down"])
        l = analyzer.analyze_level(s["level"], s["in"], s["out"])
        report.append(
            {
                "scenario": s["name"],
                "pressure_analysis": p.to_dict(),
                "level_analysis": l.to_dict(),
            }
        )
    return report


async def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        print(json.dumps(generate_report(), indent=2, ensure_ascii=False))
    else:
        await monitor_loop()


if __name__ == "__main__":
    print(__doc__)
    print("\nUsage:")
    print("  python demo.py           # Run interactive monitoring")
    print("  python demo.py --report  # Generate analysis report\n")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")
