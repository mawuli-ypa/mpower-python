import unittest
import mpower
from . import MP_ACCESS_TOKENS

mpower.debug = True
mpower.api_keys = MP_ACCESS_TOKENS


class TestGeneral(unittest.TestCase):
    """General/Miscellaneous tests"""
    def setUp(self):
        # Your MPower developer tokens
        self.store = mpower.Store(name="FooBar store")
        self.opr_data = {'total_amount': 345,
                         'description': "Hello World",
                         "account_alias": "0266636984"}
        self.opr = mpower.OPR(self.opr_data, self.store)

    def tearDown(self):
        self.opr = None
        self.store = None
        self.opr_data = None

    def test_rsc_endpoints(self):
        endpoint = 'checkout-invoice/confirm/test_98567JGF'
        url = self.opr.get_rsc_endpoint(endpoint)
        self.assertTrue(url.startswith('https') and url.endswith(endpoint))

    def test_add_headers(self):
        header = {'Foo': 'Bar'}
        self.opr.add_header(header)
        self.assertTrue("Foo" in self.opr.headers.keys())
        self.assertFalse('FooBar' in self.opr.headers.keys())


if __name__ == '__main__':
    unittest.main()
