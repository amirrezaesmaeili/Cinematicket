import os
import datetime
import pickle
import json

class MyException(Exception):
    pass

class User:
    def __init__(self, name: str, birthdate: datetime.date, membership_months: int, age_rating: int):
        """
        Initialize a User object with the provided attributes.
        """
        self.name = name
        self.birthdate = birthdate
        self.membership_months = membership_months
        self.age_rating = age_rating

