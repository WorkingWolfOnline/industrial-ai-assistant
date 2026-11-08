"""适配器统一接口。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from ..models import ProcessParameter


class DataAdapter(ABC):
    """所有工业数据适配器的统一接口。

    上层（分析、MCP 工具）只依赖本接口，不关心底层是
    OPC UA 还是仿真器。默认只读。
    """

    read_only: bool = True

    @abstractmethod
    def read_parameter(self, tag_name: str) -> Optional[ProcessParameter]:
        """读取单个点位。"""

    def read_multiple(self, tag_names: List[str]) -> Dict[str, ProcessParameter]:
        """读取多个点位，返回 ``{tag: parameter}`` 字典。"""
        results: Dict[str, ProcessParameter] = {}
        for tag in tag_names:
            param = self.read_parameter(tag)
            if param is not None:
                results[tag] = param
        return results
