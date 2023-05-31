from bankaccount import ShahrBankAccount,PasargadAccount,BankAccount

import unittest

class BankAccountTest(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("hossein", 50000, "1234", "1234", "Bank")

    def test_balance(self):
        self.assertEqual(self.account.balance, 50000)

    def test_add(self):
        result = self.account + 10000
        self.assertEqual(result, 60000)

    def test_subtract(self):
        result = self.account - 10000
        self.assertEqual(result, 40000)

    def test_verify_password(self):
        result = self.account.verify_password("1234")
        self.assertTrue(result)

    def test_verify_cvv2(self):
        result = self.account.verify_cvv2("1234")
        self.assertTrue(result)

    def test_to_rial(self):
        result = self.account.to_rial(50000)
        self.assertEqual(result, 500000)

    def tearDown(self):
        self.account = None


class PasargadAccountTest(unittest.TestCase):
    def setUp(self):
        self.account1 = PasargadAccount("hossein", 50000, "1234", "1234", "Pasargad")
        self.account2 = PasargadAccount("zahra", 70000, "5678", "5678", "Pasargad")

    def test_transfer(self):
        self.account1.transfer(self.account2, 20000, "1234", "1234")
        self.assertEqual(self.account1.balance, 30000)
        self.assertEqual(self.account2.balance, 90000)

    def test_maximum(self):
        maximum_balance = PasargadAccount.maximum()
        self.assertEqual(maximum_balance, 70000)

    def tearDown(self):
        self.account1 = None
        self.account2 = None


class ShahrBankAccountTest(unittest.TestCase):
    def setUp(self):
        self.account1 = ShahrBankAccount("hossein", 50000, "1234", "1234", "Shahr Bank")
        self.account2 = ShahrBankAccount("zahra", 70000, "5678", "5678", "Shahr Bank")

    def test_transfer(self):
        self.account1.transfer(self.account2, 20000, "1234", "1234")
        self.assertEqual(self.account1.balance, 30000)
        self.assertEqual(self.account2.balance, 90000)

    def test_maximum(self):
        maximum_balance = ShahrBankAccount.maximum()
        self.assertEqual(maximum_balance, 70000)

    def tearDown(self):
        self.account1 = None
        self.account2 = None


if __name__ == "__main__":
    unittest.main()
