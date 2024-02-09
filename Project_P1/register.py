from google.cloud import bigquery
import json
from google.oauth2 import service_account
import os
os.chdir('C:/Users/User/Training/Project_P1/')


# Load your GCP credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file('gcp_con.json')
project_id ='theta-cell-406519'
client = bigquery.Client(credentials= credentials,project=project_id)


# Set your dataset name
dataset_name = 'goutham_rev_trends'

def register(username, password, role):
    try:
        query = f"INSERT INTO `{project_id}.{dataset_name}.users` (username, password, role) VALUES ('{username}', '{password}', '{role}')"
        client.query(query)
        print("Registration successful!")
    except Exception as e:
        print(f"Error: {e}")

def login():
    username = input("Enter the username: ")
    password = input("Enter the password: ")

    try:
        query = f"SELECT * FROM `{project_id}.{dataset_name}.users` WHERE username = '{username}' AND password = '{password}'"
        query_job = client.query(query)
        user_rows = list(query_job)

        if user_rows:
            user = user_rows[0]
            print(f"Login successful! Welcome, {user['username']} (Role: {user['role']})")
        else:
            print("Invalid username or password")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    username_input = input("Enter the username: ")
    password_input = input("Enter the password: ")
    role_input = input("Enter the role (user/admin): ")

    register(username_input, password_input, role_input)
    login()

