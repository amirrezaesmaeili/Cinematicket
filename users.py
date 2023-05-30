from uuid import uuid4
import hashlib
import json
from enum import Enum
import os
import platform
import logging

logger = logging.getLogger("UserLogger")
logger.setLevel(level=logging.INFO)
file_handler = logging.FileHandler("cinematicket.log")
pattern = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(pattern)
logger.addHandler(file_handler)

class UserRole(Enum):
    MANAGER = "manager"
    ADMIN = "admin"
    USER = "user"

class User:
    _users = {}

    def __init__(self, username: str, password: str, birth: str, id: str, submit_date, telephone_number= None, role=UserRole.USER) -> None:
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
        return f"ID: {self.id}\nUsername: {self.username}\nTelephone Number: {self.telephone_number}"

    def age_counter(self) -> int:
        """
        calculate and return user age.
        """
        today = dt.datetime.today()
        user_birth = dt.datetime.strptime(self.birth, '%Y-%m-%d')
        user_age = (today - user_birth).days // 365
        logger.info(f"{self.username} is {user_age} years old.")
        return user_age

    def calculate_membership(self) -> int:
        """
        calculate and return user membership time.
        """
        today = dt.date.today()
        membership = today - self.submit_date
        logger.info(f"{self.username}'s membership is {membership}")
        return membership

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
    def sign_up(cls, username: str, password: str, role: str, birth: str, telephone_number=None):
        cls.load_from_database()
        if username in cls._users:
            logger.error("This username already exists.")
            raise ValueError("This username already exists.")
        else:
            validate = cls.validate_password(password)
            if validate:
                if role == "USER":
                    if birth:
                        logger.info("Creating User")
                        cls.create_user(username, password, birth, telephone_number,role=UserRole.USER)
                    else:
                        raise ValueError("Birthday field is required!")
                elif role == "ADMIN":
                    logger.info("Creating Admin")
                    cls.create_admin(username, password,role=UserRole.ADMIN)
                elif role == "MANAGER":
                    logger.info("Creating Manager")
                    cls.create_manager(username, password, role=UserRole.MANAGER)
            else:
                raise ValueError("Password must be at least 4 characters long.")

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
            submit_date = dt.date.today()
            user = cls(username, password, birth, id, submit_date, telephone_number,role=UserRole.USER)
            user.save_to_database()
            logger.info("Welcome : User created successfully.")
        except ValueError as Err:
            logger.error(Err)
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
            user = cls(username, password,role=UserRole.ADMIN)
            user.save_to_database()
            logger.info("Welcome : Admin created successfully.")
        except ValueError as Err:
            logger.error(Err)
            return str(Err)
        
    @classmethod
    def create_manager(cls, username: str, password: str,role=UserRole.MANAGER) -> str:
        try:
            password = cls.build_pass(password)
            user = cls(username, password, role=UserRole.MANAGER)
            user.save_to_database()
            logger.info("Welcome : Manager created successfully.")
            return "\n>>>> Welcome: Manager created successfully. <<<<\n"
        except ValueError as Err:
            logger.error(Err)
            return str(Err)
    
    @classmethod
    def create_manager_from_args(cls, args):
        username = args.username
        password = args.password
        role = "MANAGER"
        cls.sign_up(username, password, role)
        # message_create_user = cls.create_manager(username, password, UserRole.MANAGER)
        # print(message_create_user)

    @classmethod
    def get_manager_details(cls):
        manager_username = None
        for username, user_info in cls._users.items():
            if user_info["role"] == UserRole.MANAGER.value:
                manager_username = username
                break

        if manager_username is not None:
            logger.info("<---------Manager Details--------->")
            logger.info(f"Manager Username: {manager_username}")
            print("<---------Manager Details--------->")
            print(f"Manager Username: {manager_username}\n")
        else:
            logger.warning("No manager user found.")
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
            User._users.pop(self.username)
            self.username = new_username
            User._users[new_username] = self
            self.save_to_database()
            logger.info("The username was updated successfully")
        except ValueError as Err:
            logger.error(Err)
            return str(Err)    

    def update_telephone_number(self, new_telephone_number: str) -> str:
        """
        Update the telephone number for the user.

        Args:
            new_telephone_number: The new telephone number set.

        """
        try:
            self.telephone_number = new_telephone_number
            self.save_to_database()
            logger.info("Telephone number was updated successfully.")
        except ValueError as Err:
            logger.error(Err)
            return str(Err)

    def update_password(self, old_password: str, new_password1: str, new_password2: str) -> str:
        """
        Update the password for the user.

        Args:
            old_password: The old password.
            new_password1: The new password.
            new_password2: The new password confirmation.

        Returns:
            raise value eror if password is wrong.
        """
        try:
            new_pass = self.validate_newpass(new_password1, new_password2)
            old_password = self.build_pass(old_password)

            if old_password != self._password:
                logger.error("Incorrect old password.")
                raise ValueError("Incorrect old password.")
            elif new_pass is not None:
                logger.error(ValueError)
                raise ValueError(new_pass)
            elif new_password1 != new_password2:
                logger.error("New passwords do not match.")
                raise ValueError("New passwords do not match.")
            elif len(new_password1) < 4:
                logger.error("New password must be at least 4 characters long.")
                raise ValueError("New password must be at least 4 characters long.")
            elif self.build_pass(new_password1) == old_password:
                logger.error("New password must be different from the old password.")
                raise ValueError("New password must be different from the old password.")
            else:
                self._password = self.build_pass(new_password1)
                self.save_to_database()
                logger.info("Password updated successfully.")          
        except ValueError as Err:
            logger.error(Err)
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
            logger.error("New passwords do not match.")
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
            logger.error("New password must be at least 4 characters long.")
        return True
     
    @staticmethod
    def clear_screen():
        if platform.system() == "Windows":
            os.system("cls")    
        else:
            os.system("clear")      



#user = User.create_user("mah", "aban")
# print(type(user.role))
# print(user.role.value)