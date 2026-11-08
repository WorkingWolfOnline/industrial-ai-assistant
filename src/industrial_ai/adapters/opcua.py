"""OPC UA 适配器（可选依赖）。

需要安装 ``asyncua`` 才能使用。连接真实 DCS/SCADA 前务必：
1. 只配置只读权限；
2. 经过安全评估；
3. 由合格的工业自动化专业人员操作。
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Dict, List, Optional

from ..models import ProcessParameter


class OPCUAAdapter:
    """通过 OPC UA 读取工业过程数据（只读）。"""

    def __init__(self, endpoint: str, security_policy: str = "Basic256Sha256"):
        self.endpoint = endpoint
        self.security_policy = security_policy
        self.read_only = True
        self._client = None

    async def connect(self) -> None:
        """建立 OPC UA 连接。"""
        from asyncua import Client  # 延迟导入，避免未安装时崩溃

        self._client = Client(url=self.endpoint)
        await self._client.connect()

    async def disconnect(self) -> None:
        if self._client is not None:
            await self._client.disconnect()

    def read_parameter(self, tag_name: str) -> Optional[ProcessParameter]:
        """同步读取（内部使用 asyncio.run 包裹异步调用）。"""
        return asyncio.run(self._read_async(tag_name))

    async def _read_async(self, node_id: str) -> Optional[ProcessParameter]:
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
