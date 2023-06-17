from tonpay.constants import ZERO_ADDRESS

BRIDGE_WALLET = "te6cckECEwEAA4UAART/APSkE/S88sgLAQIBYgIDAgLLBAUAG6D2BdqJofQB9IH0gamjAgHOBgcCAVgKCwL3CDHAJJfBOAB0NMDAXGwlRNfA/Ad4PpA+kAx+gAxcdch+gAx+gAwc6m0AALTHwHbPFsyNDQ0JIIQD4p+pbqaMGwiNl4xECPwGuAkghAXjUUZupswbCJeMhAkQwDwG+A3WzaCEFlfB7y6nwJxsPLSwFAjuvLixgHwHOBfBYAgJABE+kQwwADy4U2AAXIBP+DMgbpUwgLH4M94gbvLSmtDTBzHT/9P/9ATTB9Qw0PoA+gD6APoA+gD6ADAACIQP8vACAVgMDQIBSBESAfcBdM/AQH6APpAIfAB7UTQ+gD6QPpA1NFRNqFSLMcF8uLBKsL/8uLCVDRCcFQgE1QUA8hQBPoCWM8WAc8WzMkiyMsBEvQA9ADLAMkgcAH5AHTIywISygfL/8nQBPpA9AQx+gAg10nCAPLixMiAGAHLBVAHzxZw+gJ3ActrgDgLzO1E0PoA+kD6QNTRCtM/AQH6AFFRoAX6QPpAU13HBVRzb3BUIBNUFAPIUAT6AljPFgHPFszJIsjLARL0APQAywDJcAH5AHTIywISygfL/8nQUA/HBR6x8uLDDPoAUcqhKbYIGaFQB6AYoSaSbFXjDSXXCwHDACHCALCAPEACqE8zIghAXjUUZWAoCyx/LP1AH+gIizxZQBs8WJfoCUAPPFslQBcwjkXKRceJQB6gToAiqAFAEoBegFLzy4sUByYBA+wBDAMhQBPoCWM8WAc8WzMntVAByUmmgGKHIghBzYtCcKQLLH8s/UAf6AlAEzxZQB88WyciAEAHLBSfPFlAE+gJxActqE8zJcfsAUEITAHSOI8iAEAHLBVAGzxZQBfoCcAHLaoIQ1TJ221gFAssfyz/JcvsAklsz4kADyFAE+gJYzxYBzxbMye1UAOs7UTQ+gD6QPpA1NEF0z8BAfoAIcIA8uLC+kD0BAHQ05/RAdFRYqFSWMcF8uLBJsL/8uLCyIIQe92X3lgEAssfyz8B+gIjzxYBzxYTy5/JyIAYAcsFI88WcPoCcQHLaszJgED7AEATyFAE+gJYzxYBzxbMye1UgAIcgCDXIe1E0PoA+kD6QNTRBNMfAYQPIYIQF41FGboCghB73ZfeuhKx8vTTPwEw+gAwE6BQI8hQBPoCWM8WAc8WzMntVINjFu1o=";

BOLT_WALLET = "te6cckECEQEAAxcAART/APSkE/S88sgLAQIBYgIDAgLMBAUAG6D2BdqJofQB9IH0gahhAgEgBgcCASAICQC30QY4B5IADoaYGAuNhKia+B+AZwfSB9IBj9ABi465D9ABj9ABgBaY/BCAfFP1KpEF1KmJos+ATwQQgLxqKMqRBdSxiZoBn4BXAawQgsr4PeXUms+AXwL4JCB/l4QAEWvpEMHC68uFNgIBIAoLAIPUAQa5D2omh9AH0gfSBqGAJpj8EIC8aijKkQXUEIPe7L7wndCVj5cWLpn5j9ABgJ0CgR5CgCfQEsZ4sA54tmZPaqQB9VA9M/+gD6QCHwBu1E0PoA+kD6QNQwUTahUirHBfLiwSjC//LiwlQ0QnBUIBNUFAPIUAT6AljPFgHPFszJIsjLARL0APQAywDJIPkAcHTIywLKB8v/ydAE+kD0BDH6AHeAGMjLBVAIzxZw+gIXy2sTzIIQF41FGcjLHxmAwCASANDgCOyz9QB/oCIs8WUAbPFiX6AlADzxbJUAXMB6oAE6CCCJiWgKoAggiYloCgoBS88uLFBMmAQPsAECPIUAT6AljPFgHPFszJ7VQC8TtRND6APpA+kDUMAfTP/oAUVGgBfpA+kBTWscFVHNscFQgE1QUA8hQBPoCWM8WAc8WzMkiyMsBEvQA9ADLAMn5AHB0yMsCygfL/8nQUAzHBRux8uLDCfoAggiYloCCCJiWgKAaoSGVEEk4XwTjDSXXCwHDACTCALCAPEADbO1E0PoA+kD6QNQwB9M/+gD6QDBRUaFSSccF8uLBJ8L/8uLCggiYloCqABagFrzy4sOCEHvdl97Iyx8Vyz9QA/oCIs8WAc8WyXGAEMjLBSTPFnD6AstqzMmAQPsAQBPIUAT6AljPFgHPFszJ7VSAAbFIZoBihghBzYtCcyMsfUkDLP1AD+gIBzxZQB88WyXGAGMjLBSXPFlAH+gIWy2oVzMlx+wAQNACCjiqCCJiWgHL7AoIQ1TJ223CAEMjLBVAIzxZQBfoCFstqE8sfE8s/yXL7AFiSbDPiVQLIUAT6AljPFgHPFszJ7VSoVpbw";

DEFAULT_WALLET = "te6cckECEQEAAyMAART/APSkE/S88sgLAQIBYgIDAgLMBAUAG6D2BdqJofQB9IH0gahhAgHUBgcCASAICQDDCDHAJJfBOAB0NMDAXGwlRNfA/AM4PpA+kAx+gAxcdch+gAx+gAwc6m0AALTH4IQD4p+pVIgupUxNFnwCeCCEBeNRRlSILqWMUREA/AK4DWCEFlfB7y6k1nwC+BfBIQP8vCAAET6RDBwuvLhTYAIBIAoLAIPUAQa5D2omh9AH0gfSBqGAJpj8EIC8aijKkQXUEIPe7L7wndCVj5cWLpn5j9ABgJ0CgR5CgCfQEsZ4sA54tmZPaqQB8VA9M/+gD6QCHwAe1E0PoA+kD6QNQwUTahUirHBfLiwSjC//LiwlQ0QnBUIBNUFAPIUAT6AljPFgHPFszJIsjLARL0APQAywDJIPkAcHTIywLKB8v/ydAE+kD0BDH6ACDXScIA8uLEd4AYyMsFUAjPFnD6AhfLaxPMgMAgEgDQ4AnoIQF41FGcjLHxnLP1AH+gIizxZQBs8WJfoCUAPPFslQBcwjkXKRceJQCKgToIIJycOAoBS88uLFBMmAQPsAECPIUAT6AljPFgHPFszJ7VQC9ztRND6APpA+kDUMAjTP/oAUVGgBfpA+kBTW8cFVHNtcFQgE1QUA8hQBPoCWM8WAc8WzMkiyMsBEvQA9ADLAMn5AHB0yMsCygfL/8nQUA3HBRyx8uLDCvoAUaihggiYloBmtgihggiYloCgGKEnlxBJEDg3XwTjDSXXCwGAPEADXO1E0PoA+kD6QNQwB9M/+gD6QDBRUaFSSccF8uLBJ8L/8uLCBYIJMS0AoBa88uLDghB73ZfeyMsfFcs/UAP6AiLPFgHPFslxgBjIywUkzxZw+gLLaszJgED7AEATyFAE+gJYzxYBzxbMye1UgAHBSeaAYoYIQc2LQnMjLH1Iwyz9Y+gJQB88WUAfPFslxgBDIywUkzxZQBvoCFctqFMzJcfsAECQQIwB8wwAjwgCwjiGCENUydttwgBDIywVQCM8WUAT6AhbLahLLHxLLP8ly+wCTNWwh4gPIUAT6AljPFgHPFszJ7VSV6u3X";


class Currency:
    def __init__(self,
                 name: str,
                 description: str,
                 symbol: str,
                 decimals: int,
                 address: str,
                 image: str,
                 wallet_code: str,
                 verified: bool,
                 testnet: bool = False
                 ):
        self.name = name
        self.description = description
        self.symbol = symbol
        self.decimals = decimals
        self.address = address
        self.image = image
        self.verified = verified
        self.wallet_code = wallet_code
        self.testnet = testnet


class Currencies:
    TON = Currency(
        "Toncoin",
        "Native Toncoin",
        "TON",
        9,
        ZERO_ADDRESS,
        "https://avatars.githubusercontent.com/u/55018343?s=256",
        "te6cckEBAQEAAgAAAEysuc0=",  # empty cell base64
        True
    )
    jUSDT = Currency(
        "jUSDT",
        "USDT transferred from Ethereum via bridge.ton.org.",
        "jUSDT",
        6,
        "EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA",
        "https://bridge.ton.org/token/1/0xdac17f958d2ee523a2206206994597c13d831ec7.png",
        BRIDGE_WALLET,
        True,
    )
    jUSDC = Currency(
        "jUSDC",
        "USDC transferred from Ethereum via bridge.ton.org.",
        "jUSDC",
        6,
        "EQB-MPwrd1G6WKNkLz_VnV6WqBDd142KMQv-g1O-8QUA3728",
        "https://bridge.ton.org/token/1/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.png",
        BRIDGE_WALLET,
        True,
    )
    oUSDT = Currency(
        "Orbit Bridge Ton USD Tether",
        "Orbit Bridge Token on TON blockchain!",
        "oUSDT",
        6,
        "EQC_1YoM8RBixN95lz7odcF3Vrkc_N8Ne7gQi7Abtlet_Efi",
        "https://raw.githubusercontent.com/orbit-chain/bridge-token-image/main/ton/usdt.png",
        DEFAULT_WALLET,
        True,
    )
    oUSDC = Currency(
        "Orbit Bridge Ton USD Coin",
        "Orbit Bridge Token on TON blockchain!",
        "oUSDC",
        6,
        "EQC61IQRl0_la95t27xhIpjxZt32vl1QQVF2UgTNuvD18W-4",
        "https://raw.githubusercontent.com/orbit-chain/bridge-token-image/main/ton/usdt.png",
        DEFAULT_WALLET,
        True,
    )
    jWBTC = Currency(
        "jWBTC",
        "WBTC transferred from Ethereum via bridge.ton.org.",
        "jWBTC",
        8,
        "EQDcBkGHmC4pTf34x3Gm05XvepO5w60DNxZ-XT4I6-UGG5L5",
        "https://bridge.ton.org/token/1/0x2260fac5e5542a773aa44fbcfedf7c193bc2c599.png",
        BRIDGE_WALLET,
        True,
    )
    jDAI = Currency(
        "jDAI",
        "DAI transferred from Ethereum via bridge.ton.org.",
        "jDAI",
        18,
        "EQDo_ZJyQ_YqBzBwbVpMmhbhIddKtRP99HugZJ14aFscxi7B",
        "https://bridge.ton.org/token/1/0x6b175474e89094c44da98b954eedeac495271d0f.png",
        BRIDGE_WALLET,
        True,
    )
    oWBTC = Currency(
        "Orbit Bridge Ton Wrapped BTC",
        "Orbit Bridge Token on TON blockchain!",
        "oWBTC",
        8,
        "EQANasbzD5wdVx0qikebkchrH64zNgsB38oC9PVu7rG16qNB",
        "https://raw.githubusercontent.com/orbit-chain/bridge-token-image/main/ton/wbtc.png",
        DEFAULT_WALLET,
        True,
    )
    oETH = Currency(
        "Orbit Bridge Ton Ethereum",
        "Orbit Bridge Token on TON blockchain!",
        "oETH",
        18,
        "EQAW42HutyDem98Be1f27PoXobghh81umTQ-cGgaKVmRLS7-",
        "https://raw.githubusercontent.com/orbit-chain/bridge-token-image/main/ton/eth.png",
        DEFAULT_WALLET,
        True,
    )
    oDAI = Currency(
        "Orbit Bridge Ton Dai",
        "Orbit Bridge Token on TON blockchain!",
        "oDAI",
        18,
        "EQAAXwH0cajPsMF-nNC5kz-SaLaeaDr4M7Q1foVwP_vOW1tR",
        "https://raw.githubusercontent.com/orbit-chain/bridge-token-image/main/ton/dai.png",
        DEFAULT_WALLET,
        True,
    )
    BOLT = Currency(
        "Huebel Bolt",
        "Official token of the Huebel Company",
        "BOLT",
        9,
        "EQD0vdSA_NedR9uvbgN9EikRX-suesDxGeFg69XQMavfLqIw",
        "https://cloudflare-ipfs.com/ipfs/QmX47dodUg1acXoxYDULWTNfShXRW5uHrCmoKSUNR9xKQw",
        BOLT_WALLET,
        True,
    )
    SCALE = Currency(
        "Scaleton",
        "SCALE is a utility token that will be used to support all independent developers.",
        "SCALE",
        9,
        "EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE",
        "https://cloudflare-ipfs.com/ipfs/QmSMiXsZYMefwrTQ3P6HnDQaCpecS4EWLpgKK5EX1G8iA8",
        DEFAULT_WALLET,
        True,
    )
    KINGY = Currency(
        "Jetton kingy",
        "Jetton for the kingy community, united by the common idea of developing the TON ecosystem.",
        "KINGY",
        9,
        "EQC-tdRjjoYMz3MXKW4pj95bNZgvRyWwZ23Jix3ph7guvHxJ",
        "https://i.ibb.co/FbTCKRP/logotokenkingy.png",
        DEFAULT_WALLET,
        True,
    )
    PAY = Currency(
        "Tonpay test token",
        "Test token for jetton integration into @TheTonpay",
        "PAY",
        9,
        "EQAWROADS1e8nOgXmSjlSZS35kC5aWTvj8ukCj4ojrQqrr_a",
        "https://avatars.githubusercontent.com/u/122553410?s=256",
        DEFAULT_WALLET,
        True,
        True,
    )


def get_currency_by_address(address: str) -> Currency:
    currency = Currencies.TON

    for key in Currencies.__dict__:
        if isinstance(Currencies.__dict__[key], Currency):
            if Currencies.__dict__[key].address == address:
                currency = Currencies.__dict__[key]
                break

    return currency
