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


    def is_birthday(self) -> bool:
        """
        Check if it's the user's birthday today.
        """
        today = datetime.date.today()
        return today.month == self.birthdate.month and today.day == self.birthdate.day
    
    def can_get_discount(self) -> bool:
        """
        Check if the user is eligible for a discount.
        """
        return self.is_birthday() or self.membership_months > 0
    

    def can_reserve_session(self, session_time: datetime.datetime, theater_capacity: int = None) -> bool:
        """
        Check if the user can reserve a session.
        """
        if session_time < datetime.datetime.now():
            raise MyException("Session time has passed.")
        if theater_capacity is not None and theater_capacity <= 0:
            raise MyException("Theater capacity is full.")
        return True



