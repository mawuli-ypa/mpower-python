import unittest
import mpower
from . import MP_ACCESS_TOKENS

mpower.debug = True
mpower.api_keys = MP_ACCESS_TOKENS


class TestDirectCard(unittest.TestCase):
    def test_directcard(self):
        card_info = {
            "card_name": "Alfred Robert Rowe",
            "card_number": "4242424242424242",
            "card_cvc": "123",
            "exp_month": "06",
            "exp_year": "2010",
            "amount": "300"
        }
        direct_card = mpower.DirectCard(card_info)
        # this request should fail since the card_info data is invalid
        status, response = direct_card.process()
        self.assertFalse(status)

    def test_directpay(self):
        account_alias = "0266636984"
        amount = 30.50
        # toggle debug switch to True
        direct_pay = mpower.DirectPay(account_alias, amount)
        status, response = direct_pay.process()
        # DirectPay works in sandbox/debug mode
        self.assertTrue(status)
