import base64
from typing import Union

from tonsdk.boc import begin_cell, Cell
from tonsdk.utils import Address, TonCurrencyEnum, to_nano

from ...constants import ZERO_ADDRESS
from ..jetton_wallet import build_send_jettons_message
from ._opcodes import StoreOpCodes
from ...utils import string_to_cell, string_as_comment


def build_edit_store_message(name: str, description: str, image: str, webhook: str, mcc_code: int) -> Cell:
    return (
        begin_cell()
        .store_uint(StoreOpCodes.EDIT_STORE, 32)
        .store_uint(0, 64)
        .store_ref(string_to_cell(string_as_comment(name)))
        .store_ref(string_to_cell(string_as_comment(description)))
        .store_ref(string_to_cell(string_as_comment(image)))
        .store_ref(string_to_cell(string_as_comment(webhook)))
        .store_uint(mcc_code, 16)
        .end_cell()
    )


def build_activate_store_message() -> Cell:
    return (
        begin_cell()
        .store_uint(StoreOpCodes.ACTIVATE_STORE, 32)
        .store_uint(0, 64)
        .end_cell()
    )


def build_deactivate_store_message() -> Cell:
    return (
        begin_cell()
        .store_uint(StoreOpCodes.DEACTIVATE_STORE, 32)
        .store_uint(0, 64)
        .end_cell()
    )


def build_issue_invoice_message(
        has_customer: bool,
        customer: str,
        invoice_id: str,
        metadata: str,
        amount: int,
        accepts_jetton: bool,
        jetton_master_address: str,
        jetton_wallet_code: str
) -> Cell:
    return (
        begin_cell()
        .store_uint(StoreOpCodes.ISSUE_INVOICE, 32)
        .store_uint(0, 64)
        .store_int(-1 if has_customer else 0, 2)
        .store_ref(
            begin_cell()
            .store_address(Address(customer) if has_customer else Address(ZERO_ADDRESS))
            .end_cell()
        )
        .store_ref(string_to_cell(string_as_comment(invoice_id)))
        .store_ref(string_to_cell(string_as_comment(metadata)))
        .store_uint(amount, 64)
        .store_int(-1 if accepts_jetton else 0, 2)
        .store_address(Address(jetton_master_address))
        .store_ref(Cell.one_from_boc(base64.b64decode(jetton_wallet_code)))
        .end_cell()
    )


def build_request_purchase_message(invoice_id: str, amount: int, metadata: Union[str, None]) -> Cell:
    return (
        begin_cell()
        .store_uint(StoreOpCodes.REQUEST_PURCHASE, 32)
        .store_uint(0, 64)
        .store_ref(string_to_cell(string_as_comment(invoice_id)))
        .store_ref(string_to_cell(string_as_comment(metadata if metadata is not None else "")))
        .store_uint(amount, 64)
        .end_cell()
    )


def build_request_purchase_with_jettons_message(
        invoice_id: str,
        amount: int,
        metadata: Union[str, None],
        store_address: str,
        jetton_master_address: str,
        jetton_wallet_code: str
) -> Cell:
    return build_send_jettons_message(
        amount,
        store_address,
        store_address,
        to_nano("0.5", TonCurrencyEnum.ton),
        begin_cell()
        .store_uint(StoreOpCodes.REQUEST_PURCHASE, 32)
        .store_ref(Cell.one_from_boc(base64.b64decode(jetton_wallet_code)))
        .store_address(Address(jetton_master_address))
        .store_ref(string_to_cell(string_as_comment(invoice_id)))
        .store_ref(string_to_cell(string_as_comment(metadata if metadata is not None else "")))
        .store_uint(amount, 64)
        .end_cell(),
        True
    )


def build_full_code_upgrade_message(
        store_code: Cell,
        invoice_code: Cell,
        has_new_data: bool,
        new_data: Union[Cell, None]
) -> Cell:
    if has_new_data and not new_data:
        raise ValueError("Can't build message if has_new_data is true but new_data is None")

    return (
        begin_cell()
        .store_uint(StoreOpCodes.UPGRADE_CODE_FULL, 32)
        .store_uint(0, 64)
        .store_ref(store_code)
        .store_ref(invoice_code)
        .store_int(-1 if has_new_data else 0, 2)
        .store_ref(new_data if new_data else begin_cell().end_cell())
        .end_cell()
    )


def build_store_code_upgrade_message(store_code: Cell, has_new_data: bool, new_data: Cell or None) -> Cell:
    if has_new_data and not new_data:
        raise ValueError("Can't build message if has_new_data is true but new_data is None")

    return (
        begin_cell()
        .store_uint(StoreOpCodes.UPGRADE_CODE_STORE, 32)
        .store_uint(0, 64)
        .store_ref(store_code)
        .store_int(-1 if has_new_data else 0, 2)
        .store_ref(new_data if new_data else begin_cell().end_cell())
        .end_cell()
    )


def build_invoice_code_upgrade_message(invoice_code: Cell) -> Cell:
    return (
        begin_cell()
        .store_uint(StoreOpCodes.UPGRADE_CODE_INVOICE, 32)
        .store_uint(0, 64)
        .store_ref(invoice_code)
        .end_cell()
    )
