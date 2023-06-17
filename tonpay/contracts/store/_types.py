from typing import Optional

from tonsdk.boc import Cell

from ...currency import Currency


class StoreConfig:
    def __init__(self,
                 owner: str,
                 name: str,
                 description: str,
                 image: str,
                 webhook: str,
                 mcc_code: int,
                 active: bool,
                 invoice_code: Cell
                 ):
        self.owner = owner
        self.name = name
        self.description = description
        self.image = image
        self.webhook = webhook
        self.mcc_code = mcc_code
        self.active = active
        self.invoice_code = invoice_code


class StoreData:
    def __init__(self,
                 owner: str,
                 name: str,
                 description: str,
                 image: str,
                 webhook: str,
                 mcc_code: int,
                 active: bool,
                 invoice_code: Cell,
                 version: int
                 ):
        self.owner = owner
        self.name = name
        self.description = description
        self.image = image
        self.webhook = webhook
        self.mcc_code = mcc_code
        self.active = active
        self.invoice_code = invoice_code
        self.version = version


class InvoiceInfo:
    def __init__(self,
                 has_customer: bool,
                 customer: str,
                 invoice_id: str,
                 metadata: str,
                 amount: int,
                 currency: Currency
                 ):
        self.has_customer = has_customer
        self.customer = customer
        self.invoice_id = invoice_id
        self.metadata = metadata
        self.amount = amount
        self.currency = currency


class PurchaseRequestInvoice:
    def __init__(self, invoice_id: str, metadata: str, amount: int, currency: Currency, customer: Optional[str] = None):
        self.invoice_id = invoice_id
        self.metadata = metadata
        self.amount = amount
        self.currency = currency
        self.customer = customer
