from typing import Optional

from TonTools.Providers.TonCenterClient import TonCenterClient

from .contracts.invoice import Invoice
from .contracts.store import Store
from .enums import TonNetwork
from .network import Sender
from .utils.ton_access import get_http_endpoint


class Tonpay:
    __inner_key = object()

    def __init__(self, ton_network: TonNetwork, client: TonCenterClient, sender: Optional[Sender], key: object):
        assert key == Tonpay.__inner_key, "Tonpay is a singleton. Use Tonpay.create() instead"

        self.network = ton_network.value
        self._sender = sender
        self._client = client

    @classmethod
    async def create(cls, ton_network: TonNetwork, sender: Optional[Sender] = None):
        endpoint = await get_http_endpoint({'network': ton_network.value, 'protocol': "rest"})
        client = TonCenterClient(base_url=endpoint, testnet=ton_network == TonNetwork.TESTNET)
        return cls(ton_network, client, sender, cls.__inner_key)

    def get_store(self, address) -> Store:
        return Store(address, self._client, self._sender)

    def get_invoice(self, address) -> Invoice:
        return Invoice(address, self._client, self._sender)
