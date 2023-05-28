from unittest import TestCase, main
from unittest.mock import patch
from users import User,UserRole
from argparse import Namespace

class TestUser(TestCase):
    def setUp(self):
        self.username_user = "user"
        self.password_user = "password"
        self.telephone_number = "null"
        self.username_admin = "admin"
        self.password_admin = "password"
        self.username_manager = "manager"
        self.password_manager = "password"
        self.user_update = User("old_username", "password")
        User.create_user("old_username", "password")
        self.user_phone = User("John", "password","1234")
        
    
    def tearDown(self):
        User.users.clear()
        
    def test_create_user(self):
        expected_output = "\n>>>> Welcome : User created successfully. <<<<\n"
        actual_output = User.create_user(self.username_user, self.password_user)
        self.assertEqual(actual_output, expected_output)

        expected_output = "This username already exists."
        actual_output = User.create_user(self.username_user, self.password_user)
        self.assertEqual(actual_output, expected_output)

        self.password_user = "123"
        expected_output = "New password must be at least 4 characters long."
        actual_output = User.create_user(self.username_user, self.password_user)
        self.assertEqual(actual_output, expected_output)

        self.password_user = "password"
        expected_output = "This username already exists."
        actual_output = User.create_user(self.username_user, self.password_user)
        self.assertEqual(actual_output, expected_output)
    
    def test_create_admin(self):

        expected_output = "\n>>>> Welcome : Admin created successfully. <<<<\n"
        actual_output = User.create_admin(self.username_admin, self.password_admin)
        self.assertEqual(actual_output, expected_output)
            
        expected_output = "This username already exists."
        actual_output = User.create_admin(self.username_admin, self.password_admin)
        self.assertEqual(actual_output, expected_output)


        self.password_admin = "123"
        expected_output = "New password must be at least 4 characters long."
        actual_output = User.create_admin(self.username_admin, self.password_admin)
        self.assertEqual(actual_output, expected_output)

    def test_create_manager(self):

        expected_output = "\n>>>> Welcome: Manager created successfully. <<<<\n"
        actual_output = User.create_manager(self.username_manager, self.password_manager)
        self.assertEqual(actual_output, expected_output)

        expected_output = "This username already exists."
        actual_output = User.create_manager(self.username_manager, self.password_manager)
        self.assertEqual(actual_output, expected_output)

        self.password_manager = "123"
        expected_output = "New password must be at least 4 characters long."
        actual_output = User.create_manager(self.username_manager, self.password_manager)
        self.assertEqual(actual_output, expected_output)

        self.password_manager = "password"
        expected_output = "This username already exists."
        actual_output = User.create_manager(self.username_manager, self.password_manager)
        self.assertEqual(actual_output, expected_output)

    def test_create_manager_from_args(self):
        args = Namespace(username="mng", password="password")
        expected_output = "\n>>>> Welcome: Manager created successfully. <<<<\n"
        
        with patch('builtins.print') as mock_print:
            User.create_manager_from_args(args)
            mock_print.assert_called_with(expected_output)
    
    def test_get_manager_details(self):
        manager_username = 'ali'
        expected_output = f"Manager Username: {manager_username}\n"
        
        User.users = {manager_username: {"role": UserRole.MANAGER.value}}
        
        with patch('builtins.print') as mock_print:
            User.get_manager_details()
            mock_print.assert_called_with(expected_output)
       
    def test_update_username(self):

            new_username = "username"
            result = self.user_update.update_username(new_username)
            self.assertEqual(result, "\n>>>> Username updated successfully. <<<<\n")
            
            new_username = "username"
            result = self.user_update.update_username(new_username)
            self.assertEqual(result, "This username already exists.")
            
            User.users.clear()
            new_username = "new_username"
            result = self.user_update.update_username(new_username)
            self.assertEqual(result, "The user does not exist.") 

    def test_update_telephone_number(self):
        
        user1 = self.user_phone
    
        result1 = user1.update_telephone_number("1234567890")

        self.assertEqual(result1, "\n>>>> Telephone number updated successfully. <<<<\n")
        self.assertEqual(user1.telephone_number, "1234567890")

if __name__ == "__main__":
    main()