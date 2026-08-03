#admin.py
import pandas
import user
import os
import json
import basicFunctions as bf

class CarManager:
    cars = []

    @classmethod
    def LoadFromFile(cls):
        CarManager.cars = []
        with open("cars.csv", "r") as file:
            items = file.readlines()

        for i in range(1, len(items)):
            car = dict()
            carId, brand, name, model, rent, availability = items[i].strip().split(",")
            car["Car ID"] = carId
            car["Brand"] = brand
            car["Name"] = name
            car["Model"] = int(model)
            car["Rent"] = int(rent)
            car["Availability Status"] = availability
            CarManager.cars.append(car)

    @classmethod
    def WriteToFile(cls):
        os.remove("cars.csv")
        with open("cars.csv", "a") as file:
            file.write("Car ID,Brand,Name,Model,RentPerDay,AvailabilityStatus\n")
            for car in CarManager.cars:
                file.write(f"{car["Car ID"]},{car["Brand"]},{car["Name"]},{car["Model"]},{car["Rent"]},{car["Availability Status"]}\n")

class Admin:
    def __init__(self):
        self.password = "RentNRide@123"

    def SignIn(self):
        while True:
            try:
                password = input("Enter Password: ")
                if password == self.password:
                    return True
            except Exception as e:
                print("Wrong Password! Try again.")

    def search_user(self):
        while True:
            try:
                if len(user.User.user_names) == 0:
                    print("Currently There are no users")
                    return None
                userName = input("UserName: ")
                if userName in user.User.user_names:
                    break
                else:
                    raise Exception("Invlid Username! Try Again.")
            except Exception as e:
                print("Error:", e)


        with open("dates.json","r") as file:
            data = json.load(file)
        length = 0
        if userName in data.keys():
            length = len(data[userName]["Car ID"])

        if length == 0:
            print("\nNo Bookings Found...\n")
            return

        index = None
        for i in range(len(data.keys())):
            if str(list(data.keys())[i]) == userName:
                index = i

        print("\n-----User Profile-----")
        print("Account ID:", user.User.user_accounts[index])
        print("Username:", user.User.user_names[index])
        print("Booking History: ")
        print(pandas.DataFrame(data[userName]))
        print("\nTotal Bookings:", length)

        print("-" * 60)

    def view_cars(self):
        print("Cars in Inventory\n".center(60))
        data = pandas.read_csv("cars.csv")
        print(data)

    def edit_car_details(self):
        CarManager.LoadFromFile()

        print("1. Brand")
        print("2. Name")
        print("3. Model")
        print("4. RentPerDay")

        option = None
        while True:
            option = bf.get_int("Enter Your Option: ")
            if 1 <= option <= 4:
                break
            print("Invalid Choice")

        while True:
            try:
                car_id = bf.get_string("Car ID: ")
                flag = 0
                for car in CarManager.cars:
                    if car_id == car["Car ID"]:
                        if option == 1:
                            car["Brand"] = bf.get_string("New Brand: ")
                        elif option == 2:
                            car["Name"] = bf.get_string("New Name: ")
                        elif option == 3:
                            car["Model"] = bf.get_int("Model: ")
                        elif option == 4:
                            car["Rent"] = bf.get_int("New RentPerDay: ")

                        flag = 1
                        break
                if flag == 0:
                    raise Exception("Invalid Car ID")
                break

            except Exception as e:
                print("Error:", e)

        CarManager.WriteToFile()
        return True


    def add_car(self):
        CarManager.LoadFromFile()

        car = {"Car ID" : bf.get_string("Car ID: "),
               "Brand" : bf.get_string("Brand: "),
               "Name" : bf.get_string("Name: "),
               "Model" : bf.get_int("Model: ") ,
               "Rent" : bf.get_int("RentPerDay: "),
               "Availability Status" : "Yes"}

        CarManager.cars.append(car)

        CarManager.WriteToFile()

    def view_customers(self):
        try:
            if 0 <= os.path.getsize("users.csv") <= len("Account Name,Username,Password"):
                if os.path.getsize("users.csv") == 0:
                    with open("users.csv", "w") as file:
                        file.write("Account Name,Username,Password")
                print("Currently there are no Users")
                return None
        except FileNotFoundError:
            with open("users.csv", "w") as file:
                file.write("Account Name,Username,Password")
            print("Currently there are no Users")
            return None

        with open("users.csv", "r") as file:
            data = pandas.read_csv(file)

        data = data.drop("Password", axis = 1)
        print(data)



