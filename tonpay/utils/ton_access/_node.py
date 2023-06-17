import time
from typing import List, Set

import requests

STALE_PERIOD = 10 * 60 * 1000  # 10 Min


class Nodes:
    committee: Set[str]
    topology: List[dict]
    node_index: int
    init_time: int

    def __init__(self):
        self.node_index = -1
        self.committee = set()
        self.topology = []
        self.init_time = 0

    async def init(self, nodes_url: str):
        self.node_index = -1
        self.committee.clear()
        self.topology = []
        self.init_time = int(time.time() * 1000)

        try:
            response = requests.get(nodes_url)
            response.raise_for_status()
            data = response.json()
            topology = data
        except Exception as e:
            raise ValueError(f"exception in fetch({nodes_url}): {e}")

        # remove unhealthy nodes
        for node in topology:
            if node["Healthy"] == "1":
                self.topology.append(node)

        if len(self.topology) == 0:
            raise ValueError("no healthy nodes retrieved")

    def get_healthy_for(self, protonet: str) -> List[dict]:
        res = []
        stale_count = 0
        for node in self.topology:
            stale = self.init_time - node["Mngr"]["successTS"] > STALE_PERIOD
            if not stale and node["Weight"] > 0 and node["Mngr"]["health"].get(protonet, False):
                res.append(node)
            elif stale:
                stale_count += 1

        if stale_count == len(self.topology):
            raise ValueError("all nodes manager's data are stale")

        return res
