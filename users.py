from uuid import uuid4
import hashlib
import json
from enum import Enum
import os
import platform
import datetime as dt
from argparse import Namespace

class UserRole(Enum):
    MANAGER = "manager"
    ADMIN = "admin"
    USER = "user"

class User:
    _users = {}

    def __init__(self, username: str, password: str, birth: str, id: str, submit_date: str, telephone_number= None,role=UserRole.USER) -> None:
        """
        Initialize a User object.

        Args:
            username : The username for the user.
            password : The password for the user.
            telephone_number: telephone number for the user. Defaults to None.
        """
        self.username = username
        self._password = password
        self.birth = birth
        self.submit_date = submit_date
        self.telephone_number = telephone_number
        self.id = id
        self.role = role

    def __str__(self) -> str:
        """
        Return a string representation of the User object.
        """
        return f"ID: {self.id}\nUsername: {self.username}\nTelephone Number: {self.telephone_number}\
            Birthday: {self.birth}\nSubmit_date: {self.submit_date}"

    def age_counter(self) -> int:
        """
        calculate and return user age.
        """
        today = dt.datetime.today()
        user_birth = dt.datetime.strptime(self.birth, '%Y-%m-%d')
        user_age = (today - user_birth).days // 365
        return user_age

    def calculate_membership(self) -> int:
        """
        calculate and return user membership time.
        """
        today = dt.date.today()
        membership = (today - self.submit_date).days // 30
        return membership

    @classmethod
    def sign_up(cls, username: str, password: str, role: str, birth: str, telephone_number=None):
        cls.load_from_database()
        if username in cls._users:
            raise ValueError("This username already exists.")
        else:
            validate = cls.validate_password(password)
            if validate:
                if role == "USER":
                    if birth:
                        cls.create_user(username, password, birth, telephone_number,role=UserRole.USER)
                        return "Creating User"
                    else:
                        raise ValueError("Birthday field is required!")
                elif role == "ADMIN":
                    cls.create_admin(username, password,role=UserRole.ADMIN)
                    return "Creating Admin"
                elif role == "MANAGER":
                    cls.create_manager(username, password, role=UserRole.MANAGER)
                    return "Creating Manager"
            else:
                raise ValueError("Password must be at least 4 characters long.")

    @staticmethod
    def build_pass(password: str) -> str:
        """
        Hash the given password using SHA-256 algorithm.

        Args:
            password: The password to hashed.
        """
        p_hash = hashlib.sha256(password.encode())
        return p_hash.hexdigest()

    @classmethod
    def create_user(cls, username: str, password: str, birth: str, telephone_number: str = None,role=UserRole.USER) -> str:
        """
        Create a new user and save it to the database.

        Args:
            username: The username for the new user.
            password: The password for the new user.
            telephone_number: The telephone number for the new user. Defaults to None.
        """
        try:
            password = cls.build_pass(password)
            id = str(uuid4())
            submit_date = str(dt.date.today())
            user = cls(username, password, birth, id, submit_date, telephone_number,role=UserRole.USER)
            user.save_to_database()
            return "\n>>>> Welcome : User created successfully. <<<<\n"
        except ValueError as Err:
            return str(Err)
        
    @classmethod
    def create_admin(cls, username: str, password: str,role=UserRole.ADMIN) -> str:
        """
        Create a new user and save it to the database.

        Args:
            username: The username for the new user.
            password: The password for the new user.
            telephone_number: The telephone number for the new user. Defaults to None.
        """
        try:
            password = cls.build_pass(password)
            birth = ""
            id = str(uuid4())
            submit_date = ""
            user = cls(username, password, birth, id, submit_date, role=UserRole.ADMIN)
            user.save_to_database()
            return "\n>>>> Welcome : Admin created successfully. <<<<\n"
        except ValueError as Err:
            return str(Err)
        
    @classmethod
    def create_manager(cls, username: str, password: str,role=UserRole.MANAGER) -> str:
        try:
            password = cls.build_pass(password)
            birth = ""
            id = str(uuid4())
            submit_date = ""
            user = cls(username, password, birth, id, submit_date, role=UserRole.MANAGER)
            user.save_to_database()
            return "\n>>>> Welcome: Manager created successfully. <<<<\n"
        except ValueError as Err:
            return str(Err)
    
    @classmethod
    def create_manager_from_args(cls, args):
        username = args.username
        password = args.password
        # role = "MANAGER"
        # cls.create_manager(username, password, role)

        message_create_user = cls.create_manager(username, password, UserRole.MANAGER)
        print(message_create_user)

    @classmethod
    def get_manager_details(cls):
        manager_username = None
        for username, user_info in cls._users.items():
            if user_info["role"] == UserRole.MANAGER.value:
                manager_username = username
                break

        if manager_username is not None:
            print("<---------Manager Details--------->")
            print(f"Manager Username: {manager_username}\n")
        else:
            print("No manager user found.")

    def update_username(self, new_username: str) -> str:
        """
        Update the username for the user.

        Args:
            new_username: The new username set.

        Returns:
            message: the username was updated successfully.
        """
        try:
            if self.username in User._users:
                if new_username in User._users:
                    raise ValueError("This username already exists.")
                else:
                    User._users.pop(self.username)
                    self.username = new_username
                    User._users[new_username] = self
                    self.save_to_database()
                    return "\n>>>> Username updated successfully. <<<<\n"
            else:
                raise ValueError("The user does not exist.")
        except ValueError as err:
            return str(err)

    def update_telephone_number(self, new_telephone_number: str) -> str:
        """
        Update the telephone number for the user.

        Args:
            new_telephone_number: The new telephone number set.

        Returns:
            message: telephone number was updated successfully.
        """
        try:
                self.telephone_number = new_telephone_number
                self.save_to_database()
                return "\n>>>> Telephone number updated successfully. <<<<\n"
        except ValueError as Err:
            return str(Err)

    def update_password(self, old_password: str, new_password1: str, new_password2: str) -> str:
        """
        Update the password for the user.

        Args:
            old_password: The old password.
            new_password1: The new password.
            new_password2: The new password confirmation.

        Returns:
            message: password was updated successfully
        """
        try:
            new_pass = self.validate_newpass(new_password1, new_password2)
            old_password = self.build_pass(old_password)

            if old_password != self._password:
                raise ValueError("Incorrect old password.")
            elif new_pass is not None:
                raise ValueError(new_pass)
            elif new_password1 != new_password2:
                raise ValueError("New passwords do not match.")
            elif len(new_password1) < 4:
                raise ValueError("New password must be at least 4 characters long.")
            elif self.build_pass(new_password1) == old_password:
                raise ValueError("New password must be different from the old password.")
            else:
                self._password = self.build_pass(new_password1)
                self.save_to_database()
                return "\n>>>> Password updated successfully. <<<<\n"
           
        except ValueError as Err:
            return str(Err)

    @staticmethod
    def validate_newpass(pass1: str, pass2: str) -> str:
        """
        Validate the new password and check if it matches the confirmation.

        Args:
            pass1: The new password.
            pass2: The new password confirmation.

        Returns:
            message: new passwords match or not
        """
        if pass1 != pass2:
            raise ValueError("New passwords do not match.")
        return None

    def save_to_database(self) -> None:
        """
        Save the user data to the database file.
        """
        with open("database.json", "w", encoding="utf_8") as file:
            user_data = {
                "id": self.id,
                "username": self.username,
                "password": self._password,
                "birthday": self.birth,
                "submit_date": self.submit_date,
                "telephone_number": self.telephone_number,
                "role": self.role.value,
            }
            User._users[self.username] = user_data
            json.dump(User._users, file, indent=4)

    @classmethod
    def load_from_database(cls) -> None:
        """
        Load user data from the database file.
        """
        try:
            with open("database.json", "r", encoding="utf_8") as file:
                User._users = json.load(file)
       
        except FileNotFoundError:
            User._users = {}
            
    @staticmethod
    def validate_password(password: str) -> str:
        """
        Validate the password and check if it meets the requirements.

        Args:
            password: The password to be validated.
        """
        if len(password) < 4:
            return False
        return True
       
    @staticmethod
    def clear_screen():
        if platform.system() == "Windows":
            os.system("cls")    
        else:
            os.system("clear")

    def is_birthday(self) -> bool:
        """
        Check if it's the user's birthday today.
        """
        today = dt.date.today()
        user_birth = dt.datetime.strptime(self.birth, '%Y-%m-%d')
        if today.month == user_birth.month and today.day == user_birth.day:
            return True
        return False
    
    def apply_discount(self, original_price: float) -> float:
            """
            Apply a discount to the original price based on the user's membership and birthday.
            """
            if self.is_birthday():
                final_price = original_price * 0.5
            else:
                membership_months = self.calculate_membership()
                discount_percentage = membership_months * 0.1
                discount_amount = original_price * discount_percentage
                final_price = original_price - round(discount_amount, 2)
            return final_price