from enum import IntEnum


class InvoiceOpCodes(IntEnum):
    EDIT_INVOICE = 0x48c504f3
    DEACTIVATE_INVOICE = 0x1cc0b11e
    ACTIVATE_INVOICE = 0xc285952f
    PAY_INVOICE = 0xf53a02d3
