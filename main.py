from users import User
from cinema import Cinema
import getpass
import argparse

def main():
    User.clear_screen()
    parser = argparse.ArgumentParser(description="User Login")
    parser.add_argument("-m","--manager", action="store_true", help="Create an admin user")
    parser.add_argument('-u',"--username", type=str, help="Username")
    parser.add_argument('-p',"--password", type=str, help="Password")
    args = parser.parse_args()

    if args.manager:
        User.create_manager_from_args(args)
        User.get_manager_details()
        
        
    while True:
        User.clear_screen()
        print("<------Menu------>")
        print("0: Exit program")
        print("1: Manager Panel")
        print("2: User Panel")
        choice = input("\nEnter your choice: ")
        
        if choice == "0":
            User.clear_screen()
            break
        
        elif choice == "1":
            User.clear_screen()
            if args.manager:
                print("<------Manager Panel------>")
                print("0: Exit program")
                print("1: Add Admin")
                print("2: cinema screenings")
                print("3: Logout")
                manager_choice = input("\nEnter your choice: ")
                
                if manager_choice == "0":
                    User.clear_screen()
                    break
                
                elif manager_choice == "1":
                    User.clear_screen()
                    username = input("Enter a username for admin: \n")
                    password = getpass.getpass("Enter a password (at least 4 characters): \n")
                    message_create_user = User.create_admin(username, password)
                    print(message_create_user)
                    
                
                elif manager_choice == "2":
                    User.clear_screen()
                    film_name = input("Enter Film Name: \n")
                    film_genre = input("Enter Film Genre: \n")
                    film_play_time = input("Enter Film Playing Time In 00:00 Format: \n")
                    film_age_category = input("Enter Age Category Of The Film: \n")
                    capacity = input("Enter The Cinema Capacity: \n")
                    message_create_sans = Cinema.create_sans(film_name,film_genre,film_play_time,film_age_category,capacity)
                    print(message_create_sans)
                
                elif manager_choice == "3":
                    User.clear_screen()
                    break
                    
            else:
                print("You Have No Permissions")
                User.clear_screen()
                
        elif choice == "2":
            User.clear_screen()
            print("Menu:")
            print("0: Exit program")
            print("1: Register user")
            print("2: Login user")
            user_choice = input("\nEnter your choice: ")
            
            
            if user_choice == "0":
                User.clear_screen()
                break
            
            elif user_choice == "1":
                User.clear_screen()
                username = input("Enter a username: \n")
                password = getpass.getpass("Enter a password (at least 4 characters): \n")
                telephone_number = input("Enter a telephone number (optional): \n")
                message_create_user = User.create_user(username, password, telephone_number)
                print(message_create_user)
                
            
            elif user_choice == "2":
                User.clear_screen()
                username = input("Enter your username: ")
                password = User.build_pass(getpass.getpass("Enter your password: \n"))
                User.load_from_database()
                if username in User.users and User.users[username]["password"] == password:
                    user = User(username, User.users[username]["password"], User.users[username]["telephone_number"])
                    
                    while True:
                        User.clear_screen()
                        print("User menu:")
                        print("1: View user information")
                        print("2: Edit user information")
                        print("3: Change password")
                        print("4: Logout")
                        user_login_choice = input("Enter your choice: ")
                        
                        if  user_login_choice == "1":
                            User.clear_screen()
                            print(user)

                        elif  user_login_choice == "2":
                            User.clear_screen()
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
                            User.clear_screen()
                            old_password = getpass.getpass("Enter your old password: ")
                            new_password1 = getpass.getpass("Enter your new password: ")
                            new_password2 = getpass.getpass("Enter your new password again: ")
                            message_update_password = user.update_password(old_password, new_password1, new_password2)
                            print(message_update_password)

                        elif user_login_choice == "4":
                            User.clear_screen()
                            break
                        
                        else:
                            User.clear_screen()            
                            print("\n>>>> Invalid choice <<<<\n")
                            

            else:  
                User.clear_screen()          
                print("\n>>>> Invalid choice <<<<\n")
       
        else: 
            User.clear_screen()           
            print("\n>>>> Invalid choice <<<<\n")
                 
        
if __name__ == "__main__":
    main()
    