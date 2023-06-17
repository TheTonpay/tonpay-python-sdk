import random
from typing import List, Optional

from tonpay.utils.ton_access._node import Nodes


class Access:
    nodes: Nodes
    host: str
    url_version: int

    def __init__(self):
        self.host = "ton.access.orbs.network"
        self.url_version = 1
        self.nodes = Nodes()

    async def init(self):
        await self.nodes.init(f"https://{self.host}/mngr/nodes?npm_version=2.3.1")

    @staticmethod
    def make_protonet(edge_protocol: str, network: str) -> str:
        res = ""
        if edge_protocol == "toncenter-api-v2":
            res += "v2-"
        elif edge_protocol == "ton-api-v4":
            res += "v4-"
        res += network
        return res

    @staticmethod
    def weighted_random(nodes: List[dict]) -> Optional[dict]:
        sum_weights = sum(node["Weight"] for node in nodes)
        rnd = random.randint(0, sum_weights - 1)

        cur = 0
        for node in nodes:
            if cur <= rnd < cur + node["Weight"]:
                return node
            cur += node["Weight"]
        return None

    def build_urls(
            self,
            network: str = "mainnet",
            edge_protocol: str = "toncenter-api-v2",
            suffix: str = "",
            single: bool = False
    ) -> List[str]:
        if not suffix:
            suffix = ""
        if not edge_protocol:
            edge_protocol = "toncenter-api-v2"
        if not network:
            network = "mainnet"

        suffix = suffix.lstrip("/")

        res = []
        protonet = self.make_protonet(edge_protocol, network)
        healthy_nodes = self.nodes.get_healthy_for(protonet)
        if not healthy_nodes:
            raise ValueError(f"no healthy nodes for {protonet}")

        if single and healthy_nodes:
            chosen = self.weighted_random(healthy_nodes)
            if not chosen:
                raise ValueError("weighted_random returned empty")
            healthy_nodes = [chosen]

        for node in healthy_nodes:
            url = f"https://{self.host}/{node['NodeId']}/{self.url_version}/{network}/{edge_protocol}/"
            if suffix:
                url += f"{suffix}"
            res.append(url)
        return res


async def get_endpoints(
        network: str = "mainnet",
        edge_protocol: str = "toncenter-api-v2",
        suffix: str = "",
        single: bool = False
) -> List[str]:
    access = Access()
    await access.init()
    return access.build_urls(network, edge_protocol, suffix, single)


async def get_http_endpoints(config: dict = None, single: bool = False) -> List[str]:
    network = config.get("network") if config and config.get("network") else "mainnet"
    suffix = "jsonRPC" if not config or config.get("protocol") != "rest" else ""
    return await get_endpoints(network, "toncenter-api-v2", suffix, single)


async def get_http_endpoint(config: dict = None) -> str:
    endpoints = await get_http_endpoints(config, True)
    return endpoints[0]


async def get_http_v4_endpoints(config: dict = None, single: bool = False) -> List[str]:
    network = config.get("network") if config and config.get("network") else "mainnet"
    if config and config.get("protocol") == "json-rpc":
        raise ValueError("config.protocol json-rpc is not supported for get_http_v4_endpoints")

    suffix = ""
    return await get_endpoints(network, "ton-api-v4", suffix, single)


async def get_http_v4_endpoint(config: dict = None) -> str:
    endpoints = await get_http_v4_endpoints(config, True)
    return endpoints[0]
