import base64
from enum import IntEnum
from typing import Union, Optional

from TonTools.Contracts.Jetton import Jetton, JettonWallet
from TonTools.Providers.TonCenterClient import TonCenterClient
from tonsdk.boc import Cell
from tonsdk.utils import TonCurrencyEnum, to_nano, Address

from ...constants import ZERO_ADDRESS
from ..invoice import InvoiceConfig, INVOICE_CODE, InvoiceContract, Invoice
from ._types import InvoiceInfo, PurchaseRequestInvoice
from ._code import STORE_VERSION, STORE_CODE
from ._contract import StoreContract
from ._messages import build_activate_store_message, build_edit_store_message, \
    build_deactivate_store_message, build_issue_invoice_message, build_request_purchase_message, \
    build_request_purchase_with_jettons_message, build_full_code_upgrade_message
from ...currency import Currencies
from ...enums import DeeplinkFormat
from ...network import Sender
from ._deeplink import build_user_payment_link, build_user_payment_with_jettons_link


class StoreFees(IntEnum):
    DEPLOY = to_nano("0.005", TonCurrencyEnum.ton)
    EDIT = to_nano("0.005", TonCurrencyEnum.ton)
    ACTIVATE = to_nano("0.005", TonCurrencyEnum.ton)
    DEACTIVATE = to_nano("0.005", TonCurrencyEnum.ton)
    ISSUE_INVOICE = to_nano("0.042", TonCurrencyEnum.ton)
    REQUEST_PURCHASE = to_nano("0.05", TonCurrencyEnum.ton)
    FULL_UPGRADE = to_nano("0.006", TonCurrencyEnum.ton)
    INVOICE_UPGRADE = to_nano("0.006", TonCurrencyEnum.ton)
    REQUEST_PURCHASE_JETTON = to_nano("0.6", TonCurrencyEnum.ton)


class Store:

    def __init__(self, address: str, client: TonCenterClient, sender: Optional[Sender] = None):
        self.address = address
        self._sender = sender
        self._client = client
        self._wrapper = StoreContract(address=address, client=client)

    def get_address(self):
        return self.address

    async def edit(self, name: str, description: str, image: str, webhook: str, mcc_code: int):
        """
        This method edits the store data

        :param name: New store name
        :param description: New store description
        :param image: New store image URL
        :param webhook: New store webhook URL
        :param mcc_code: New store MCC code
        """

        if not self._sender:
            raise Exception("This store is read-only. Pass the sender to the constructor to make changes.")

        await self._sender.send(
            StoreFees.EDIT,
            Address(self.address),
            build_edit_store_message(name, description, image, webhook, mcc_code)
        )

    async def activate(self):
        """
        This method activates the store
        """

        if not self._sender:
            raise Exception("This store is read-only. Pass the sender to the constructor to make changes.")

        await self._sender.send(
            StoreFees.ACTIVATE,
            Address(self.address),
            build_activate_store_message()
        )

    async def deactivate(self):
        """
        This method deactivates the store
        """

        if not self._sender:
            raise Exception("This store is read-only. Pass the sender to the constructor to make changes.")

        await self._sender.send(
            StoreFees.DEACTIVATE,
            Address(self.address),
            build_deactivate_store_message()
        )

    async def issue_invoice(self, invoice: InvoiceInfo) -> Invoice:
        """
        This method issues the invoice

        :param invoice: invoice info. Amount must be a rational number, e.g. 1.5 (TON/jUSDT, etc.)
        :return: Invoice object after the transaction is sent
        """

        if not self._sender:
            raise Exception("This store is read-only. Pass the sender to the constructor to make changes.")

        await self._sender.send(
            StoreFees.ISSUE_INVOICE,
            Address(self.address),
            build_issue_invoice_message(
                invoice.has_customer,
                invoice.customer,
                invoice.invoice_id,
                invoice.metadata,
                invoice.amount * pow(10, invoice.currency.decimals),
                invoice.currency != Currencies.TON,
                invoice.currency.address,
                invoice.currency.wallet_code
            )
        )

        owner = await self.get_owner()

        return Invoice(
            address=InvoiceContract(None, self._client, config=InvoiceConfig(
                self.address,
                owner.to_string(True, True, True),
                "EQD2wz8Rq5QDj9iK2Z_leGQu-Rup__y-Z4wo8Lm7-tSD6Iz2",
                invoice.has_customer,
                invoice.customer,
                invoice.invoice_id,
                invoice.metadata,
                invoice.amount * pow(10, invoice.currency.decimals),
                False,
                True,
                invoice.currency != Currencies.TON,
                invoice.currency.address,
                Cell.one_from_boc(base64.b64decode(invoice.currency.wallet_code))
            )).address.to_string(True, True, True),
            sender=self._sender,
            client=self._client
        )

    async def request_purchase(self, invoice: PurchaseRequestInvoice) -> Invoice:
        """
        This method makes a purchase request to the store from the customer's side.

        :param invoice: invoice info. Amount must be a rational number, e.g. 1.5 (TON/jUSDT, etc.)
        :return: Invoice object after the transaction is sent
        """

        if not self._sender:
            raise Exception("This store is read-only. Pass the sender to the constructor to make changes.")

        merchant_address = await self.get_owner()

        if invoice.currency == Currencies.TON:
            await self._sender.send(
                to_nano(str(invoice.amount), TonCurrencyEnum.ton) + StoreFees.REQUEST_PURCHASE,
                Address(self.address),
                build_request_purchase_message(
                    invoice.invoice_id,
                    to_nano(str(invoice.amount), TonCurrencyEnum.ton),
                    invoice.metadata
                )
            )
            return Invoice(
                address=InvoiceContract(None, self._client, config=InvoiceConfig(
                    self.address,
                    merchant_address.to_string(True, True, True),
                    "EQD2wz8Rq5QDj9iK2Z_leGQu-Rup__y-Z4wo8Lm7-tSD6Iz2",
                    False,
                    Address(ZERO_ADDRESS).to_string(True, True, True),
                    invoice.invoice_id,
                    invoice.metadata,
                    invoice.amount * pow(10, invoice.currency.decimals),
                    False,
                    True,
                    False,
                    invoice.currency.address,
                    Cell.one_from_boc(base64.b64decode(invoice.currency.wallet_code))
                )).address.to_string(True, True, True),
                sender=self._sender,
                client=self._client
            )

        if not invoice.customer:
            raise ValueError("Customer address is required")

        Address(invoice.customer)  # validate address

        jetton_wallet: JettonWallet = await Jetton(invoice.currency.address, self._client).get_jetton_wallet(
            invoice.customer)
        await self._sender.send(
            StoreFees.REQUEST_PURCHASE_JETTON,
            Address(jetton_wallet.address),
            build_request_purchase_with_jettons_message(
                invoice.invoice_id,
                invoice.amount * pow(10, invoice.currency.decimals),
                invoice.metadata,
                self.address,
                invoice.currency.address,
                invoice.currency.wallet_code
            )
        )
        return Invoice(
            address=InvoiceContract(None, self._client, config=InvoiceConfig(
                self.address,
                merchant_address.to_string(True, True, True),
                "EQD2wz8Rq5QDj9iK2Z_leGQu-Rup__y-Z4wo8Lm7-tSD6Iz2",
                False,
                Address(ZERO_ADDRESS).to_string(True, True, True),
                invoice.invoice_id,
                invoice.metadata,
                invoice.amount * pow(10, invoice.currency.decimals),
                False,
                True,
                True,
                invoice.currency.address,
                Cell.one_from_boc(base64.b64decode(invoice.currency.wallet_code))
            )).address.to_string(True, True, True),
            sender=self._sender,
            client=self._client
        )

    async def get_request_purchase_link(
            self,
            invoice: PurchaseRequestInvoice,
            url_format: DeeplinkFormat = DeeplinkFormat.TON
    ) -> str:
        """
        This method returns the universal link for the purchase request by customer.

        :param invoice: invoice info. Amount must be a rational number, e.g. 1.5 (TON/jUSDT, etc.)
        :param url_format: deeplink format. Default is TON
        :return: Universal payment link for the purchase request
        """
        if invoice.currency == Currencies.TON:
            return build_user_payment_link(
                self.address,
                invoice.amount,
                invoice.invoice_id,
                StoreFees.REQUEST_PURCHASE,
                invoice.metadata,
                url_format
            )

        if not invoice.customer:
            raise ValueError("Customer address is required for jetton payment requests")

        Address(invoice.customer)  # validate address

        jetton_wallet: JettonWallet = await Jetton(invoice.currency.address, self._client).get_jetton_wallet(
            invoice.customer)

        return build_user_payment_with_jettons_link(
            self.address,
            jetton_wallet.address,
            invoice.currency.address,
            invoice.currency.wallet_code,
            invoice.currency.decimals,
            invoice.amount,
            invoice.invoice_id,
            invoice.metadata,
            StoreFees.REQUEST_PURCHASE_JETTON,
            url_format
        )

    async def apply_update(self, new_data: Optional[Cell] = None):
        if not self._sender:
            raise Exception("This store is read-only. Pass the sender to the constructor to make changes.")

        await self._sender.send(
            StoreFees.FULL_UPGRADE,
            Address(self.address),
            build_full_code_upgrade_message(
                Cell.one_from_boc(base64.b64decode(STORE_CODE)),
                Cell.one_from_boc(base64.b64decode(INVOICE_CODE)),
                new_data is not None,
                new_data
            )
        )

    async def get_owner(self) -> Address:
        return await self._wrapper.get_store_owner()

    async def get_name(self) -> str:
        return await self._wrapper.get_store_name()

    async def get_description(self) -> str:
        return await self._wrapper.get_store_description()

    async def get_image(self) -> str:
        return await self._wrapper.get_store_image()

    async def get_webhook(self) -> str:
        return await self._wrapper.get_store_webhook()

    async def get_mcc_code(self) -> int:
        return await self._wrapper.get_store_mcc_code()

    async def is_active(self) -> bool:
        return await self._wrapper.get_store_active()

    async def get_version(self) -> int:
        return await self._wrapper.get_store_version()

    async def get_invoice_code(self, as_base64: bool = False) -> Union[Cell, str]:
        invoice_code = await self._wrapper.get_store_invoice_code()
        return base64.b64encode(invoice_code.to_boc()) if as_base64 else invoice_code

    async def get_data(self, version: int = STORE_VERSION):
        return await self._wrapper.get_store_data(version)

    async def should_upgrade_self(self) -> bool:
        version = await self.get_version()
        return version < STORE_VERSION

    async def should_upgrade_invoice(self) -> bool:
        invoice_code = await self.get_invoice_code(True)
        return invoice_code != INVOICE_CODE
