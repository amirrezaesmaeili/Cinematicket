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


    def can_watch_movie(self, movie_age_rating: int) -> bool:
        """
        Check if the user can watch a movie based on its age rating.
        """
        return self.age_rating >= movie_age_rating
    
    def discount_apply(self, original_price: float) -> float:
        """
        Apply a discount to the original price based on the user's membership months or birthday.
        """
        if self.is_birthday():
            # Calculate birthday discount (50%)
            discount_percentage = 0.5
        elif self.membership_months > 0:
            # Calculate membership discount (5% per month)
            discount_percentage = self.membership_months * 0.05
        else:
            # No discount available
            discount_percentage = 0

        discount_amount = original_price * discount_percentage
        final_price = original_price - discount_amount
        return final_price

class UserEncoder(json.JSONEncoder):
    def default(self, o):
        """
        Convert User and datetime.date objects to JSON serializable format.
        """
        if isinstance(o, User):
            return o.__dict__
        if isinstance(o, datetime.date):
            return o.isoformat()
        return super().default(o)
    
    # Example usage of the User class:
user1 = User("John", datetime.date(1990, 5, 29), 8, 32)
user2 = User("Jane", datetime.date(1995, 7, 12), 12, 27)
user3 = User("Mike", datetime.date(1988, 9, 3), 6, 34)
user4= User("Jacksone",datetime.date(2000,5,26),2,23)

users = [user1, user2, user3,user4]

# Clear the console screen
os.system('cls')



    



