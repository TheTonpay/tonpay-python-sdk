from enum import IntEnum


class StoreOpCodes(IntEnum):
    ISSUE_INVOICE = 0x4b4e70b0
    REQUEST_PURCHASE = 0x36b795b5
    EDIT_STORE = 0xa0b2b61d
    DELETE_STORE = 0xfb4aca1a
    DEACTIVATE_STORE = 0xf9bf9637
    ACTIVATE_STORE = 0x97500daf
    UPGRADE_CODE_FULL = 0xb43bbb52
    UPGRADE_CODE_STORE = 0xacb08f28
    UPGRADE_CODE_INVOICE = 0xb5f1424f