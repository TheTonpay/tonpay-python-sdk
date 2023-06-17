import base64

from tonsdk.boc import Cell

from ._types import StoreData
from ...utils import cell_to_string

STORE_CODE = "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"
STORE_VERSION = 12


def map_data_latest(stack: list):
    return StoreData(
        Cell.one_from_boc(base64.b64decode(stack[0][1]["bytes"]))
        .begin_parse().read_msg_addr().to_string(True, True, True),
        cell_to_string(Cell.one_from_boc(base64.b64decode(stack[1][1]["bytes"])))[4:],
        cell_to_string(Cell.one_from_boc(base64.b64decode(stack[2][1]["bytes"])))[4:],
        cell_to_string(Cell.one_from_boc(base64.b64decode(stack[3][1]["bytes"])))[4:],
        cell_to_string(Cell.one_from_boc(base64.b64decode(stack[4][1]["bytes"])))[4:],
        int(stack[5][1], 16),
        int(stack[6][1], 16) == -1,
        Cell.one_from_boc(base64.b64decode(stack[7][1]["bytes"])),
        int(stack[8][1], 16),
    )


def map_data_v7(stack: list):
    return StoreData(
        Cell.one_from_boc(base64.b64decode(stack[0][1]["bytes"]))
        .begin_parse().read_msg_addr().to_string(True, True, True),
        cell_to_string(Cell.one_from_boc(base64.b64decode(stack[1][1]["bytes"])))[4:],
        cell_to_string(Cell.one_from_boc(base64.b64decode(stack[2][1]["bytes"])))[4:],
        cell_to_string(Cell.one_from_boc(base64.b64decode(stack[3][1]["bytes"])))[4:],
        "",
        int(stack[5][1], 16),
        int(stack[6][1], 16) == -1,
        Cell.one_from_boc(base64.b64decode(stack[7][1]["bytes"])),
        int(stack[8][1], 16),
    )


SUPPORTED_VERSIONS = [
    {
        'version': STORE_VERSION,
        'map_data': map_data_latest
    },
    {
        'version': 7,
        'map_data': map_data_v7
    }
]
