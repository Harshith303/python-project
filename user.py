#user.py
import basicFunctions as bf
import pandas
import admin
import json
import os
import datetime

class User:
    users_list = dict()
    try :
        if os.path.getsize("dates.json") == 0:
            with open("dates.json", "w") as file:
                json.dump(users_list, file)
        else:
            with open("dates.json", "r") as file:
                users_list = json.load(file)

    except FileNotFoundError:
        with open("dates.json", "w") as file:
            json.dump(users_list, file)

    def __init__(self):
        self.accountName = None
        self.userName = None
        self.password = None
        self.booking_date = None
        self.selected_car = None
        self.returning_date = None

    try:
        if 0 <= os.path.getsize("users.csv") <= len("Account Name,Username,Password"):
            if os.path.getsize("users.csv") == 0:
                with open("users.csv", "w") as file:
                    file.write("Account Name,Username,Password\n")
    except FileNotFoundError:
        with open("users.csv", "w") as file:
            file.write("Account Name,Username,Password\n")

    with open("users.csv", "r") as file:
        next(file)
        user_accounts = []
        user_names = []
        passwords = []
        for line in file:
            account, userName, passWord = line.strip().split(",")
            user_accounts.append(account.strip())
            user_names.append(userName.strip())
            passwords.append(passWord.strip())


    def create_account(self):
        while True:
            try:
                print("Sample Account Name: username@rentnride.cars")
                account_name = input("Account Name: ")
                if account_name in User.user_accounts:
                    raise Exception("Account Already Exists")
                if bf.valid_account(account_name):
                    self.accountName = account_name
                    User.user_accounts.append(account_name)
                    break
                else:
                    raise Exception("Invalid Account Name")
            except Exception as e:
                print("\nError:", e)

        while True:
            try:
                user_name = bf.get_string("User Name: ")
                if user_name in User.user_names:
                    raise Exception("UserName Already Exists")
                else:
                    self.userName = user_name
                    User.user_names.append(user_name)
                    break
            except Exception as e:
                print("\nError:", e)

        print('\n"""')
        print("Password should contain:")
        print("--> 5 Alphabets")
        print("--> 2 digits")
        print("--> 1 special character")
        print('"""\n')
        while True:
            try:
                key = input("Password: ")
                if bf.valid_password(key):
                    self.password = key
                    User.passwords.append(key)
                    break
                else:
                    raise Exception("Invalid PassWord")
            except Exception as e:
                print("Error:", e)

        with open("users.csv", "a") as file:
            file.write(f"{self.accountName},{self.userName},{self.password}\n")


    def signIn(self):
        while True:
            try:
                name = input("UserName: ")
                password = input("Password: ")

                if name in User.user_names:
                    index = User.user_names.index(name)
                    if password == User.passwords[index]:
                        self.userName = name
                        self.password = password
                        self.accountName = User.user_accounts[index]
                        return True
                    else :
                        raise Exception("Wrong Username or password! Try Again")
            except Exception as e:
                print("Login Failed:", e)


    def book_car(self):
        data = pandas.read_csv("cars.csv")
        print(data, end = "\n\n")

        self.booking_date = bf.get_date("Booking Date(DD/MM/YYYY): ")
        self.returning_date = bf.get_date("Returning Date(DD/MM/YYYY)(Expected): ")

        admin.CarManager.LoadFromFile()

        while True:
            flag = 0
            car_id = input("Car ID: ")
            for car in admin.CarManager.cars:
                if car_id == car["Car ID"] and car["Availability Status"] == "Yes":
                    self.selected_car = car
                    print("\nBooking Completed Successfully\n")
                    print("----Booking details----")
                    bf.show_details(self.selected_car)
                    print("-" * 23)
                    car["Availability Status"] = "No"
                    flag = 1
                    break
            if flag == 1:
                break
            else:
                print("Car Is Not Available")

        admin.CarManager.WriteToFile()

        with open("dates.json", "r") as file:
            User.users_list = json.load(file)

        if self.userName not in User.users_list.keys():
            User.users_list.update({self.userName : dict()})
            User.users_list[self.userName].update({"Booking Dates" : []})
            User.users_list[self.userName].update({"Returning Dates" : []})
            User.users_list[self.userName].update({"Car ID": []})
            User.users_list[self.userName].update({"Payment Status": []})
        copy_booking, copy_returning = str(self.booking_date), str(self.returning_date)
        User.users_list[self.userName]["Booking Dates"].append(str(copy_booking))
        User.users_list[self.userName]["Car ID"].append(str(self.selected_car["Car ID"]))
        User.users_list[self.userName]["Returning Dates"].append(str(copy_returning))
        User.users_list[self.userName]["Payment Status"].append("No")

        with open("dates.json", "w") as file:
            json.dump(User.users_list, file)


    def calculate_bill(self):

        if self.userName not in User.users_list:
            print("No Bookings Found")
            return

        admin.CarManager.LoadFromFile()

        found = False

        for i in range(len(User.users_list[self.userName]["Payment Status"])):

            if User.users_list[self.userName]["Payment Status"][i] == "No":

                found = True

                self.booking_date = datetime.datetime.strptime(User.users_list[self.userName]["Booking Dates"][i],"%Y-%m-%d").date()
                self.returning_date = datetime.datetime.strptime(User.users_list[self.userName]["Returning Dates"][i],"%Y-%m-%d").date()

                car_id = User.users_list[self.userName]["Car ID"][i]

                self.selected_car = None

                for car in admin.CarManager.cars:
                    if car["Car ID"] == car_id:
                        self.selected_car = car
                        break

                if self.selected_car is None:
                    continue

                days_rented = (self.returning_date - self.booking_date).days

                days = bf.get_int(f"Extra days for Car ID {car_id}: ")

                if days > 0:
                    days_rented += days
                    self.returning_date += datetime.timedelta(days=days)

                total_bill = (self.selected_car["Rent"] * days_rented)

                print("\n-----Bill-----")

                bf.show_details(self.selected_car)

                print("\nBooking Date     :", self.booking_date)
                print("Returning Date   :", self.returning_date)
                print("No.of Days Rented:", days_rented)
                print("Total Bill       :", total_bill)

                print("----------------\n")

                User.users_list[self.userName]["Payment Status"][i] = "Yes"

                for car in admin.CarManager.cars:
                    if car["Car ID"] == self.selected_car["Car ID"]:
                        car["Availability Status"] = "Yes"
                        break

        if found == False:
            print("No Pending Bills Found")

        with open("dates.json", "w") as file:
            json.dump(User.users_list, file)

        admin.CarManager.WriteToFile()

        return None


    def view_profile(self):

        print("--------Profile--------")
        print("Account ID:", self.accountName)
        print("Username:", self.userName)
        print("Booking History: ")

        with open("dates.json","r") as file:
            data = json.load(file)

        for key in data:
            if key == self.userName:
                print(pandas.DataFrame(data[key]))

        print("-" * 24)

        return None




