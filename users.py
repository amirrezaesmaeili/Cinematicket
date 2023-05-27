import uuid
import hashlib
import json
from enum import Enum

class UserRole(Enum):
    MANAGER = "manager"
    ADMIN = "admin"
    USER = "user"

class User:
    users = {}

    def __init__(self, username: str, password: str, telephone_number= None,role=UserRole.USER) -> None:
        """
        Initialize a User object.

        Args:
            username : The username for the user.
            password : The password for the user.
            telephone_number: telephone number for the user. Defaults to None.
        """
        self.username = username
        self._password = password
        self.telephone_number = telephone_number
        self.id = str(uuid.uuid4())
        self.role = role

    def __str__(self) -> str:
        """
        Return a string representation of the User object.
        """
        return f"ID: {self.id}\nUsername: {self.username}\nTelephone Number: {self.telephone_number}\nUser Role{self.role}"

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
    def create_user(cls, username: str, password: str, telephone_number: str = None,role=UserRole.USER) -> str:
        """
        Create a new user and save it to the database.

        Args:
            username: The username for the new user.
            password: The password for the new user.
            telephone_number: The telephone number for the new user. Defaults to None.
        """
        try:
            cls.load_from_database()
            validate = cls.validate_password(password)

            if username in cls.users:
                raise ValueError("This username already exists.")
            elif validate is not None:
                raise ValueError(validate)
            else:
                password = cls.build_pass(password)
                user = cls(username, password, telephone_number,role=UserRole.USER)
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
            cls.load_from_database()
            validate = cls.validate_password(password)

            if username in cls.users:
                raise ValueError("This username already exists.")
            elif validate is not None:
                raise ValueError(validate)
            else:
                password = cls.build_pass(password)
                user = cls(username, password,role=UserRole.ADMIN)
                user.save_to_database()
                return "\n>>>> Welcome : Admin created successfully. <<<<\n"
        except ValueError as Err:
            return str(Err)
        
    @classmethod
    def create_manager(cls, username: str, password: str,role=UserRole.MANAGER) -> str:
        try:
            cls.load_from_database()
            validate = cls.validate_password(password)

            if username in cls.users:
                raise ValueError("This username already exists.")
            elif validate is not None:
                raise ValueError(validate)
            else:
                password = cls.build_pass(password)
                user = cls(username, password, role=UserRole.MANAGER)
                user.save_to_database()
                return "\n>>>> Welcome: Manager created successfully. <<<<\n"
        except ValueError as Err:
            return str(Err)
    
    @classmethod
    def create_manager_from_args(cls, args):
        username = args.username
        password = args.password

        message_create_user = cls.create_manager(username, password, UserRole.MANAGER)
        print(message_create_user)

    @classmethod
    def get_manager_details(cls):
        manager_username = None
        for username, user_info in cls.users.items():
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
            if new_username in User.users:
                raise ValueError("This username already exists.")
            else:
                User.users.pop(self.username)
                self.username = new_username
                User.users[new_username] = self
                self.save_to_database()
                return "\n>>>> Username updated successfully. <<<<\n"
        except ValueError as Err:
            return str(Err)    

    def update_telephone_number(self, new_telephone_number: str) -> str:
        """
        Update the telephone number for the user.

        Args:
            new_telephone_number: The new telephone number set.

        Returns:
            message: telephone number was updated successfully.
        """
        try:
            if new_telephone_number in User.users:
                raise ValueError("This telephone number already exists.")
            else:
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
                "telephone_number": self.telephone_number,
                "role": self.role.value,
            }
            User.users[self.username] = user_data
            json.dump(User.users, file, indent=4)

    @classmethod
    def load_from_database(cls) -> None:
        """
        Load user data from the database file.
        """
        try:
            with open("database.json", "r", encoding="utf_8") as file:
                User.users = json.load(file)
       
        except FileNotFoundError:
            User.users = {}
            
    @staticmethod
    def validate_password(password: str) -> str:
        """
        Validate the password and check if it meets the requirements.

        Args:
            password: The password to be validated.
        """
        if len(password) < 4:
            raise ValueError("New password must be at least 4 characters long.")
        
    