import base64
from typing import Optional

from tonsdk.boc import Cell
from tonsdk.utils import Address

from ...enums import DeeplinkFormat


def build_ton_deeplink(
        address: Address,
        amount: int,
        body: Optional[Cell] = None,
        state_init: Optional[Cell] = None,
        url_format: DeeplinkFormat = DeeplinkFormat.TON) -> str:
    return f"{'ton://' if url_format == DeeplinkFormat.TON else 'https://app.tonkeeper.com'}transfer" + \
        f"/{address.to_string(True, True, True)}?" + \
        f"amount={amount}" + \
        f"{'' if body is None else f'&bin={base64.urlsafe_b64encode(body.to_boc()).decode()}'}" + \
        f"{'' if state_init is None else f'&stateInit={base64.urlsafe_b64encode(state_init.to_boc()).decode()}'}"


def build_coins_transfer_deeplink(address: Address, amount: int) -> str:
    return build_ton_deeplink(address, amount)


def build_contract_deploy_deeplink(
        address: Address,
        amount: int,
        state_init: Cell,
        body: Optional[Cell] = None,
        url_format: DeeplinkFormat = DeeplinkFormat.TON) -> str:
    return build_ton_deeplink(address, amount, body, state_init, url_format)


def build_message_deeplink(
        address: Address,
        amount: int,
        body: Cell,
        url_format: DeeplinkFormat = DeeplinkFormat.TON) -> str:
    return build_ton_deeplink(address, amount, body, None, url_format)
