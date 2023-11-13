import pandas as pd
import matplotlib.pyplot as plt
from random import randint

df = pd.read_csv("Task3_data.csv")  # import df
pd.set_option('display.max_columns', None)  # set display all columns
pd.options.mode.chained_assignment = None

possible_destinations = df.drop(columns=["Month", "Airline", "Price"])
possible_destinations = possible_destinations.drop_duplicates()
print(possible_destinations)  # print possible destinations
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
}
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

while True:
    destination = input("What destination would you like to go?\n").strip()

    first_letter = destination[0].upper()
    destination = destination[1:]
    destination = f'{first_letter}{destination}'

    if not possible_destinations['Destination'].eq(destination).any():
        print("Invalid destination, try again.")
        continue
    break

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']
for i in months:
    print(i)  # print possible months

while True:
    month = input("In which month?\n").strip()

    first_letter = month[0].upper()
    month = month[1:]
    month = f'{first_letter}{month}'

    if month not in months:
        print("Invalid month, try again.")
        continue
    break

chosen = df[(df['Month'] == month) & (df['Destination'] == destination)]
chosen = chosen.sort_values(by='Price')
print(chosen)

print(f'The lowest price for that specified destination and date range is '
      f'£{chosen["Price"].iloc[0]} '
      f'from {chosen["Airline"].iloc[0]}.'
      f'\nThe average price is £{round(chosen["Price"].mean(), 2)}')
chosen = chosen.drop_duplicates(subset="Airline")
plt.bar(chosen["Airline"], chosen["Price"], label='Price', color='lightcoral')
plt.title(f'Airline prices for {destination} in {month}')
plt.legend()
plt.show()

best_price_month = input("Would you like to see the "
                         "best price for every month? "
                         "(y for yes, n for no)\n").lower().strip()

if best_price_month[0] == "y":
    plt.figure().clear()
    print(possible_destinations)  # print possible destinations

    while True:
        destination = input("What destination would you like to go?\n").strip()

        first_letter = destination[0].upper()
        destination = destination[1:]
        destination = f'{first_letter}{destination}'

        if not possible_destinations['Destination'].eq(destination).any():
            print("Invalid destination, try again.")
            continue
        break

    airline_colors = ['firebrick', 'moccasin', 'salmon', 'mediumseagreen',
                      'royalblue', 'lavender', 'aquamarine', 'red', 'blue', 'purple', 'green']
    best = df[(df['Destination'] == destination)]



    airlines = list(best["Airline"].drop_duplicates())
    airlines_2 = airlines

    for idx, i in enumerate(airlines):
        best = df[(df['Destination'] == destination)]
        best = best.sort_values(by='Price')
        best = best.drop_duplicates(subset='Month')
        best = best.sort_index()
        
        for jidx, j in enumerate(best["Month"]):
            best["Month"].iloc[idx] = months_to_numbers[i]
        best = best.sort_values(by=["Airline", "Month", "Price"])
        for jidx, j in enumerate(best["Month"]):
            best["Month"].iloc[idx] = numbers_to_months[i]
        airlines = list(best["Airline"].drop_duplicates())
        airlines_2 = airlines

        airlines_2.pop(idx)
        best = best[~best['Airline'].str.contains('|'.join(airlines_2))]
        plt.scatter(best["Month"], best["Price"], c=airline_colors[randint(0, len(airline_colors) - 1)])
        plt.plot(best["Month"], best["Price"], color="mediumorchid", label="best")
        plt.legend()
        plt.title(f"price per month for {i}")
        plt.show()
        best = df[(df['Destination'] == destination)]
        airlines_2 = airlines
