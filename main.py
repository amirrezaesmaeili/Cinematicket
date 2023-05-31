from users import User
from cinema import Cinema
import getpass
import argparse
import datetime
import re as regex
import logging

logger = logging.getLogger("UserLogger")
logger.setLevel(level=logging.INFO)

def main():
    User.clear_screen()          
    parser = argparse.ArgumentParser(description="User Login")
    parser.add_argument("-m","--manager", action="store_true", help="Create an admin user")
    parser.add_argument('-u',"--username", type=str, help="Username")
    parser.add_argument('-p',"--password", type=str, help="Password")
    parser.add_argument('-b',"--birthday", type=str, help="birthday")
    args = parser.parse_args()
    logger.info("args entered.")

    if args.manager:
        User.create_manager_from_args(args)
        User.get_manager_details()
        logger.info("if args.manager;  called 2 funcs: create_manager_from_args, get_manager_details")
        
        
    while True:
        # User.clear_screen()
        print("<------Menu------>")
        print("0: Exit program")
        print("1: Manager Panel")
        print("2: User Panel")
        choice = input("\nEnter your choice: ")
        logger.info("while True;  choice entered.")
        
        if choice == "0":
            User.clear_screen()
            logger.info("while True/ if;  Exit program.")
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
                logger.info("while True/ elif 1/ if;  manager's choice entered.")
                
                if manager_choice == "0":
                    User.clear_screen()
                    logger.info("while True/ elif choice 1/ if/ if;  Exit program.")
                    break
                
                elif manager_choice == "1":
                    User.clear_screen()
                    username = input("Enter a username for admin: \n")
                    password = getpass.getpass("Enter a password (at least 4 characters): \n")
                    role = "ADMIN"
                    birth = ""
                    User.sign_up(username, password, role, birth)
                    print("\n>>>> Welcome : Admin created successfully. <<<<\n")
                    logger.info("while True/ elif manager_choice 1;  printed message: Welcome : Admin created successfully.")
                    
                
                elif manager_choice == "2":
                    User.clear_screen()
                    film_name = input("Enter Film Name: \n")
                    film_genre = input("Enter Film Genre: \n")
                    film_play_time = input("Enter Film Playing Time In 00:00 Format: \n")
                    film_age_category = input("Enter Age Category Of The Film: \n")
                    capacity = input("Enter The Cinema Capacity: \n")
                    ticket_price = input("Enter The Ticket Price: \n")
                    message_create_sans = Cinema.create_sans(film_name,film_genre,film_play_time,film_age_category,capacity,ticket_price)
                    print(message_create_sans)
                    logger.info("while True/ elif manager_choice 2;  called create_sans")
                
                elif manager_choice == "3":
                    User.clear_screen()
                    logger.info("while True/ elif manager_choice 3;  Exit program.")
                    break
                    
            else:
                print("You Have No Permissions")

            User.clear_screen()
            logger.info("while True/ elif choice 1/ if args/ else;  printed message: You Have No Permissions")
                
                
        elif choice == "2":
            User.clear_screen()
            print("Menu:")
            print("0: Exit program")
            print("1: Register user")
            print("2: Login user")
            user_choice = input("\nEnter your choice: ")
            logger.info("while True/ elif choice 2;  user's choice entered.")
            
            
            if user_choice == "0":
                User.clear_screen()
                logger.info("while True/ elif choice 2/ if user_choice;  Exit program.")
                break
            
            elif user_choice == "1":
                User.clear_screen()
                username = input("Enter a username: \n")
                password = getpass.getpass("Enter a password (at least 4 characters): \n")

                birth = input("Enter your burthday (yyyy-mm-dd): ")

              
                telephone_number = input("Enter Your Telephone Number In +98 Format: \n")
                pattern = regex.compile(r"^\+98\d{10}$")
                if not pattern.match(telephone_number):
                    raise ValueError("Phone number is invalid.")

                role = "USER"
                User.sign_up(username, password, role, birth, telephone_number)
                print("\n>>>> Welcome : User created successfully. <<<<")
                logger.info("while True/ elif choice 2/ elif user_choice 1;  printed message: Welcome : User created successfully.")
    
            
            elif user_choice == "2":
                User.clear_screen()
                username = input("Enter your username: \n")
                password = User.build_pass(getpass.getpass("Enter your password: \n"))
                User.load_from_database()
                if username in User._users and User._users[username]["password"] == password:
                    user = User(username, User._users[username]["password"], User._users[username]["birthday"],
                     User._users[username]["id"], User._users[username]["submit_date"])
                    logger.info("while True/ elif choice 2/ elif user_choice 2/ if username;  user logged in.")

                    while True:
                        print("User menu:")
                        print("1: View user information")
                        print("2: Edit user information")
                        print("3: Change password")
                        print("4: cinema screenings")
                        print("5: Bank Account")
                        print("6: Logout")
                        user_login_choice = input("Enter your choice: ")
                        logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True;  user's login choice entered.")
                        
                        if user_login_choice == "1":
                            User.clear_screen()
                            print(user)
                            logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ if; user's info printed.")

                        elif user_login_choice == "2":
                            User.clear_screen()
                            print("1: Edit username")
                            print("2: Edit phone number")
                            user_edit_choice = input("Enter choice: ")
                            logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 2; user's edit choice entered.")
                            if user_edit_choice == "1":
                                new_username = input("Enter a new username: ")
                                logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 2/ if; new username entered.")
                                if new_username in User._users:
                                   print("Username already exists.")
                                   logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 2/ if/ if; printed message: Username already exists.")
                                else:
                                   message_update_username = user.update_username(new_username)
                                   print(message_update_username)
                                   logger.info(f"while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 2/ if/ else; printed message: {message_update_username}")
                            elif user_edit_choice == "2":
                                new_telephone_number = input("Enter Your New Telephone Number In +98 Format: ")
                                logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 2/ elif user_edit_choice 2; new telephone number entered.")
                                pattern = regex.compile(r"^\+98\d{10}$")
                                if not pattern.match(new_telephone_number):
                                    logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 2/ elif user_edit_choice 2/ if; raised error: Phone number is invalid.")
                                    raise ValueError("Phone number is invalid.")
                                message_update_telephonenumber = user.update_telephone_number(new_telephone_number)
                                print(message_update_telephonenumber)
                                logger.info(f"while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 2/ elif user_edit_choice 2; printed message: {message_update_telephonenumber}")
                            else:            
                              print("\n>>>> Invalid choice <<<<\n")
                              logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 2/ else; printed message: Invalid choice.")
                                
                        elif user_login_choice == "3":
                            User.clear_screen()
                            old_password = getpass.getpass("Enter your old password: ")
                            new_password1 = getpass.getpass("Enter your new password: ")
                            new_password2 = getpass.getpass("Enter your new password again: ")
                            message_update_password = user.update_password(old_password, new_password1, new_password2)
                            print(message_update_password)
                            logger.info(f"while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 3; printed message: {message_update_password}")

                        elif user_login_choice == "4":
                            print("1: Cinema Sans")
                            print("2: Reserve Sans")
                            user_cinema_choice = input("Enter choice: ")
                            logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 4; user's cinema choice entered.")
                            if user_cinema_choice == "1":
                                sans_list = Cinema.get_all_sans()
                                for sans in sans_list:
                                    print("---------------------------")
                                    print(f"Film ID: {sans['id']}")
                                    print(f"Film Name: {sans['film_name']}")
                                    print(f"Film Genre: {sans['film_genre']}")
                                    print(f"Film Playing Time: {sans['film_play_time']}")
                                    print(f"Age Category: {sans['film_age_category']}")
                                    print(f"Capacity: {sans['capacity']}")
                                    print("---------------------------")
                                logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 4/ if; sans list printed.")
                            elif user_cinema_choice == "2":
                                sans_list = Cinema.get_all_sans()
                                film_name = input("Enter The Film Name For Reserving: ")
                                film_play_time = input("Enter The Film Playing Time: ")
                                logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 4/ elif; film name and film play time entered.")

                                for sans in sans_list:
                                    if sans['film_name'] == film_name and sans['film_play_time'] == film_play_time:
                                        capacity = int(input("Enter the number of seats to reserve: "))
                                        logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 4/ elif/ for/ if; number of seats to reserve entered.")
                                        try:
                                            cinema_sans = Cinema(sans['film_name'], sans['film_genre'], sans['film_play_time'], sans['film_age_category'], sans['capacity'])
                                            can_reserve = cinema_sans.can_reserve_sans(film_play_time, capacity)
                                            if can_reserve:
                                                cinema_sans.capacity = int(cinema_sans.capacity)
                                                capacity = int(capacity)
                                                if capacity <= cinema_sans.capacity:
                                                    cinema_sans.capacity -= capacity
                                                    cinema_sans.save_sans_to_file()
                                                    print(f"\n>>>> Seats reserved successfully. Remaining capacity: {cinema_sans.capacity} <<<<\n")
                                                    logger.info(f"while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 4/ elif/ for/ if/ try/ if/ if capacity;\
                                printed message: Seats reserved successfully. Remaining capacity: {cinema_sans.capacity}.")
                                                else:
                                                    print("\n>>>> Insufficient capacity. <<<<\n")
                                                    logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 4/ elif/ for/ if/ try/ if/ else;\
                                printed message: Insufficient capacity.")
                                        except ValueError as e:
                                            print(str(e))
                                            logger.info(f"while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 4/ elif/ for/ if/ except;  printed message: {e}")
                                        break
                                else:
                                    print("\n>>>> Sans not found. <<<<\n")
                                    logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 4/ elif/ else;  printed message: Sans not found.")

                        elif user_login_choice == "5":
                            logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelif user_login_choice 5; ")
                            ticket_value = User.apply_discount(self, original_price)
                   
                        elif user_login_choice == "6":
                            logger.info("while True/ elif user_login_choice 6;  Exit program.")
                            break
                        
                        else:
                            User.clear_screen()            
                            print("\n>>>> Invalid choice <<<<\n")
                            logger.info("while True/ elif choice 2/ elif user_choice 2/ if username/ while True/ \
                                \nelse;  printed message: Invalid choice")
                            
            
    
            else:  
                User.clear_screen()          
                print("\n>>>> Invalid choice <<<<\n")
                logger.info("while True/ elif choice 2/ else;  printed message: Invalid choice")
       
        else: 
            User.clear_screen()           
            print("\n>>>> Invalid choice <<<<\n")
            logger.info("while True/ else;  printed message: Invalid choice")
                 
        
if __name__ == "__main__":
    main()