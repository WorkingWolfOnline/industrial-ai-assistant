#!/usr/bin/env python3
"""
Industrial AI Assistant - Chemical Process Demo

This is a demonstration of the Industrial AI Assistant Framework
for educational and research purposes.

⚠️ WARNING: This is a simulation/demo only. Do not connect to
production systems without proper security assessment.
"""

import asyncio
import json
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime


class AlertLevel(Enum):
    """Alert severity levels."""
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class ProcessParameter:
    """Represents a process parameter reading."""
    name: str
    value: float
    unit: str
    timestamp: datetime
    normal_range: tuple
    alarm_high: Optional[float] = None
    alarm_low: Optional[float] = None

    @property
    def status(self) -> AlertLevel:
        """Determine parameter status based on value."""
        if self.alarm_high and self.value > self.alarm_high:
            return AlertLevel.CRITICAL
        if self.alarm_low and self.value < self.alarm_low:
            return AlertLevel.CRITICAL
        min_norm, max_norm = self.normal_range
        if not (min_norm <= self.value <= max_norm):
            return AlertLevel.WARNING
        return AlertLevel.NORMAL


@dataclass
class AnalysisResult:
    """Result of process analysis."""
    timestamp: datetime
    parameter: str
    status: AlertLevel
    value: float
    issue: Optional[str] = None
    recommendation: Optional[str] = None
    causal_chain: Optional[List[str]] = None


class ExpertAnalyzer:
    """
    Implements domain expert thinking patterns for industrial analysis.

    This class demonstrates how to embed expert knowledge:
    - Pressure balance analysis
    - Causal chain derivation
    - Design intent understanding
    """

    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()

    def _load_knowledge_base(self) -> Dict:
        """Load generic expert knowledge patterns."""
        return {
            "pressure_analysis": {
                "description": "All fluid systems are pressure balance problems",
                "rules": [
                    "Low pressure cannot feed high pressure systems",
                    "Pressure differential indicates flow resistance",
                    "Sudden pressure drops indicate blockages"
                ]
            },
            "causal_chain": {
                "description": "Derive root causes from symptoms",
                "methodology": [
                    "Identify observable symptoms",
                    "Trace upstream dependencies",
                    "Identify common cause factors",
                    "Verify with multiple data points"
                ]
            }
        }

    def analyze_pressure_system(
        self,
        upstream_pressure: float,
        downstream_pressure: float,
        design_diff: float = 0.2
    ) -> AnalysisResult:
        """
        Analyze pressure balance using expert heuristics.

        Args:
            upstream_pressure: Pressure at system inlet (MPa)
            downstream_pressure: Pressure at system outlet (MPa)
            design_diff: Expected pressure differential (MPa)

        Returns:
            AnalysisResult with status and recommendations
        """
        pressure_diff = upstream_pressure - downstream_pressure

        # Rule 1: Check for negative differential
        if pressure_diff < 0:
            return AnalysisResult(
                timestamp=datetime.now(),
                parameter="pressure_differential",
                status=AlertLevel.CRITICAL,
                value=pressure_diff,
                issue="Negative pressure differential detected",
                recommendation=(
                    "Check pump operation and upstream blockages. "
                    "Verify pressure transmitter calibration."
                ),
                causal_chain=[
                    "Negative pressure differential observed",
                    "Possible causes: Pump failure, upstream blockage, or transmitter error",
                    "Immediate action: Verify pump status and inlet conditions"
                ]
            )

        # Rule 2: Check for deviation from design
        deviation = abs(pressure_diff - design_diff)
        if deviation > 0.1:
            return AnalysisResult(
                timestamp=datetime.now(),
                parameter="pressure_differential",
                status=AlertLevel.WARNING,
                value=pressure_diff,
                issue=f"Pressure differential deviation: {deviation:.2f} MPa",
                recommendation=(
                    f"Expected {design_diff} MPa, actual {pressure_diff:.2f} MPa. "
                    "Check for fouling, valve position, or flow changes."
                ),
                causal_chain=[
                    f"Pressure differential {pressure_diff:.2f} MPa vs design {design_diff} MPa",
                    "Possible causes: Fouling, partial blockage, or valve malfunction",
                    "Recommended: Inspect filters and valve positions"
                ]
            )

        return AnalysisResult(
            timestamp=datetime.now(),
            parameter="pressure_differential",
            status=AlertLevel.NORMAL,
            value=pressure_diff,
            recommendation="Pressure system operating normally"
        )

    def analyze_level_system(
        self,
        level: float,
        inflow: float,
        outflow: float,
        level_setpoint: float = 50.0
    ) -> AnalysisResult:
        """
        Analyze vessel level using mass balance principles.

        Args:
            level: Current level percentage
            inflow: Inlet flow rate
            outflow: Outlet flow rate
            level_setpoint: Target level

        Returns:
            AnalysisResult with status and recommendations
        """
        flow_balance = inflow - outflow
        level_deviation = abs(level - level_setpoint)

        # Check for level deviation with flow imbalance
        if level_deviation > 10 and abs(flow_balance) > 5:
            if flow_balance > 0:
                issue = "Level rising: Inflow exceeds outflow"
                recommendation = "Increase outflow or reduce inflow to maintain level"
            else:
                issue = "Level falling: Outflow exceeds inflow"
                recommendation = "Reduce outflow or increase inflow to maintain level"

            return AnalysisResult(
                timestamp=datetime.now(),
                parameter="vessel_level",
                status=AlertLevel.WARNING,
                value=level,
                issue=issue,
                recommendation=recommendation,
                causal_chain=[
                    f"Level at {level:.1f}% (setpoint {level_setpoint}%)",
                    f"Flow imbalance: In {inflow}, Out {outflow}",
                    "Control action required to restore balance"
                ]
            )

        return AnalysisResult(
            timestamp=datetime.now(),
            parameter="vessel_level",
            status=AlertLevel.NORMAL,
            value=level,
            recommendation="Level system operating normally"
        )


class DCSClient:
    """
    Simulated DCS client for demonstration purposes.

    In production, this would connect to actual OPC UA or other
    industrial protocols with proper security controls.
    """

    def __init__(self, read_only: bool = True):
        self.read_only = read_only
        self._simulated_data = {
            "REACTOR_PRESSURE_IN": 5.2,
            "REACTOR_PRESSURE_OUT": 5.0,
            "VESSEL_LEVEL": 55.0,
            "INLET_FLOW": 100.0,
            "OUTLET_FLOW": 95.0,
            "TEMPERATURE": 250.0
        }

    def read_parameter(self, tag_name: str) -> Optional[ProcessParameter]:
        """
        Read a process parameter from DCS.

        Args:
            tag_name: Name of the parameter tag

        Returns:
            ProcessParameter object or None if not found
        """
        if tag_name not in self._simulated_data:
            return None

        value = self._simulated_data[tag_name]

        # Define generic ranges for demo
        ranges = {
            "REACTOR_PRESSURE_IN": ((4.5, 5.5), 5.8, 4.2),
            "REACTOR_PRESSURE_OUT": ((4.3, 5.3), 5.6, 4.0),
            "VESSEL_LEVEL": ((30.0, 70.0), 80.0, 20.0),
            "INLET_FLOW": ((80.0, 120.0), 130.0, 70.0),
            "OUTLET_FLOW": ((80.0, 120.0), 130.0, 70.0),
            "TEMPERATURE": ((200.0, 300.0), 320.0, 180.0)
        }

        range_info = ranges.get(tag_name, ((0, 100), None, None))

        return ProcessParameter(
            name=tag_name,
            value=value,
            unit="GENERIC",
            timestamp=datetime.now(),
            normal_range=range_info[0],
            alarm_high=range_info[1],
            alarm_low=range_info[2]
        )

    def read_multiple(self, tag_names: List[str]) -> Dict[str, ProcessParameter]:
        """Read multiple parameters."""
        results = {}
        for tag in tag_names:
            param = self.read_parameter(tag)
            if param:
                results[tag] = param
        return results


class AIAssistant:
    """
    Main AI Assistant class that orchestrates data collection,
    analysis, and recommendation generation.
    """

    def __init__(self):
        self.dcs = DCSClient(read_only=True)
        self.analyzer = ExpertAnalyzer()

    async def monitor_loop(self, interval: int = 5):
        """
        Main monitoring loop.

        Args:
            interval: Seconds between readings
        """
        print("=" * 60)
        print("Industrial AI Assistant - Demo Mode")
        print("=" * 60)
        print("\n⚠️  SIMULATION MODE - No actual DCS connection\n")

        while True:
            try:
                # Read process data
                data = self.dcs.read_multiple([
                    "REACTOR_PRESSURE_IN",
                    "REACTOR_PRESSURE_OUT",
                    "VESSEL_LEVEL",
                    "INLET_FLOW",
                    "OUTLET_FLOW"
                ])

                # Perform analysis
                await self._analyze_and_report(data)

                # Wait for next cycle
                await asyncio.sleep(interval)

            except KeyboardInterrupt:
                print("\n\nMonitoring stopped by user.")
                break
            except Exception as e:
                print(f"\nError: {e}")
                await asyncio.sleep(interval)

    async def _analyze_and_report(self, data: Dict[str, ProcessParameter]):
        """Analyze data and generate report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\n[{timestamp}] Process Scan")
        print("-" * 60)

        # Pressure analysis
        if "REACTOR_PRESSURE_IN" in data and "REACTOR_PRESSURE_OUT" in data:
            result = self.analyzer.analyze_pressure_system(
                upstream_pressure=data["REACTOR_PRESSURE_IN"].value,
                downstream_pressure=data["REACTOR_PRESSURE_OUT"].value
            )
            self._print_analysis(result)

        # Level analysis
        if "VESSEL_LEVEL" in data and "INLET_FLOW" in data and "OUTLET_FLOW" in data:
            result = self.analyzer.analyze_level_system(
                level=data["VESSEL_LEVEL"].value,
                inflow=data["INLET_FLOW"].value,
                outflow=data["OUTLET_FLOW"].value
            )
            self._print_analysis(result)

    def _print_analysis(self, result: AnalysisResult):
        """Print analysis result in formatted way."""
        status_icon = {
            AlertLevel.NORMAL: "✅",
            AlertLevel.WARNING: "⚠️ ",
            AlertLevel.CRITICAL: "🚨"
        }.get(result.status, "❓")

        print(f"\n{status_icon} {result.parameter.upper()}")
        print(f"   Status: {result.status.value.upper()}")
        print(f"   Value: {result.value:.2f}")

        if result.issue:
            print(f"   Issue: {result.issue}")

        if result.recommendation:
            print(f"   Recommendation: {result.recommendation}")

        if result.causal_chain:
            print(f"   Causal Chain:")
            for i, step in enumerate(result.causal_chain, 1):
                print(f"      {i}. {step}")


def generate_report():
    """Generate a sample analysis report."""
    analyzer = ExpertAnalyzer()

    # Simulate different scenarios
    scenarios = [
        {
            "name": "Normal Operation",
            "upstream": 5.2,
            "downstream": 5.0,
            "level": 52.0,
            "inflow": 100.0,
            "outflow": 100.0
        },
        {
            "name": "Pressure Deviation",
            "upstream": 5.2,
            "downstream": 4.5,
            "level": 55.0,
            "inflow": 100.0,
            "outflow": 100.0
        },
        {
            "name": "Level Imbalance",
            "upstream": 5.2,
            "downstream": 5.0,
            "level": 65.0,
            "inflow": 120.0,
            "outflow": 95.0
        }
    ]

    report = []
    for scenario in scenarios:
        pressure_result = analyzer.analyze_pressure_system(
            scenario["upstream"],
            scenario["downstream"]
        )
        level_result = analyzer.analyze_level_system(
            scenario["level"],
            scenario["inflow"],
            scenario["outflow"]
        )

        report.append({
            "scenario": scenario["name"],
            "pressure_analysis": asdict(pressure_result),
            "level_analysis": asdict(level_result)
        })

    return report


async def main():
    """Main entry point."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        # Generate static report
        report = generate_report()
        print(json.dumps(report, indent=2, default=str))
    else:
        # Run interactive monitoring
        assistant = AIAssistant()
        await assistant.monitor_loop()


if __name__ == "__main__":
    # Run the demo
    print(__doc__)
    print("\nUsage:")
    print("  python demo.py           # Run interactive monitoring")
    print("  python demo.py --report  # Generate analysis report\n")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")
