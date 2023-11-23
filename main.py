import pandas as pd
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None
months_to_numbers = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}  # initialize dictionaries for conversions, to be used later
numbers_to_months = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


# displays main menu and collects user choice of destination
def menu():
    flag = True

    while flag:
        print("######################################################")
        print("########         Choose a destination          ########")
        print("Alicante (ALC)")
        print("Amsterdam (AMS)")
        print("Athens (ATH)")
        print("Budapest (BUD)")
        print("Cologne (CGN)")
        print("Dublin (DUB)")
        print("Munich (MUC)")
        print("Paris (CDG)")
        print("Rhodes (RHO)")
        print("######################################################")

        # collects and validates user input to ensure choice is in the list
        # converts the collected code to full name

        menu_choice = input("Please enter the three letter "
                            "destination code").upper()

        code_list = ["ALC", "AMS", "ATH", "BUD", "CGN", "DUB", "MUC", "CDG",
                     "RHO"]
        airport_list = ["Alicante", "Amsterdam", "Athens", "Budapest",
                        "Cologne", "Dublin", "Munich", "Paris", "Rhodes"]

        if menu_choice in code_list:
            airport_position = code_list.index(menu_choice)
            return airport_list[airport_position]
        else:
            print("Sorry, you did not enter a valid three letter code")
            flag = True


# collects the month that the user wishes to travel and validates input
def get_date():
    flag = True

    while flag:
        print("######################################################")
        print("When will you be traveling?")
        print("Please enter the number of the month you will be travelling ("
              "1-12)")
        print("for example June = 6")
        print("######################################################")

        month_list = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November",
                      "December"]

        month_choice = input("Please enter the number of your choice (1-12): ")

        try:
            int(month_choice)
        except ValueError:
            print("Sorry, you did not enter a valid choice")
            flag = True
        else:
            if int(month_choice) < 1 or int(month_choice) > 12:
                print("Sorry, you did not enter a valid choice")
                flag = True
            else:
                travel_date = month_list[int(month_choice) - 1]
                return travel_date


destination = menu()
month = get_date()


# gets the main list of data that matches user search criteia and displays it
def get_data():
    df = pd.read_csv("Task4a_data.csv")
    extract = df.loc[(df['Month'] == month) &
                     (df['Destination'] == destination),
                     df.columns != "Commission (%)"]
    print("We have found these flights that match your criteria:")
    return extract


extracted_data = get_data()
extract_no_index = extracted_data.to_string(index=False)


# extracts more meaningful data from the results for comparison
def compare_data():
    compare_df = extracted_data[['Airline', 'Price']]

    column = compare_df['Price']
    max_price = column.max()
    min_price = column.min()

    most_expensive = compare_df.loc[(extracted_data['Price'] == max_price)]
    least_expensive = compare_df.loc[(extracted_data['Price'] == min_price)]

    average_price = round(compare_df['Price'].mean(), 2)

    print("###############################################")
    print(f"The most expensive flights to {destination} in {month} are: ")
    print(most_expensive.to_string(index=False))
    print("")
    print(f"The least expensive flights to {destination} in {month} are: ")
    print(least_expensive.to_string(index=False))
    print("")
    print(f"The average price of a flight to {destination} in {month} is: ")
    print(average_price)
    print("###############################################")

    graph_data = compare_df.sort_values(by="Price")
    graph_data = graph_data.drop_duplicates(subset="Airline")
    plt.bar(graph_data["Airline"], graph_data["Price"], label="graph",
            color="lightcoral")
    plt.title(f'Airline prices for {destination} in {month}')
    plt.legend()
    plt.show()


def flights_per_airline():
    df = pd.read_csv("Task4a_data.csv")
    df = df.groupby('Airline').count()
    df = df.reset_index()
    df = df.rename(columns={'Month': 'Total Flights'})
    plt.bar(df["Airline"], df["Total Flights"])
    plt.title("Flights per Airline")
    plt.show()


def avg_price_per_month():
    df = pd.read_csv("Task4a_data.csv")
    df = df.groupby('Month', sort=False)['Price'].mean()
    df = df.reset_index()
    plt.plot(df["Month"], df["Price"], label="Average Price")
    plt.title("Average Price Per Month For All Destinations")
    plt.legend()
    plt.show()


def avg_price_per_airline():
    df = pd.read_csv("Task4a_data.csv")
    df = df.groupby('Airline', sort=False)['Price'].mean()
    df = df.reset_index()
    plt.pie(df["Price"], labels=df["Airline"].tolist())
    plt.title("Average Price Per Airline")
    plt.legend()
    plt.show()


def low_avg_max_price_per_month_per_dest():
    df = pd.read_csv("Task4a_data.csv")
    df = df[(df["Destination"] == destination)]
    df_max = df[(df["Destination"] == destination)]
    df_min = df[(df["Destination"] == destination)]
    df = df.groupby('Month', sort=False)['Price'].mean()
    df_max = df_max.groupby('Month', sort=False)['Price'].max()
    df_min = df_min.groupby('Month', sort=False)['Price'].min()
    df_max = df_max.reset_index()
    df_min = df_min.reset_index()
    df = df.reset_index()
    plt.plot(df_min["Month"], df_min["Price"], label="Lowest Price", c="red")
    plt.plot(df["Month"], df["Price"], label="Average Price", c="blue")
    plt.plot(df_max["Month"], df_max["Price"], label="Highest Price", c="green")
    plt.title(f"Prices Per Month for {destination}")
    plt.legend()
    plt.show()


def flights_per_month():
    df = pd.read_csv("Task4a_data.csv")
    df = df.groupby('Month', sort=False).count()
    df = df.reset_index()
    df = df.rename(columns={'Airline': 'Total Flights'})
    plt.bar(df["Month"], df["Total Flights"])
    plt.title("Flights per Month")
    plt.show()

def bands():
    df = pd.read_csv("Task4a_data.csv")
    df['Price Bands'] = pd.cut(df['Price'], bins=3, labels=["Good Price", "Average Price", "Bad Price"])
    df = df.groupby('Price Bands')['Price'].count()
    df = df.reset_index()
    print(df)


print(extract_no_index)
compare_data()
#flights_per_airline()
#avg_price_per_month()
#avg_price_per_airline()
#low_avg_max_price_per_month_per_dest()
#flights_per_month()
bands()
