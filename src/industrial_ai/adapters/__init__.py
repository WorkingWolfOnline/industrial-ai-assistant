"""协议适配器：统一数据访问接口，隔离上层与具体工业协议。"""

from .base import DataAdapter
from .simulation import SimulationAdapter

__all__ = ["DataAdapter", "SimulationAdapter"]

try:
    from .opcua import OPCUAAdapter  # noqa: F401

    __all__.append("OPCUAAdapter")
except ImportError:  # asyncua 未安装时优雅降级
    pass
