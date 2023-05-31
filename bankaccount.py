import json
import logging
from abc import ABC


logger = logging.getLogger("MyLogger")
logger.setLevel(level=logging.INFO)

file_handler = logging.FileHandler("accounts.log", mode="a")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
pattern = logging.Formatter("%(levelname)s - %(lineno)d - %(msg)s")
console_handler.setFormatter(pattern)
file_handler.setFormatter(pattern)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


class BankAccount(ABC):
    def __init__(self, owner_name: str, balance: int, password: str, cvv2: str, bank: str):
        """
        Initializes a BankAccount object.

        Args:
            owner_name : The owner's name.
            balance : The account balance.
            password : The account password.
            cvv2 : The account CVV2.
            bank : The bank name.
        """
        self.owner_name = owner_name
        self._balance = balance
        self._password = password
        self._cvv2 = cvv2
        self.bank = bank

    @property
    def balance(self) -> int:
        """Returns the account balance."""
        return self._balance

    @balance.setter
    def balance(self, balance: int):
        """
        Sets the account balance.

        Args:
            balance : The new account balance.

        Raises:
            ValueError: If the balance is less than 10,000.
        """
        if balance < 10_000:
            raise ValueError("Invalid balance")

        self._balance = balance

    def __repr__(self) -> str:
        """Returns a string representation of the BankAccount object."""
        dictionary = vars(self)
        dictionary["rial"] = self.to_rial(self._balance)
        return str(dictionary)

    def __str__(self) -> str:
        """Returns a string representation of the account details."""
        return f"{self.owner_name}: {self._balance:,}"

    def __add__(self, amount: int):
        """Adds the given amount to the account balance and returns the result."""
        return self._balance + amount

    def __sub__(self, amount: int):
        """Subtracts the given amount from the account balance and returns the result."""
        return self._balance - amount

    def verify_password(self, password: int) -> bool:
        """
        Verifies if the provided password matches the account password.

        Args:
            password : The password to verify.

        """
        return self._password == password

    def verify_cvv2(self, cvv2: int) -> bool:
        """
        Verifies if the provided CVV2 matches the account CVV2.

        Args:
            cvv2 : The CVV2 to verify.

        """
        return self._cvv2 == cvv2

    @staticmethod
    def to_rial(balance: int) -> int:
        """
        Converts the given balance from the account currency to Iranian Rial.

        Args:
            balance : The balance to convert.

        Returns:
            int: The converted balance in Iranian Rial.
        """
        return balance * 10


class PasargadAccount(BankAccount):
    __MINIMUM = 10_000
    __accounts = []

    def __init__(self, owner_name: str, balance: int, password: str, cvv2: str, bank: str):
        super().__init__(owner_name, balance, password, cvv2, bank)
        type(self).__accounts.append(self)

    def __add__(self, amount: int):
        if self._balance + amount < self.__MINIMUM:
            raise ValueError("Invalid balance")

        return super().__add__(amount)

    def __sub__(self, amount: int):
        if self._balance - amount < self.__MINIMUM:
            raise ValueError("Invalid balance")

        return super().__sub__(amount)

    def transfer(self, other: "BankAccount", amount: int, password: str, cvv2: str):
        if amount < 0:
            logger.error("Raised")
            raise ValueError("Invalid amount")

        if not self.verify_password(password):
            logger.error("Raised")
            raise ValueError("Invalid password")

        if not self.verify_cvv2(cvv2):
            logger.error("Raised")
            raise ValueError("Invalid cvv2")

        if self.balance < amount:
            logger.error("Raised")
            raise ValueError("Insufficient balance")

        self.balance = self.balance - amount
        other.balance = other.balance + amount
        logger.info("Successfully transferred")

        self.save()
        other.save()

    @classmethod
    def maximum(cls) -> int:
        """Returns the maximum balance among all PasargadAccount instances."""
        return max([account.balance for account in cls.__accounts])

    @classmethod
    def save(cls):
        """
        Saves the PasargadAccount instances to a JSON file.
        """
        data = [
            {
                "owner_name": account.owner_name,
                "balance": account.balance,
                "password": account._password,
                "cvv2": account._cvv2,
                "bank": account.bank
            }
            for account in cls.__accounts
        ]

        filename = "account_Pasargad.json"

        with open(filename, "w", encoding="utf_8") as file:
            json.dump(data, file, indent=4)

    @classmethod
    def load(cls):
        """
        Loads the PasargadAccount instances from the JSON file.
        """
        with open("account_Pasargad.json", "r", encoding="utf_8") as file:
            data = json.load(file)
            cls.__accounts = [
                cls(
                    owner_name=account_data["owner_name"],
                    balance=account_data["balance"],
                    password=account_data["password"],
                    cvv2=account_data["cvv2"],
                    bank=account_data["bank"]
                )
                for account_data in data
            ]


class ShahrBankAccount(BankAccount):
    __MINIMUM = 10_000
    __accounts = []

    def __init__(self, owner_name: str, balance: int, password: str, cvv2: str, bank: str):
        super().__init__(owner_name, balance, password, cvv2, bank)
        type(self).__accounts.append(self)

    def __add__(self, amount: int):
        if self._balance + amount < self.__MINIMUM:
            raise ValueError("Invalid balance")

        return super().__add__(amount)

    def __sub__(self, amount: int):
        if self._balance - amount < self.__MINIMUM:
            raise ValueError("Invalid balance")

        return super().__sub__(amount)

    def transfer(self, other: "BankAccount", amount: int, password: str, cvv2: str):
        if amount < 0:
            logger.error("Raised")
            raise ValueError("Invalid amount")

        if not self.verify_password(password):
            logger.error("Raised")
            raise ValueError("Invalid password")

        if not self.verify_cvv2(cvv2):
            logger.error("Raised")
            raise ValueError("Invalid cvv2")

        if self.balance < amount:
            logger.error("Raised")
            raise ValueError("Insufficient balance")

        self.balance = self.balance - amount
        other.balance = other.balance + amount
        logger.info("Successfully transferred")

        self.save()
        other.save()

    @classmethod
    def maximum(cls) -> int:
        """Returns the maximum balance among all ShahrBankAccount instances."""
        return max([account.balance for account in cls.__accounts])

    @classmethod
    def save(cls):
        """
        Saves the ShahrBankAccount instances to a JSON file.
        """
        data = [
            {
                "owner_name": account.owner_name,
                "balance": account.balance,
                "password": account._password,
                "cvv2": account._cvv2,
                "bank": account.bank
            }
            for account in cls.__accounts
        ]

        filename = "account_shahr.json"

        with open(filename, "w", encoding="utf_8") as file:
            json.dump(data, file, indent=4)

    @classmethod
    def load(cls):
        """
        Loads the ShahrBankAccount instances from the JSON file.
        """
        with open("account_shahr.json", "r", encoding="utf_8") as file:
            data = json.load(file)
            cls.__accounts = [
                cls(
                    owner_name=account_data["owner_name"],
                    balance=account_data["balance"],
                    password=account_data["password"],
                    cvv2=account_data["cvv2"],
                    bank=account_data["bank"]
                )
                for account_data in data
            ]
