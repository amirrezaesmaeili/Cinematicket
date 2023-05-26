from users import User
import pwinput


def main()-> None:
    """
    Main function to run the user management program.
    """
    while True:
        print("Menu:")
        print("0: Exit program")
        print("1: Create a new user")
        print("2: Login with username and password")
        choice = input("\nEnter your choice: ")

        if choice == "0":
            break

        elif choice == "1":
            username = input("Enter a username: \n")
            password = pwinput.pwinput("Enter a password: \n")
            telephone_number = input("Enter a telephone number (optional): \n")
            message_create_user = User.create_user(username, password, telephone_number)
            print(message_create_user)

        elif choice == "2":
            username = input("Enter your username: ")
            password = User.build_pass(pwinput.pwinput("Enter your password: \n"))
            User.load_from_database()
            if username in User.users and User.users[username]["password"] == password:
                user = User(username, User.users[username]["password"], User.users[username]["telephone_number"])
                
                while True:
                    print("User menu:")
                    print("1: View user information")
                    print("2: Update username or telephone number")
                    print("3: Change password")
                    print("4: Log out and return to main menu")
                    user_choice = input("Enter your choice: ")
                    
                    if user_choice == "1":
                        print(user)

                    elif user_choice == "2":
                        new_username = input("Enter a new username: ")
                        new_telephone_number = input("Enter a new telephone number: ")
                        if new_username or new_telephone_number:
                            message_update_username = user.update_username(new_username)
                            print(message_update_username)
                            message_update_telephonenumber = user.update_telephone_number(new_telephone_number)
                            print(message_update_telephonenumber)

                    elif user_choice == "3":
                        old_password = pwinput.pwinput("Enter your old password: ")
                        new_password1 = pwinput.pwinput("Enter your new password: ")
                        new_password2 = pwinput.pwinput("Enter your new password again: ")
                        message_update_password = user.update_password(old_password, new_password1, new_password2)
                        print(message_update_password)

                    elif user_choice == "4":
                        break

                    else:            
                        print("\n>>>> Invalid choice <<<<\n")

            else:
                print("\n>>>> Invalid username or password <<<<\n")

        else:
            print("\n>>>> Invalid choice <<<<\n")

if __name__ == "__main__":
    main()