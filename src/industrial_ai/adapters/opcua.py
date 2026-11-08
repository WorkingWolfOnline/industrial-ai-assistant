"""OPC UA 适配器（可选依赖，异步接口）。

使用前需安装 ``asyncua``（``pip install asyncua``）。

⚠️ 重要说明：
- OPC UA 是异步协议，本适配器提供 **异步接口**，需在事件循环中使用
  （例如 ``asyncio.run(main())`` 或 MCP / FastAPI 等异步框架内）。
- 连接真实 DCS/SCADA 前务必：只配置只读权限、经过安全评估、
  由合格的工业自动化专业人员操作。
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from ..models import ProcessParameter


class OPCUAAdapter:
    """通过 OPC UA 异步读取工业过程数据（只读）。

    用法::

        async def main():
            adapter = OPCUAAdapter("opc.tcp://dcs-server:4840")
            await adapter.connect()
            try:
                p = await adapter.read_parameter("ns=2;s=Reactor.Temperature")
            finally:
                await adapter.disconnect()
    """

    def __init__(self, endpoint: str, security_policy: str = "Basic256Sha256"):
        self.endpoint = endpoint
        self.security_policy = security_policy
        self.read_only = True
        self._client = None

    async def connect(self) -> None:
        """建立 OPC UA 连接（复用连接，无需每次读取前重复调用）。"""
        from asyncua import Client  # 延迟导入，避免未安装时崩溃

        if self._client is not None:
            return
        self._client = Client(url=self.endpoint)
        await self._client.connect()

    async def disconnect(self) -> None:
        """断开连接。"""
        if self._client is not None:
            await self._client.disconnect()
            self._client = None

    async def read_parameter(self, node_id: str) -> Optional[ProcessParameter]:
        """异步读取单个点位。"""
        if self._client is None:
            await self.connect()
        node = self._client.get_node(node_id)
        value = await node.read_value()
        return ProcessParameter(
            name=node_id,
            value=float(value),
            unit="",
            timestamp=datetime.now(),
            normal_range=(0.0, 100.0),
        )

    async def read_multiple(self, node_ids: List[str]) -> Dict[str, ProcessParameter]:
        """异步读取多个点位，返回 ``{node_id: parameter}``。"""
        results: Dict[str, ProcessParameter] = {}
        for nid in node_ids:
            param = await self.read_parameter(nid)
            if param is not None:
                results[nid] = param
        return results
