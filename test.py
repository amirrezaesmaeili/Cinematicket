from unittest import TestCase, main
from users import User, UserRole

class TestUser(TestCase):
    def setUp(self):
        self.username = "admin"
        self.password = "password"

    def test_create_admin(self):

        expected_output = "\n>>>> Welcome : Admin created successfully. <<<<\n"
        actual_output = User.create_admin(self.username, self.password)
        self.assertEqual(actual_output, expected_output)
            
        expected_output = "This username already exists."
        actual_output = User.create_admin(self.username, self.password)
        self.assertEqual(actual_output, expected_output)


        self.password = "123"
        expected_output = "New password must be at least 4 characters long."
        actual_output = User.create_admin(self.username, self.password)
        self.assertEqual(actual_output, expected_output)


if __name__ == "__main__":
    main()