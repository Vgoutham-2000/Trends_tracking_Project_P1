from register import *
from login import *
from google.oauth2 import service_account
import os
os.chdir('C:/Users/User/Training/Project_P1/')


def main():
    while True:
        print("\nMain Menu:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            login()
        elif choice == "2":
            username_input = input("Enter the username: ")
            password_input = input("Enter the password: ")
            role_input = input("Enter the role (user/admin): ")
            register(username_input, password_input, role_input)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

  
  

