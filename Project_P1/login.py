from google.oauth2 import service_account
from google.cloud import bigquery
import json
from getpass import getpass
from admin_menu import admin_menu
from user_menu import user_menu

# Load your GCP credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file('gcp_con.json')
project_id ='theta-cell-406519'
client = bigquery.Client(credentials= credentials,project=project_id)


# Set your dataset name
dataset_name = 'goutham_rev_trends'

def login():
    username = input("Enter the username: ")
    password = getpass("Enter the password: ")

    try:
        query = f"SELECT * FROM `{project_id}.{dataset_name}.users` WHERE username = '{username}' AND password = '{password}'"
        query_job = client.query(query)
        user_rows = list(query_job)

        if user_rows:
            user = user_rows[0]
            print(f"Login successful! Welcome, {user['username']} (role: {user['role']})")

            if user['role'] == "admin":
                admin_menu()
            else:
                user_menu()
        else:
            print("Invalid username or password")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    login()
