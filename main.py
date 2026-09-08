from datetime import datetime, date
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

class Package(BaseModel):
    id: int
    # sender: User
    # recipient: User
    category: str
    departure_date: date
    arrival_date: date
    weight: float
    status: str


def create_package(package: Package):
    global list_of_packages
    if package.id in list_of_packages:
        print("Package already exists")
        return
    else:
        list_of_packages[package.id] = package
        print("Package created")
        return

def get_package_by_id(package_id: int):
    global list_of_packages
    if package_id in list_of_packages:
        return list_of_packages[package_id]
    else:
        print("Package not found")
        return

def get_all_packages():
    global list_of_packages

    formated_list = []

    for package in list_of_packages.values():
        formated_list.append(package)
    return formated_list

def get_package_status(package_id: int):
    global list_of_packages
    if package_id in list_of_packages:
        return list_of_packages[package_id].status
    else:
        print("Package not found")
        return None


list_of_packages = {}

while True:
    print("Available choices:\n0 - quit\n1 - create package\n2 - get package by id\n3 - get all packages\n4 - get package status")
    user_choice = input("Select your choice: ")
    match user_choice:
        case "0":
            break
        case "1":
            print("Enter package information")
            package_id = len(list_of_packages) + 1
            # sender = input("Enter sender id: ")
            # recipient = input("Enter recipient id: ")
            category = input("Enter category: ")
            departure_date = datetime.now().date()
            arrival_date = datetime.strptime(input("Enter departure date (YYYY-MM-DD): "), "%Y-%m-%d")
            weight = float(input("Enter weight: "))
            status = "Package at the drop-off point"

            package = Package(id=package_id, category=category, departure_date=departure_date,
                              arrival_date=arrival_date, weight=weight, status=status)
            create_package(package)
        case "2":
            package_id = int(input("Enter package ID: "))
            print(get_package_by_id(package_id))
        case "3":
            print(get_all_packages())
        case "4":
            package_id = int(input("Enter package ID: "))
            print(get_package_status(package_id))
        case _:
            print("Invalid choice")

