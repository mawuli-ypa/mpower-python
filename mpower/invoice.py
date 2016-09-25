"""MPower Payments Invoice"""
from collections import namedtuple
from . import Payment


InvoiceItem = namedtuple(
    'InvoiceItem', 'name quantity unit_price total_price description')


class Invoice(Payment):
    """Payment invoice"""

    def __init__(self, store=None):
        """Create an invoice

        Accepts list of store object as initial parameter and
        a dictionary of tokens for accessing the MPower Payments API
        """
        self.cancel_url = None
        self.return_url = None
        self.description = None
        self.items = {}
        self.total_amount = 0
        self.custom_data = {}
        self.taxes = {}
        super(Invoice, self).__init__()
        if store:
            self.store = store

    def create(self, items=None, taxes=None, custom_data=None):
        """Adds the items to the invoice

        Format of 'items':
        [
         InvoiceItem(
             name="VIP Ticket",
             quantity= 2,
             unit_price= "35.0",
             total_price= "70.0",
             description= "VIP Tickets for the MPower Event"
          }
        ,...
        ]
        """
        self.add_items(items or [])
        self.add_taxes(taxes or [])
        self.add_custom_data(custom_data or [])
        return self._process('checkout-invoice/create', self._prepare_data)

    def confirm(self, token=None):
        """Returns the status of the invoice

        STATUSES: pending, completed, cancelled
        """
        _token = token if token else self._response.get("token")
        return self._process('checkout-invoice/confirm/' + str(_token))

    def add_taxes(self, taxes):
        """Appends the data to the 'taxes' key in the request object

        'taxes' should be in format: [("tax_name", "tax_amount")]
        For example:
        [("NHIs TAX", 23.8), ("VAT", 5)]
        """
        # fixme: how to resolve duplicate tax names
        _idx = len(self.taxes)  # current index to prevent overwriting
        for idx, tax in enumerate(taxes):
            tax_key = "tax_" + str(idx + _idx)
            self.taxes[tax_key] = {"name": tax[0], "amount": tax[1]}

    def add_custom_data(self, data=None):
        """Adds the data to teh custom data sent to the server

        data format: [("phone_brand", Motorola V3"), ("model", "65456AH23")]
        """
        self.custom_data.update(dict(data or []))

    def add_item(self, item):
        """Updates the list of items in the current transaction"""
        _idx = len(self.items)
        self.items.update({"item_" + str(_idx + 1): item})

    def add_items(self, items):
        for item in items:
            self.add_item(item)

    @property
    def _prepare_data(self):
        """Formats the data in the current transaction for processing"""
        total_amount = self.total_amount or self.calculate_total_amt()
        self._data = {
            "invoice": {
                "items": self.__encode_items(self.items),
                "taxes": self.taxes,
                "total_amount": total_amount,
                "description": self.description,
            },
            "store": self.store.info,
            "custom_data": self.custom_data,
            "actions": {
                "cancel_url": self.cancel_url,
                "return_url": self.return_url
            }
        }
        return self._data

    def calculate_total_amt(self, items=None):
        """Returns the total amount/cost of items in the current invoice"""
        _items = (items or self.items).items()
        return sum(float(x[1].total_price) for x in _items)

    def __encode_items(self, items):
        """Encodes the InvoiceItems into a JSON serializable format

        items = [('item_1',InvoiceItem(name='VIP Ticket', quantity=2,
                             unit_price='35.0', total_price='70.0',
                             description='VIP Tickets for party')),...]
        """
        xs = [item._asdict() for (_key, item) in items.items()]
        return list(map(lambda x: dict(zip(x.keys(), x.values())), xs))
