from enum import IntEnum
from typing import Optional

from TonTools.Contracts.Jetton import JettonWallet, Jetton
from TonTools.Providers.TonCenterClient import TonCenterClient
from tonsdk.boc import Cell
from tonsdk.utils import to_nano, TonCurrencyEnum, Address

from ._types import InvoiceData
from ._code import INVOICE_VERSION
from ._contract import InvoiceContract
from ._messages import build_edit_invoice_message, build_activate_invoice_message, \
    build_deactivate_invoice_message, build_pay_invoice_message, build_pay_invoice_with_jettons_message
from ...currency import Currency, Currencies, get_currency_by_address
from ...enums import DeeplinkFormat
from ...network import Sender

from ._deeplink import build_store_payment_with_jettons_link, build_store_payment_link


class InvoiceFees(IntEnum):
    DEPLOY = to_nano("0.005", TonCurrencyEnum.ton)
    EDIT = to_nano("0.005", TonCurrencyEnum.ton)
    ACTIVATE = to_nano("0.005", TonCurrencyEnum.ton)
    DEACTIVATE = to_nano("0.005", TonCurrencyEnum.ton)
    PAY_WITH_JETTONS = to_nano("0.6", TonCurrencyEnum.ton)


class Invoice:

    def __init__(self, address: str, client: TonCenterClient, sender: Optional[Sender] = None):
        self.address = address
        self._sender = sender
        self._client = client
        self._wrapper = InvoiceContract(address=address, client=client)

    def get_address(self):
        return self.address

    async def edit(
            self,
            has_customer: bool,
            customer: str,
            invoice_id: str,
            metadata: str,
            amount: int,
            currency: Currency
    ):
        """
        This method edits the invoice data

        :param has_customer: If the invoice has a customer
        :param customer: New customer address or ZERO_ADDRESS if has_customer is False
        :param invoice_id: New invoice id
        :param metadata: New invoice metadata
        :param amount: New invoice amount, not in nanotons
        :param currency: New invoice currency
        """

        if not self._sender:
            raise Exception("This invoice is read-only. Pass the sender to the constructor to make changes.")

        await self._sender.send(
            InvoiceFees.EDIT,
            Address(self.address),
            build_edit_invoice_message(
                has_customer=has_customer,
                customer=customer,
                invoice_id=invoice_id,
                metadata=metadata,
                amount=amount * pow(10, currency.decimals),
                accepts_jetton=currency != Currencies.TON,
                jetton_master_address=currency.address,
                jetton_wallet_code=currency.wallet_code
            )
        )

    async def activate(self):
        """
        This method activates the invoice
        """

        if not self._sender:
            raise Exception("This invoice is read-only. Pass the sender to the constructor to make changes.")

        await self._sender.send(
            InvoiceFees.ACTIVATE,
            Address(self.address),
            build_activate_invoice_message()
        )

    async def deactivate(self):
        """
        This method deactivates the invoice
        """

        if not self._sender:
            raise Exception("This invoice is read-only. Pass the sender to the constructor to make changes.")

        await self._sender.send(
            InvoiceFees.DEACTIVATE,
            Address(self.address),
            build_deactivate_invoice_message()
        )

    async def pay(self, customer: Optional[str] = None):
        """
        This method pays the invoice

        :param customer: Address of the customer that will pay the invoice. Required if currency is not TON and
        invoice has no assigned customer
        """

        if not self._sender:
            raise Exception("This invoice is read-only. Pass the sender to the constructor to make changes.")

        invoice_data: InvoiceData = await self._wrapper.get_invoice_data()

        currency = get_currency_by_address(invoice_data.jetton_master_address)

        if currency is Currencies.TON:
            await self._sender.send(invoice_data.amount, Address(self.address), build_pay_invoice_message())
            return

        if not invoice_data.has_customer:
            if customer is None:
                raise ValueError("Customer address is required")
            Address(customer)

        user_address = customer or invoice_data.customer
        jetton_wallet: JettonWallet = await Jetton(invoice_data.jetton_master_address, self._client) \
            .get_jetton_wallet(user_address)

        await self._sender.send(
            InvoiceFees.PAY_WITH_JETTONS,
            Address(jetton_wallet.address),
            build_pay_invoice_with_jettons_message(invoice_data.amount, self.address)
        )

    async def get_payment_link(
            self,
            customer: Optional[str] = None,
            url_format: DeeplinkFormat = DeeplinkFormat.TON
    ) -> str:
        """
        This method returns the payment link for the user in the specified format

        :param customer: Address of the customer that will pay the invoice. Required if currency is not TON and
        invoice has no assigned customer
        :param url_format: deeplink format. Default is TON

        :return: payment link in the specified format
        """
        invoice_data = await self.get_data()
        currency = get_currency_by_address(invoice_data.jetton_master_address)

        if currency is Currencies.TON:
            return build_store_payment_link(
                self.address, invoice_data.amount, url_format
            )

        if not invoice_data.has_customer:
            if customer is None:
                raise ValueError("Customer address is required")
            Address(customer)

        user_address = customer or invoice_data.customer
        jetton_wallet: JettonWallet = await Jetton(invoice_data.jetton_master_address, self._client) \
            .get_jetton_wallet(user_address)

        return build_store_payment_with_jettons_link(
            self.address, InvoiceFees.PAY_WITH_JETTONS, invoice_data.amount, jetton_wallet.address, url_format
        )

    async def get_store(self) -> Address:
        return await self._wrapper.get_invoice_store()

    async def get_merchant(self) -> Address:
        return await self._wrapper.get_invoice_merchant()

    async def get_customer(self) -> Address:
        return await self._wrapper.get_invoice_customer()

    async def has_customer(self) -> bool:
        return await self._wrapper.get_invoice_has_customer()

    async def get_invoice_id(self) -> str:
        return await self._wrapper.get_invoice_id()

    async def get_metadata(self) -> str:
        return await self._wrapper.get_invoice_metadata()

    async def get_amount(self) -> int:
        return await self._wrapper.get_invoice_amount()

    async def is_paid(self) -> bool:
        return await self._wrapper.get_invoice_paid()

    async def is_active(self) -> bool:
        return await self._wrapper.get_invoice_active()

    async def accepts_jetton(self) -> bool:
        return await self._wrapper.get_invoice_accepts_jetton()

    async def get_jetton_master_address(self) -> Address:
        return await self._wrapper.get_invoice_jetton_master_address()

    async def get_jetton_wallet_code(self) -> Cell:
        return await self._wrapper.get_invoice_jetton_wallet_code()

    async def get_version(self) -> int:
        return await self._wrapper.get_invoice_version()

    async def get_data(self, version: int = INVOICE_VERSION) -> InvoiceData:
        return await self._wrapper.get_invoice_data(version)

    async def should_upgrade(self) -> bool:
        version = await self.get_version()
        return version < INVOICE_VERSION

    async def get_currency(self) -> Currency:
        invoice_data: InvoiceData = await self._wrapper.get_invoice_data()
        return get_currency_by_address(invoice_data.jetton_master_address)
