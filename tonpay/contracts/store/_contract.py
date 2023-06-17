import base64

from TonTools.Providers.TonCenterClient import TonCenterClient
from TonTools.Contracts.Contract import Contract as TonToolsContract
from tonsdk.boc import Builder, Cell
from tonsdk.contract import Contract
from tonsdk.utils import Address

from ._code import STORE_CODE, SUPPORTED_VERSIONS, StoreData, STORE_VERSION
from ._types import StoreConfig
from ...utils import string_to_cell, cell_to_string, string_as_comment


class StoreContract(Contract):

    def __init__(self, address: str, client: TonCenterClient, **kwargs):
        super().__init__(**kwargs)
        self.code = Cell.one_from_boc(base64.b64decode(STORE_CODE))
        self.network_contract = TonToolsContract(address=address, provider=client)

    def create_data_cell(self):
        config: StoreConfig = self.options.get('config', None)

        if not config:
            raise Exception('Store config is required')

        data = Builder()
        data.store_address(Address(config.owner))
        data.store_ref(string_to_cell(string_as_comment(config.name)))
        data.store_ref(string_to_cell(string_as_comment(config.description)))
        data.store_ref(
            Builder()
            .store_ref(string_to_cell(string_as_comment(config.image)))
            .store_ref(string_to_cell(string_as_comment(config.webhook)))
            .end_cell()
        )
        data.store_uint(config.mcc_code, 16)
        data.store_int(-1 if config.active else 0, 2)
        data.store_ref(config.invoice_code)

        return data.end_cell()

    async def get_store_owner(self) -> Address:
        raw_data = await self.network_contract.run_get_method('get_store_owner', [])
        return Cell.one_from_boc(base64.b64decode(raw_data[0][1]['bytes'])).begin_parse().read_msg_addr()

    async def get_store_name(self) -> str:
        raw_data = await self.network_contract.run_get_method('get_store_name', [])
        return cell_to_string(Cell.one_from_boc(base64.b64decode(raw_data[0][1]['bytes'])))[4:]

    async def get_store_description(self) -> str:
        raw_data = await self.network_contract.run_get_method('get_store_description', [])
        return cell_to_string(Cell.one_from_boc(base64.b64decode(raw_data[0][1]['bytes'])))[4:]

    async def get_store_image(self) -> str:
        raw_data = await self.network_contract.run_get_method('get_store_image', [])
        return cell_to_string(Cell.one_from_boc(base64.b64decode(raw_data[0][1]['bytes'])))[4:]

    async def get_store_webhook(self) -> str:
        raw_data = await self.network_contract.run_get_method('get_store_webhook', [])
        return cell_to_string(Cell.one_from_boc(base64.b64decode(raw_data[0][1]['bytes'])))[4:]

    async def get_store_mcc_code(self) -> int:
        raw_data = await self.network_contract.run_get_method('get_store_mcc_code', [])
        return int(raw_data[0][1], 16)

    async def get_store_active(self) -> bool:
        raw_data = await self.network_contract.run_get_method('get_store_active', [])
        return int(raw_data[0][1], 16) == -1

    async def get_store_invoice_code(self) -> Cell:
        raw_data = await self.network_contract.run_get_method('get_store_invoice_code', [])
        return Cell.one_from_boc(base64.b64decode(raw_data[0][1]['bytes']))

    async def get_store_version(self) -> int:
        raw_data = await self.network_contract.run_get_method('get_store_version', [])
        return int(raw_data[0][1], 16)

    async def get_store_data(self, version: int = STORE_VERSION) -> StoreData:
        raw_data = await self.network_contract.run_get_method('get_store_data', [])

        # find item with specified version
        mapper = next((item for item in SUPPORTED_VERSIONS if item['version'] == version), None)

        if not mapper:
            raise Exception(f'Version {version} is not supported')

        return mapper.get('map_data')(raw_data)
