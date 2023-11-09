import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Task3_data.csv")  # import df
pd.set_option('display.max_columns', None)  # set display all columns

possible_destinations = df.drop(columns=["Month", "Airline", "Price"])
possible_destinations = possible_destinations.drop_duplicates()
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

    best = df[(df['Destination'] == destination)]
    best = best.sort_values(by='Price')
    best = best.drop_duplicates(subset='Month')
    best = best.sort_index()
    plt.plot(best["Month"], best["Price"],color="mediumorchid",label="best")
    plt.title(f'Airline prices for {destination} over the year.')
    plt.legend()

    airline_colors = ['firebrick', 'moccasin', 'salmon', 'mediumseagreen',
                       'royalblue', 'lavender']

    best = df[(df['Destination'] == destination)]
    best = best.sort_values(by="Airline")
    airlines = best["Airline"]
    for idx, col in enumerate(airlines):
        Airline = airlines.iloc[idx]
        print(Airline)
        current_color = idx
        best = best.drop()
        plt.scatter(best["Price"],)


    plt.show()
