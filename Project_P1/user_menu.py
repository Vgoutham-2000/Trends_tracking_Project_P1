from google.cloud import bigquery
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
from google.oauth2 import service_account
# Load your GCP credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file('gcp_con.json')
project_id ='theta-cell-406519'
client = bigquery.Client(credentials= credentials,project=project_id)


# Set your dataset name
dataset_name = 'goutham_rev_trends'


def view_all_data():
    query = "SELECT * FROM `{}.{}.{}`".format(project_id, dataset_name, 'main_table')
    df = client.query(query).to_dataframe()

    if df.empty:
        print("No data")
    else:
        print(tabulate(df, headers='keys', tablefmt='pretty'))



def user_menu():
    while True:
        print("\n User menu")
        print("1. View overall main table")
        print("2. Bar plot for Categories")
        print("3. Distribution of Posts by Country")
        print("4. Retweets and Likes Over Hours")
        print("5. Sentiment vs. Likes")
        print("6. Exit")

        choice = input("Enter the choice: ")

        if choice == "1":
            view_all_data()

        elif choice == "2":
            # Example 1: Bar plot for Categories
            query = """
            SELECT main.Categories_id, categories.categories, COUNT(*) as count
            FROM `{}.{}.{}` as main
            JOIN `{}.{}.{}` as categories
            ON main.Categories_id = categories.categories_id
            GROUP BY 1, 2
            """.format(project_id, dataset_name, 'main_table', project_id, dataset_name, 'categories')

            df = client.query(query).to_dataframe()
    
            if not df.empty:
                plt.bar(df['categories'], df['count'])
                plt.title('Number of Posts in Each Category')
                plt.xlabel('Categories')
                plt.ylabel('Count')
                plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
                plt.show()
            else:
                print("No data to display.")



        elif choice == "3":
            # Example 2: Pie chart for Country distribution
            query = """
            SELECT country.country, COUNT(*) as count
            FROM `{}.{}.{}` as main
            JOIN `{}.{}.{}` as country
            ON main.Country_id = country.country_id
            GROUP BY 1
            """.format(project_id, dataset_name, 'main_table', project_id, dataset_name, 'country')

            df = client.query(query).to_dataframe()

            if not df.empty:
                df.set_index('country')['count'].plot.pie(autopct='%1.1f%%', startangle=90)
                plt.title('Distribution of Posts by Country')
                plt.show()
            else:
                print("No data to display.")





        elif choice == "4":
            # Example 3: Line plot for Retweets and Likes
            query = "SELECT Country_id, SUM(Likes) as Likes FROM `{}.{}.{}` GROUP BY Country_id".format(project_id, dataset_name, 'main_table')
            df = client.query(query).to_dataframe()
            # plt.bar(df['Country_id'], df['Retweets'], label='Retweets')
            plt.bar(df['Country_id'], df['Likes'], label='Likes')
            plt.title('Likes Over Country')
            plt.legend()
            plt.show()

        elif choice == "5":
            # Example 4: Scatter plot for Sentiment vs. Likes
            query = "SELECT Sentiment_id, AVG(Likes) as AvgLikes FROM `{}.{}.{}` GROUP BY Sentiment_id".format(project_id, dataset_name, 'main_table')
            df = client.query(query).to_dataframe()
            plt.scatter(df['Sentiment_id'], df['AvgLikes'])
            plt.title('Sentiment vs. Likes')
            plt.show()

        elif choice=="6":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    user_menu()
