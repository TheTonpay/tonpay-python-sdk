from tonsdk.utils import Address

from ._messages import build_pay_invoice_message, build_pay_invoice_with_jettons_message
from ...enums import DeeplinkFormat
from ...utils.deeplink import build_message_deeplink


def build_store_payment_link(
        invoice_address: str,
        amount: int,
        url_format: DeeplinkFormat = "ton"
) -> str:
    if amount <= 0:
        raise ValueError("Amount must be positive")

    Address(invoice_address)  # validate address

    return build_message_deeplink(
        Address(invoice_address),
        amount,
        build_pay_invoice_message(),
        url_format
    )


def build_store_payment_with_jettons_link(
        invoice_address: str,
        amount: int,
        jetton_amount: int,
        jetton_wallet_address: str,
        url_format: DeeplinkFormat = "ton"
) -> str:
    if amount <= 0:
        raise ValueError("Amount must be positive")

    if jetton_amount <= 0:
        raise ValueError("Jetton amount must be positive")

    Address(invoice_address)  # validate address

    Address(jetton_wallet_address)  # validate address

    return build_message_deeplink(
        Address(jetton_wallet_address),
        amount,
        build_pay_invoice_with_jettons_message(jetton_amount, invoice_address),
        url_format
    )
