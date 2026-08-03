import basicFunctions as bf
import admin
import user
import sys
import os
import pickle
import pyfiglet

def main():
    print("-" * 60)
    print(pyfiglet.figlet_format(">>> Welcome >>>", font = "smslant"))
    while True:
        print("-" * 60)
        print(">>>>>> Home Page >>>>>>".center(60))
        print("1. Admin")
        print("2. User")
        print("3. Exit\n")

        choice = None
        while True:
            choice = bf.get_int("Enter Your Choice(1 to 3): ")
            if 1 <= choice <= 3:
                break

        if choice == 1:
            admin_obj = admin.Admin()
            admin_obj.SignIn()
            while True:
                print("-" * 60)
                print(">>>>>> Admin Page >>>>>>".center(60))
                print("\n1.Search User")
                print("2.View Cars")
                print("3.Edit Car Details")
                print("4.Add car to the Inventory")
                print("5.View All the Customers")
                print("6. Back to Home Page\n")

                admin_choice = bf.get_int("Enter your Choice: ")
                match admin_choice:
                    case 1:
                        print("-" * 60)
                        print("\nSearching for User....\n")
                        admin_obj.search_user()

                    case 2:
                        print("-" * 60)
                        print("\nViewing Car details...\n")
                        admin_obj.view_cars()

                    case 3:
                        print("-" * 60)
                        print("\nEditing Car Details...\n")
                        admin_obj.edit_car_details()
                        print("\nDetails Edited Successfully...\n")

                    case 4:
                        print("-" * 60)
                        print("\nAdding Car to The Inventory...\n")
                        admin_obj.add_car()
                        print("\nCar Added to the Inventory Successfully...\n")

                    case 5:
                        print("-" * 60)
                        print("\nViewing Customers...\n")
                        admin_obj.view_customers()

                    case 6:
                        print("\nGoing Back to Home Page.......\n")
                        print("-" * 80)
                        break

                    case _:
                        print("\nInvalid Choice! Choose a valid option....\n")
                        print("-" * 80)

        elif choice == 2:
            currentUsers = []
            try :
                if os.path.getsize("users.pkl") != 0:
                    with open("users.pkl", "rb") as file:
                        currentUsers = pickle.load(file)
            except FileNotFoundError:
                with open("users.pkl", "wb") as file:
                    pass


            while True:
                user_obj = user.User()
                print("-" * 60)
                print(">>>>>> User Login Page >>>>>>".center(60))
                print("\n1.Sign Up")
                print("2.Sign In")
                print("3.HomePage")

                user_choice = None
                while True:
                    user_choice = bf.get_int("Enter Your Choice: ")
                    if 1 <= user_choice <= 3:
                        break
                    print("Invalid Choice")
                found = None

                if user_choice == 1:
                    user_obj.create_account()
                elif user_choice == 2:
                    user_obj.signIn()
                    found = False

                    for obj in currentUsers:
                        if obj.userName == user_obj.userName:
                            user_obj = obj
                            found = True

                    if found == False:
                        currentUsers.append(user_obj)
                elif user_choice == 3:
                    break

                while True:
                    print("-" * 60)
                    print(">>>>>> User Page >>>>>>".center(60))
                    print("\n1.View Profile")
                    print("2.Book Car")
                    print("3.Calculate Bill")
                    print("4.Login Page")

                    option = bf.get_int("Enter Your Option: ")

                    match option:
                        case 1:
                            print("-" * 60)
                            print("\nViewing Profile....\n")
                            user_obj.view_profile()

                        case 2:
                            print("-" * 60)
                            print("\nBooking Car....\n")
                            user_obj.book_car()

                        case 3:
                            print("-" * 60)
                            print("\nCalculating all the Bills....\n")
                            user_obj.calculate_bill()
                        case 4:
                            print("\nMoving To User Login Page....\n")
                            break

                        case _:
                            print("\nInvalid choice! Choose a Valid Option....\n")
                            print("-" * 60)


                with open("users.pkl","wb") as file:
                    pickle.dump(currentUsers, file)


        elif choice == 3:
            print(pyfiglet.figlet_format("\nThank You.....", font = "smslant"))
            sys.exit()


main()

