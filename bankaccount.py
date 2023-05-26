import json
import logging
from argparse import ArgumentParser
from abc import ABC
from hashlib import sha256


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
    def __init__(self, owner_name: str, balance: int, password: str, cvv2: str):
        self.owner_name = owner_name
        self._balance = balance
        self._password_hash = self._hash_password(password)
        self._cvv2 = cvv2

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, balance: int):
        if balance < 10_000:
            raise ValueError("Invalid balance")

        self._balance = balance

    def __repr__(self) -> str:
        dictionary = vars(self)
        dictionary["rial"] = self.to_rial(self._balance)
        return str(dictionary)

    def __str__(self) -> str:
        return f"{self.owner_name}: {self._balance:,}"

    def __add__(self, amount: int):
        return self._balance + amount

    def __sub__(self, amount: int):
        return self._balance - amount

    def _hash_password(self, password: str) -> str:
        return sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        hashed_password = self._hash_password(password)
        return self._password_hash == hashed_password

    def verify_cvv2(self, cvv2: str) -> bool:
        return self._cvv2 == cvv2

    @staticmethod
    def to_rial(balance):
        return balance * 10


class ShahrBankAccount(BankAccount):
    __MINIMUM = 10_000
    __accounts = []

    def __init__(self, owner_name: str, balance: int, password: str, cvv2: str):
        super().__init__(owner_name, balance, password, cvv2)
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

        self.balance -= (amount - 600)
        other.balance += amount
        logger.info("successfully transferred")

    @classmethod
    def maximum(cls) -> int:
        return max([account.balance for account in cls.__accounts])

    @classmethod
    def save(cls):
        data = [
            {
                "owner_name": account.owner_name,
                "balance": account.balance,
                "password": account._password_hash,
                "cvv2": account._cvv2,
            }
            for account in cls.__accounts
        ]
        with open("account.json", "w", encoding="utf_8") as file:
            json.dump(data, file , indent=4)

    @classmethod
    def load(cls):
        with open("account.json", "r", encoding="utf_8") as file:
            data = json.load(file)
            cls.__accounts = [
                cls(
                    owner_name=account_data["owner_name"],
                    balance=account_data["balance"],
                    password=account_data["password"],
                    cvv2=account_data["cvv2"],
                )
                for account_data in data
            ]

