import base64
from typing import Optional

from tonsdk.boc import begin_cell
from tonsdk.utils import Address, to_nano, TonCurrencyEnum

from ._messages import build_request_purchase_message, build_request_purchase_with_jettons_message
from ...enums import DeeplinkFormat
from ...utils.deeplink import build_message_deeplink


def build_user_payment_link(
        store_address: str,
        amount: int,
        invoice_id: str,
        gas_fee: int,
        metadata: Optional[str],
        url_format: DeeplinkFormat = DeeplinkFormat.TON
) -> str:
    if amount <= 0:
        raise ValueError("Amount must be positive")

    Address(store_address)  # validate address

    if len(invoice_id) == 0:
        raise ValueError("Invoice id must not be empty")

    if len(invoice_id) > 120:
        raise ValueError("Invoice id must not be longer than 120 characters")

    if metadata and len(metadata) > 500:
        raise ValueError("Metadata must not be longer than 500 characters")

    return build_message_deeplink(
        Address(store_address),
        to_nano(str(amount), TonCurrencyEnum.ton) + gas_fee,
        build_request_purchase_message(invoice_id, to_nano(str(amount), TonCurrencyEnum.ton), metadata),
        url_format
    )


def build_user_payment_with_jettons_link(
        store_address: str,
        jetton_wallet_address: str,
        jetton_master_address: str,
        jetton_wallet_code_base64: str,
        jetton_decimals: int,
        amount: int,
        invoice_id: str,
        metadata: Optional[str],
        gas_fee: int,
        url_format: DeeplinkFormat = "ton"
) -> str:
    if amount <= 0:
        raise ValueError("Amount must be positive")

    Address(jetton_wallet_address)  # validate address

    Address(jetton_master_address)  # validate address

    if jetton_wallet_code_base64 == base64.urlsafe_b64encode(begin_cell().end_cell().to_boc()):
        raise ValueError("Jetton wallet code must not be empty")

    if jetton_decimals <= 0:
        raise ValueError("Jetton decimals must be positive")

    Address(store_address)  # validate address

    if len(invoice_id) == 0:
        raise ValueError("Invoice id must not be empty")

    if len(invoice_id) > 120:
        raise ValueError("Invoice id must not be longer than 120 characters")

    if metadata and len(metadata) > 500:
        raise ValueError("Metadata must not be longer than 500 characters")

    return build_message_deeplink(
        Address(jetton_wallet_address),
        gas_fee,
        build_request_purchase_with_jettons_message(
            invoice_id,
            int(amount * (10 ** jetton_decimals)),
            metadata,
            store_address,
            jetton_master_address,
            jetton_wallet_code_base64
        ),
        url_format
    )
