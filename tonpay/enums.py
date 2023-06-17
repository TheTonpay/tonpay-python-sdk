from enum import StrEnum


class TonNetwork(StrEnum):
    MAINNET = "mainnet"
    TESTNET = "testnet"


class DeeplinkFormat(StrEnum):
    TON = "ton"
    TONKEEPER = "tonkeeper"
