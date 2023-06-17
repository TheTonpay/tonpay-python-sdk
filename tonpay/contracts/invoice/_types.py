from tonsdk.boc import Cell


class InvoiceConfig:
    def __init__(self,
                 store: str,
                 merchant: str,
                 beneficiary: str,
                 has_customer: bool,
                 customer: str,
                 invoice_id: str,
                 metadata: str,
                 amount: int,
                 paid: bool,
                 active: bool,
                 accepts_jetton: bool,
                 jetton_master_address: str,
                 jetton_wallet_code: Cell):
        self.store = store
        self.merchant = merchant
        self.beneficiary = beneficiary
        self.has_customer = has_customer
        self.customer = customer
        self.invoice_id = invoice_id
        self.metadata = metadata
        self.amount = amount
        self.paid = paid
        self.active = active
        self.accepts_jetton = accepts_jetton
        self.jetton_master_address = jetton_master_address
        self.jetton_wallet_code = jetton_wallet_code


class InvoiceData:
    def __init__(self,
                 store: str,
                 merchant: str,
                 beneficiary: str,
                 has_customer: bool,
                 customer: str,
                 invoice_id: str,
                 metadata: str,
                 amount: int,
                 paid: bool,
                 active: bool,
                 accepts_jetton: bool,
                 jetton_master_address: str,
                 jetton_wallet_code: Cell,
                 version: int):
        self.store = store
        self.merchant = merchant
        self.beneficiary = beneficiary
        self.has_customer = has_customer
        self.customer = customer
        self.invoice_id = invoice_id
        self.metadata = metadata
        self.amount = amount
        self.paid = paid
        self.active = active
        self.accepts_jetton = accepts_jetton
        self.jetton_master_address = jetton_master_address
        self.jetton_wallet_code = jetton_wallet_code
        self.version = version
