import unittest
import mpower
from . import MP_ACCESS_TOKENS

mpower.debug = True
mpower.api_keys = MP_ACCESS_TOKENS


class Invoice(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.store = mpower.Store(name="FooBar Shop")
        self.items = [
            mpower.InvoiceItem(
                name="VIP Ticket",
                quantity=2,
                unit_price="35.0",
                total_price="70.0",
                description="VIP Tickets for the MPower Event"
            )
        ]
        self.invoice = mpower.Invoice(self.store)
        self.invoice.add_items(self.items * 10)
        # taxes are (key,value) pairs
        self.invoice.add_taxes([("NHIS TAX", 23.8), ("VAT", 5)])
        self.invoice.add_custom_data([("phone_brand", "Motorola V3"),
                                      ("model", "65456AH23")])

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.invoice = None

    def test_create_invoice(self):
        status, _ = self.invoice.create()
        self.assertTrue(status)

    def test_add_items(self):
        _items = len(self.invoice.items)
        self.invoice.add_items(self.items * 2)
        self.assertTrue(len(self.invoice.items) > _items)

    def test_add_taxes(self):
        _taxes = len(self.invoice.taxes)
        self.invoice.add_taxes([("Foo_TAX", 9)])
        self.assertTrue(len(self.invoice.taxes) > _taxes)

    def test_add_custom_data(self):
        _data = len(self.invoice.custom_data)
        self.invoice.add_custom_data([("Category", "Sports")])
        self.assertTrue(len(self.invoice.custom_data) > _data)
