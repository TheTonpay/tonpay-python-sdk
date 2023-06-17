import base64
from typing import Optional

from TonTools.Contracts.Contract import Contract as TonToolsContract
from TonTools.Providers.TonCenterClient import TonCenterClient
from tonsdk.boc import Cell, begin_cell
from tonsdk.contract import Contract
from tonsdk.utils import Address

from ...constants import ZERO_ADDRESS
from ._code import INVOICE_CODE, INVOICE_VERSION, SUPPORTED_VERSIONS
from ._types import InvoiceData, InvoiceConfig
from ...utils import cell_to_string, string_to_cell, string_as_comment


class InvoiceContract(Contract):

    def __init__(self, address: Optional[str], client: TonCenterClient, **kwargs):
        super().__init__(**kwargs)
        self.options["code"] = Cell.one_from_boc(base64.b64decode(INVOICE_CODE))
        self.client = client
        if address:
            self.network_contract = TonToolsContract(address=address, provider=client)

    def create_data_cell(self) -> Cell:
        config: InvoiceConfig = self.options.get('config', None)

        if not config:
            raise Exception('Invoice config is required')

        return (
            begin_cell()
            .store_address(Address(config.store))
            .store_address(Address(config.merchant))
            .store_address(Address("EQD2wz8Rq5QDj9iK2Z_leGQu-Rup__y-Z4wo8Lm7-tSD6Iz2"))
            .store_int(-1 if config.has_customer else 0, 2)
            .store_ref(
                begin_cell()
                .store_address(Address(config.customer) if config.has_customer else Address(ZERO_ADDRESS))
                .end_cell()
            )
            .store_ref(string_to_cell(string_as_comment(config.invoice_id)))
            .store_ref(string_to_cell(string_as_comment(config.metadata)))
            .store_uint(config.amount, 64)
            .store_int(-1 if config.paid else 0, 2)
            .store_int(-1 if config.active else 0, 2)
            .store_ref(
                begin_cell()
                .store_int(-1 if config.accepts_jetton else 0, 2)
                .store_address(
                    Address(config.jetton_master_address) if config.accepts_jetton else Address(ZERO_ADDRESS))
                .store_ref(config.jetton_wallet_code)
                .end_cell()
            )
            .end_cell()
        )

    def try_init_network_contract(self):
        if not self.network_contract:
            self.network_contract = TonToolsContract(address=self.address, provider=self.client)

    async def get_invoice_store(self) -> Address:
        self.try_init_network_contract()
        raw_data = await self.network_contract.run_get_method('get_invoice_store', [])
        return Cell.one_from_boc(base64.b64decode(raw_data[0][1]['bytes'])).begin_parse().read_msg_addr()

    async def get_invoice_merchant(self) -> Address:
        self.try_init_network_contract()
        raw_data = await self.network_contract.run_get_method('get_invoice_merchant', [])
        return Cell.one_from_boc(base64.b64decode(raw_data[0][1]['bytes'])).begin_parse().read_msg_addr()

    async def get_invoice_customer(self) -> Address:
        self.try_init_network_contract()
        raw_data = await self.network_contract.run_get_method('get_invoice_customer', [])
        return Cell.one_from_boc(base64.b64decode(raw_data[0][1]['bytes'])).begin_parse().read_msg_addr()

    async def get_invoice_has_customer(self) -> bool:
        self.try_init_network_contract()
        raw_data = await self.network_contract.run_get_method('get_invoice_has_customer', [])
        return int(raw_data[0][1], 16) == -1

    async def get_invoice_id(self) -> str:
        self.try_init_network_contract()
        raw_data = await self.network_contract.run_get_method('get_invoice_id', [])
        return cell_to_string(Cell.one_from_boc(base64.b64decode(raw_data[0][1]['bytes'])))[4:]

    async def get_invoice_metadata(self) -> str:
        self.try_init_network_contract()
        raw_data = await self.network_contract.run_get_method('get_invoice_metadata', [])
        return cell_to_string(Cell.one_from_boc(base64.b64decode(raw_data[0][1]['bytes'])))[4:]

    async def get_invoice_amount(self) -> int:
        self.try_init_network_contract()
        raw_data = await self.network_contract.run_get_method('get_invoice_amount', [])
        return int(raw_data[0][1], 16)

    async def get_invoice_paid(self) -> bool:
        self.try_init_network_contract()
        raw_data = await self.network_contract.run_get_method('get_invoice_paid', [])
        return int(raw_data[0][1], 16) == -1

    async def get_invoice_active(self) -> bool:
        self.try_init_network_contract()
        raw_data = await self.network_contract.run_get_method('get_invoice_active', [])
        return int(raw_data[0][1], 16) == -1

    async def get_invoice_accepts_jetton(self) -> bool:
        self.try_init_network_contract()
        raw_data = await self.network_contract.run_get_method('get_invoice_accepts_jetton', [])
        return int(raw_data[0][1], 16) == -1

    async def get_invoice_jetton_master_address(self) -> Address:
        self.try_init_network_contract()
        raw_data = await self.network_contract.run_get_method('get_invoice_jetton_master_address', [])
        return Cell.one_from_boc(base64.b64decode(raw_data[0][1]['bytes'])).begin_parse().read_msg_addr()

    async def get_invoice_jetton_wallet_code(self) -> Cell:
        self.try_init_network_contract()
        raw_data = await self.network_contract.run_get_method('get_invoice_jetton_wallet_code', [])
        return Cell.one_from_boc(base64.b64decode(raw_data[0][1]['bytes']))

    async def get_invoice_version(self) -> int:
        self.try_init_network_contract()
        raw_data = await self.network_contract.run_get_method('get_invoice_version', [])
        return int(raw_data[0][1], 16)

    async def get_invoice_data(self, version: int = INVOICE_VERSION) -> InvoiceData:
        self.try_init_network_contract()
        raw_data = await self.network_contract.run_get_method('get_invoice_data', [])

        # find item with specified version
        mapper = next((item for item in SUPPORTED_VERSIONS if item['version'] == version), None)

        if not mapper:
            raise Exception(f'Version {version} is not supported')

        return mapper.get('map_data')(raw_data)
