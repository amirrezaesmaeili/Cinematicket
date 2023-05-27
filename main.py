from users import User
import getpass
import argparse

def main():
    parser = argparse.ArgumentParser(description="User Login")
    parser.add_argument("--manager", action="store_true", help="Create an admin user")
    parser.add_argument('-u',"--username", type=str, help="Username")
    parser.add_argument('-p',"--password", type=str, help="Password")
    args = parser.parse_args()

    if args.manager:
        User.create_manager_from_args(args)
        User.get_manager_details()
        
    while True:
        print("Menu:")
        print("0: Exit program")
        print("1: Admin Panel")
        print("2: User Panel")
        choice = input("\nEnter your choice: ")
        
        if choice == "0":
            break
        
        elif choice == "1":
            print("0: Exit program")
            print("1: Add Admin")
            print("2: cinema screenings")
            manager_choice = input("\nEnter your choice: ")
            
            if manager_choice == "0":
                break
            elif manager_choice == "1":
                pass
            elif manager_choice == "2":
                pass
            
                
        elif choice == "2":
            print("Menu:")
            print("0: Exit program")
            print("1: Register user")
            print("2: Login user")
            user_choice = input("\nEnter your choice: ")
            
            if user_choice == "0":
                break
            
            elif user_choice == "1":
                username = input("Enter a username: \n")
                password = getpass.getpass("Enter a password (at least 4 characters): \n")
                telephone_number = input("Enter a telephone number (optional): \n")
                message_create_user = User.create_user(username, password, telephone_number)
                print(message_create_user)
            
            elif user_choice == "2":
                username = input("Enter your username: ")
                password = User.build_pass(getpass.getpass("Enter your password: \n"))
                User.load_from_database()
                if username in User.users and User.users[username]["password"] == password:
                    user = User(username, User.users[username]["password"], User.users[username]["telephone_number"])
                    
                    while True:
                        print("User menu:")
                        print("1: View user information")
                        print("2: Edit user information")
                        print("3: Change password")
                        print("4: Logout")
                        user_login_choice = input("Enter your choice: ")
                        
                        if  user_login_choice == "1":
                            print(user)

                        elif  user_login_choice == "2":
                            print("1. Edit username")
                            print("2. Edit phone number")
                            user_edit_choice = input("Enter choice: ")
                            if user_edit_choice == "1":
                                new_username = input("Enter a new username: ")
                                if new_username in User.users:
                                   print("Username already exists.")
                                else:
                                   message_update_username = user.update_username(new_username)
                                   print(message_update_username)
                            elif user_edit_choice == "2":
                                new_telephone_number = input("Enter a new telephone number: ")
                                message_update_telephonenumber = user.update_telephone_number(new_telephone_number)
                                print(message_update_telephonenumber)
                            else:            
                              print("\n>>>> Invalid choice <<<<\n")
                                
                        elif user_login_choice == "3":
                            
                            old_password = getpass.getpass("Enter your old password: ")
                            new_password1 = getpass.getpass("Enter your new password: ")
                            new_password2 = getpass.getpass("Enter your new password again: ")
                            message_update_password = user.update_password(old_password, new_password1, new_password2)
                            print(message_update_password)

                        elif user_login_choice == "4":
                            break
                        
                        else:            
                            print("\n>>>> Invalid choice <<<<\n")

            else:            
                print("\n>>>> Invalid choice <<<<\n")
       
        else:            
            print("\n>>>> Invalid choice <<<<\n")
                 
        
if __name__ == "__main__":
    main()
    