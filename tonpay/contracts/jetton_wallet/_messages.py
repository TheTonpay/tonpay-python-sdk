from tonsdk.boc import Cell, begin_cell
from tonsdk.utils import Address

from ._opcodes import JettonWalletOpCodes


def build_send_jettons_message(
        amount: int,
        to_address: str,
        response_address: str,
        forward_payload_fee: int,
        forward_payload: Cell or None,
        put_payload_in_ref: bool
) -> Cell:
    message = (
        begin_cell()
        .store_uint(JettonWalletOpCodes.OP_JETTON_TRANSFER, 32)
        .store_uint(0, 64)
        .store_coins(amount)
        .store_address(Address(to_address))
        .store_address(Address(response_address))
        .store_bit(0)
        .store_coins(forward_payload_fee)
        .store_bit(1 if put_payload_in_ref else 0)
    )

    if put_payload_in_ref:
        message.store_ref(forward_payload)
    else:
        message.store_cell(forward_payload if forward_payload else None)

    return message.end_cell()
