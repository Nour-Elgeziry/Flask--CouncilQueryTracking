import unittest
from taxes import Taxes


class TestTaxes(unittest.TestCase):
    def setUp(self):
        print("setUp")
        self.__taxes = Taxes()
        self.totalTaxes = 1000
        self.governmentPercentage = 20

    def test_get_total_tax(self):
        result = self.__taxes.getTotalTax()
        self.assertEqual(result, 200)


def tearDown(self):
    print("tearDown")
    del self.__taxes

if __name__ == '__main__':
    unittest.main()
