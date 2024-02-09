from google.cloud import bigquery
from google.oauth2 import service_account
import json
from tabulate import tabulate
import pandas as pd

# Load your GCP credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file('gcp_con.json')
project_id ='theta-cell-406519'
client = bigquery.Client(credentials= credentials,project=project_id)



# Set your dataset name
dataset_name = 'goutham_rev_trends'

def view_all_user_data():
    query = "SELECT id, username, role FROM `goutham_rev_trends.users`"
    result = client.query(query).result()

    # Convert the result to a list of dictionaries
    result_list = [dict(row.items()) for row in result]

    if not result_list:
        print("No data")
    else:
        headers = result_list[0].keys()
        data_tuples = [(row['id'], row['username'], row['role']) for row in result_list]
        print(tabulate(data_tuples, headers=headers, tablefmt="pretty"))

def user_exists(data_id):
    # Check if the user with the specified data_id exists in the table
    query = f"SELECT COUNT(*) FROM `goutham_rev_trends.users` WHERE id = {data_id}"
    result = client.query(query).result()
    count = next(result)[0]
    return count > 0

def insert_new_data():
    query=f"SELECT COUNT(*) AS row_count from goutham_rev_trends.users;"
    query_job=client.query(query)
    df=query_job.to_dataframe()
    id=df['row_count'][0]
    id+=1
    # Get user input for new data
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    role = input("Enter the role: ")

    # Execute an INSERT query to add new data to the BigQuery table
    query = f"INSERT INTO `goutham_rev_trends.users` (id,username, password, role) VALUES ({id},'{username}', '{password}', '{role}')"
    client.query(query)

    print(f"User '{username}' created successfully by admin.")

def update_data():
    # Get user input for data to be updated
    data_id = int(input("Enter data_id to update: "))
    
    # Get user input for the new values
    new_username = input("Enter new username: ")
    new_role = input("Enter new role: ")
    if user_exists(data_id):
    # Execute an UPDATE query to modify the specified data in the BigQuery table
        query = f"UPDATE `goutham_rev_trends.users` SET username = '{new_username}', role = '{new_role}' WHERE id = {data_id}"
        client.query(query)
        print(f"Data with id {data_id} updated successfully.")
    else:
        print(f"User with id {data_id} does not exist.")

from google.cloud import bigquery



def delete_data():
    # Get user input for data to be deleted
    data_id = int(input("Enter data_id to delete: "))
    
    # Check if the user exists before attempting to delete
    if user_exists(data_id):
        # Execute a DELETE query to remove the specified data from the BigQuery table
        delete_query = f"DELETE FROM `goutham_rev_trends.users` WHERE id = {data_id}"
        client.query(delete_query)

        print(f"Data with id {data_id} deleted successfully.")
    else:
        print(f"User with id {data_id} does not exist.")


def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. View all user data")
        print("2. Insert new data")
        print("3. Update data")
        print("4. Delete data")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_all_user_data()
        elif choice == "2":
            insert_new_data()
        elif choice == "3":
            update_data()
        elif choice == "4":
            delete_data()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    admin_menu()
