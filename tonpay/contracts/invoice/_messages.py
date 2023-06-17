import base64

from tonsdk.boc import Cell, begin_cell
from tonsdk.utils import Address, to_nano, TonCurrencyEnum

from ...constants import ZERO_ADDRESS
from ._opcodes import InvoiceOpCodes
from ..jetton_wallet import build_send_jettons_message
from ...utils import string_to_cell, string_as_comment


def build_edit_invoice_message(
        has_customer: bool,
        customer: str,
        invoice_id: str,
        metadata: str,
        amount: int,
        accepts_jetton: bool,
        jetton_master_address: str,
        jetton_wallet_code: str
) -> Cell:
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    if has_customer:
        Address(customer)

    if not invoice_id:
        raise ValueError("Invoice ID must be specified")

    if len(invoice_id) > 120:
        raise ValueError("Invoice ID must not be longer than 120 characters")

    if metadata and len(metadata) > 500:
        raise ValueError("Metadata must not be longer than 500 characters")

    if accepts_jetton:
        Address(jetton_master_address)

    if accepts_jetton and not jetton_wallet_code:
        raise ValueError("Jetton wallet code must be specified")

    jetton_wallet_code_cell = Cell.one_from_boc(base64.b64decode(jetton_wallet_code))
    if accepts_jetton and begin_cell().end_cell() == jetton_wallet_code_cell:
        raise ValueError("Invalid jetton wallet code, must not be empty cell")

    return (
        begin_cell()
        .store_uint(InvoiceOpCodes.EDIT_INVOICE, 32)
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
        .store_address(Address(jetton_master_address) if accepts_jetton else Address(ZERO_ADDRESS))
        .store_ref(jetton_wallet_code_cell)
        .end_cell()
    )


def build_deactivate_invoice_message() -> Cell:
    return (
        begin_cell()
        .store_uint(InvoiceOpCodes.DEACTIVATE_INVOICE, 32)
        .store_uint(0, 64)
        .end_cell()
    )


def build_activate_invoice_message() -> Cell:
    return (
        begin_cell()
        .store_uint(InvoiceOpCodes.ACTIVATE_INVOICE, 32)
        .store_uint(0, 64)
        .end_cell()
    )


def build_pay_invoice_message() -> Cell:
    return (
        begin_cell()
        .store_uint(InvoiceOpCodes.PAY_INVOICE, 32)
        .store_uint(0, 64)
        .end_cell()
    )


def build_pay_invoice_with_jettons_message(amount: int, invoice_address: str) -> Cell:
    return build_send_jettons_message(
        amount,
        invoice_address,
        invoice_address,
        to_nano("0.15", TonCurrencyEnum.ton),
        begin_cell().store_uint(0, 1).end_cell(),
        False
    )
