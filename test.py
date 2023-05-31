from unittest import TestCase, main
from unittest.mock import patch
from users import User,UserRole
from cinema import Cinema
from argparse import Namespace
import datetime as dt
import json
import os

class TestUser(TestCase):
    def setUp(self):
        self.username_user = "user"
        self.password_user = "password"
        self.telephone_number = "null"
        self.username_admin = "admin"
        self.password_admin = "password"
        self.username_manager = "manager"
        self.password_manager = "password"
        self.id = "id"
        self.birth = "1992-11-19"
        self.submit_date = dt.date(2022,11,19)
        self.user_update = User("old_username", "password", self.birth, self.id, "submit_date")
        self.user_change_phone = User("John", "password",  self.birth, self.id, "submit_date", "1234")
        # self.user_change_pass = User("Alex", "password123")
        self.user_save_to_database = User("testuser", "password", self.birth, self.id, "submit_date", "1234567890")
        self.discount = User(self.username_user, self.password_user, self.birth, self.id, self.submit_date)
    
    def tearDown(self):
        User._users.clear()
        
    def test_create_user(self):
        expected_output = "\n>>>> Welcome : User created successfully. <<<<\n"
        actual_output = User.create_user(self.username_user, self.password_user, self.birth)
        self.assertEqual(actual_output, expected_output)
    
    def test_create_admin(self):

        expected_output = "\n>>>> Welcome : Admin created successfully. <<<<\n"
        actual_output = User.create_admin(self.username_admin, self.password_admin)
        self.assertEqual(actual_output, expected_output)

    def test_create_manager(self):

        expected_output = "\n>>>> Welcome: Manager created successfully. <<<<\n"
        actual_output = User.create_manager(self.username_manager, self.password_manager)
        self.assertEqual(actual_output, expected_output)

    def test_create_manager_from_args(self):
        args = Namespace(username="mng", password="password")
        expected_output = "\n>>>> Welcome: Manager created successfully. <<<<\n"
        
        with patch('builtins.print') as mock_print:
            User.create_manager_from_args(args)
            mock_print.assert_called_with(expected_output)
        os.remove("database.json")
    
    def test_get_manager_details(self):
        manager_username = 'ali'
        expected_output = f"Manager Username: {manager_username}\n"
        
        User._users = {manager_username: {"role": UserRole.MANAGER.value}}
        
        with patch('builtins.print') as mock_print:
            User.get_manager_details()
            mock_print.assert_called_with(expected_output)
        
       
    def test_update_username(self):
            User.create_user("old_username", "password", self.birth)
            new_username = "username"
            result = self.user_update.update_username(new_username)
            self.assertEqual(result, "\n>>>> Username updated successfully. <<<<\n")
            
            new_username = "username"
            result = self.user_update.update_username(new_username)
            self.assertEqual(result, "This username already exists.")
            
            User._users.clear()
            new_username = "new_username"
            result = self.user_update.update_username(new_username)
            self.assertEqual(result, "The user does not exist.") 
            os.remove("database.json")

    def test_update_telephone_number(self):
        
        user1 = self.user_change_phone
    
        result1 = user1.update_telephone_number("1234567890")

        self.assertEqual(result1, "\n>>>> Telephone number updated successfully. <<<<\n")
        self.assertEqual(user1.telephone_number, "1234567890")
        os.remove("database.json")

    def test_update_password(self):
        
        result1 = self.user_change_pass.update_password("password123", "newpassword123", "newpassword123")
        self.assertEqual(result1, "\n>>>> Password updated successfully. <<<<\n")

        
        result2 = self.user_change_pass.update_password("wrongpassword", "newpassword123", "newpassword123")
        self.assertEqual(result2, "Incorrect old password.")

        result3 = self.user_change_pass.update_password("password123", "short", "short")
        self.assertEqual(result3, "New password must be at least 4 characters long.")

        result4 = self.user_change_pass.update_password("password123", "newpassword123", "mismatch")
        self.assertEqual(result4, "New passwords do not match.")

        
        result5 = self.user_change_pass.update_password("password123", "password123", "password123")
        self.assertEqual(result5, "New password must be different from the old password.")
    
    def test_save_to_database(self):
        user = self.user_save_to_database

        user.save_to_database()

        User.load_from_database()

        self.assertIn("testuser", User._users)

        user_data = User._users["testuser"]

        self.assertEqual(user_data["id"], user.id)
        self.assertEqual(user_data["username"], user.username)
        self.assertEqual(user_data["password"], user._password)
        self.assertEqual(user_data["telephone_number"], user.telephone_number)
        self.assertEqual(user_data["role"], user.role.value)
        os.remove("database.json")
    
    def test_load_from_database(self):
        user_data = {
            "testuser1": {
                "id": "123",
                "username": "testuser1",
                "password": "password1",
                "telephone_number": "1234567890",
                "role": "user"
            },
            "testuser2": {
                "id": "456",
                "username": "testuser2",
                "password": "password2",
                "telephone_number": "9876543210",
                "role": "admin"
            }
        }

        with open("database.json", "w", encoding="utf_8") as file:
            json.dump(user_data, file, indent=4)

        User._users = {}

        User.load_from_database()

        self.assertEqual(User._users, user_data)
        os.remove("database.json")
    
    def test_validate_password(self):
        password = User.validate_password("abcd1234")
        self.assertTrue(password)

        password = User.validate_password("abc")
        self.assertFalse(password)
 
    def test_age_counter(self):
        expected_output = 30
        actual_output = User.age_counter(self)
        self.assertEqual(actual_output, expected_output)

    def test_calculate_membership(self):
        expected_output = 6
        actual_output = User.calculate_membership(self)
        self.assertEqual(actual_output, expected_output)

    def test_sign_up(self):
        self.password = "password"
        self.role = "USER"
        result = User.sign_up(self.username_user, self.password, self.role, self.birth, self.telephone_number)
        self.assertEqual(result, "Creating User")

        self.role = "ADMIN"
        result = User.sign_up(self.username_admin, self.password_admin, self.role, self.birth)
        self.assertEqual(result, "Creating Admin")

        self.role = "MANAGER"
        result = User.sign_up(self.username_manager, self.password_manager, self.role, self.birth)
        self.assertEqual(result, "Creating Manager")

        self.role = "USER"
        with self.assertRaises(ValueError):
            User.sign_up(self.username_user, "abc", self.role, self.birth)

        self.role = "USER"
        with self.assertRaises(ValueError):
            User.sign_up(self.username_user, self.password_user, self.role, None)

        self.role = "USER"
        User._users = {self.username_user: {"password": "existing", "role": "USER", "birth": "1990-01-01"}}
        with self.assertRaises(ValueError):
            User.sign_up(self.username_user, self.password_user, self.role, self.birth)

    def test_is_birthday(self):
        birthday = User.is_birthday(self)
        self.assertFalse(birthday)

        self.birth = str(dt.date.today())
        birthday = User.is_birthday(self)
        self.assertTrue(birthday)

    def test_apply_discount(self):
        result = self.discount.apply_discount(30000)
        self.assertEqual(result, 12000)

        self.birth = str(dt.date.today())
        self.discount = User(self.username_user, self.password_user, self.birth, self.id, self.submit_date)
        result = self.discount.apply_discount(30000)
        self.assertEqual(result, 15000)


class TestCinema(TestCase):
    
    def test_create_sans(self):
        result = Cinema.create_sans("Film1", "Genre1", "10:00", 18, 100, 20000)
        expected = "\n>>>>  Sans created successfully. <<<<\n"
        self.assertEqual(result, expected)
        os.remove("Cinema_sans.json")
        
    def test_save_sans_to_file(self):

        cinema = Cinema("Film1", "Genre1", "10:00", 18, 100)


        cinema.save_sans_to_file()


        self.assertTrue(os.path.exists("Cinema_sans.json"))


        with open("Cinema_sans.json", "r", encoding="utf_8") as file:
            data = json.load(file)


        self.assertIn("Film1", data)

        self.assertEqual(data["Film1"]["film_name"], "Film1")
        self.assertEqual(data["Film1"]["film_genre"], "Genre1")
        self.assertEqual(data["Film1"]["film_play_time"], "10:00")
        self.assertEqual(data["Film1"]["film_age_category"], 18)
        self.assertEqual(data["Film1"]["capacity"], 100)    
    
        os.remove("Cinema_sans.json")
    
    def test_load_sans_from_file(self):
        data = {
            "Film1": {
                "id": 1,
                "film_name": "Film1",
                "film_genre": "Genre1",
                "film_play_time": "10:00",
                "film_age_category": 18,
                "capacity": 100
            },
            "Film2": {
                "id": 2,
                "film_name": "Film2",
                "film_genre": "Genre2",
                "film_play_time": "12:00",
                "film_age_category": 12,
                "capacity": 80
            }
        }
        with open("Cinema_sans.json", "w", encoding="utf_8") as file:
            json.dump(data, file, indent=4)

        Cinema.load_sans_from_file()

        self.assertEqual(Cinema.sans["Film1"]["film_name"], "Film1")
        self.assertEqual(Cinema.sans["Film1"]["film_genre"], "Genre1")
        self.assertEqual(Cinema.sans["Film1"]["film_play_time"], "10:00")
        self.assertEqual(Cinema.sans["Film1"]["film_age_category"], 18)
        self.assertEqual(Cinema.sans["Film1"]["capacity"], 100)

        self.assertEqual(Cinema.sans["Film2"]["film_name"], "Film2")
        self.assertEqual(Cinema.sans["Film2"]["film_genre"], "Genre2")
        self.assertEqual(Cinema.sans["Film2"]["film_play_time"], "12:00")
        self.assertEqual(Cinema.sans["Film2"]["film_age_category"], 12)
        self.assertEqual(Cinema.sans["Film2"]["capacity"], 80)

        os.remove("Cinema_sans.json")
       
    def test_get_all_sans(self):
        film_name = "Film Name"
        film_genre = "Film Genre"
        film_play_time = "12:00"
        film_age_category = 18
        capacity = 100

        with patch('cinema.Cinema.load_sans_from_file') as mock_load_sans:
            mock_load_sans.return_value = None

            sans_list = Cinema.get_all_sans()

            mock_load_sans.assert_called_once()


        self.assertEqual(sans_list, list(Cinema.sans.values()))


if __name__ == "__main__":
    main()