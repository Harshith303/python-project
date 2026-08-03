#basicFunction.py
import re
import datetime

def show_details(car):
    print("Car ID      :", car["Car ID"])
    print("Brand       :", car["Brand"])
    print("Name        :", car["Name"])
    print("Model       :", car["Model"])
    print("Rent Per Day:", car["Rent"])
    return None

def get_date(prompt):
    while True:
        try:
            day, month, year = map(int, input(prompt).split("/"))
            date = datetime.date(year, month, day)
            if date < datetime.date.today():
                raise ValueError("Invalid Date")
            return date
        except ValueError as e:
            print(e)
        except Exception as e:
            print("Invalid Format of Date! Enter in shown format.")

def get_int(prompt):
    while True:
        try:
            num = int(input(prompt))
            return num
        except ValueError:
            pass


def get_string(prompt):
    while True:
        try:
            string = input(prompt)
            if not string:
                raise Exception()
            return string
        except Exception as e :
            pass


def valid_account(account):
    expression = r"^\w+@rentnride.cars"
    if re.match(expression, account):
        return True
    else:
        return False

def valid_password(password):
    if len(password) == 8 and len(re.findall('[a-zA-Z]', password)) == 5 and len(re.findall('[0-9]', password)) == 2 and len(re.findall('[!@#$*]', password)) == 1:
        return True
    else:
        return False



