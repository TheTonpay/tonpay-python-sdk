from abc import ABC

from tonsdk.boc import Cell
from tonsdk.utils import Address


class Sender(ABC):
    async def send(self, value: int, address: Address, body: Cell, state_init: Cell = None):
        """
        This method should be implemented in subclasses. It should send a transaction to the blockchain.

        :param value:
        :param address:
        :param body:
        :param state_init:
        """
        pass
