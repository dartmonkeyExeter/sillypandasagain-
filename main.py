import pandas as pd
import matplotlib.pyplot as plt
from random import randint

df = pd.read_csv("Task3_data.csv")  # import df
pd.set_option('display.max_columns', None)  # set display all columns
pd.options.mode.chained_assignment = None  # set chained assignment to none, this stops a warn earlier that we can ignore
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
possible_destinations = df.drop(columns=["Month", "Airline", "Price"])  # drop everything but destination
possible_destinations = possible_destinations.drop_duplicates()  # drop duplicates, so only 1 of each destination
print(possible_destinations)  # print possible destinations

while True:
    destination = input("What destination would you like to go?\n").strip()

    first_letter = destination[0].upper()  # get the first letter and set it to uppercase
    destination = destination[1:]  # remove first letter from original string
    destination = f'{first_letter}{destination}'  # add the first letter string and destination to get formatted input

    if not possible_destinations['Destination'].eq(destination).any():  # if it is not found in destinations column
        print("Invalid destination, try again.")
        continue
    break

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']  # initialize list with months of year
for i in months:  # for every month in months
    print(i)  # print possible months

while True:
    month = input("In which month?\n").strip()

    first_letter = month[0].upper()  # formatting once again
    month = month[1:]
    month = f'{first_letter}{month}'

    if month not in months:  # if input not valid, return to top of loop
        print("Invalid month, try again.")
        continue
    break  # if reached, no errors found in month name, break loop.

chosen = df[(df['Month'] == month) & (df['Destination'] == destination)]  # remove all unchosen destinations from list
chosen = chosen.sort_values(by='Price')  # sort by price
print(chosen)  # print all the prices and their respective airline.

print(f'The lowest price for that specified destination and date range is '
      f'£{chosen["Price"].iloc[0]} '
      f'from {chosen["Airline"].iloc[0]}.'
      f'\nThe average price is £{round(chosen["Price"].mean(), 2)}')  # print the lowest price, its airline and the mean
# price

chosen = chosen.drop_duplicates(subset="Airline")  # since sorted by price, will only drop the duplicate airlines,
# which are higher than their respective lowest price
plt.bar(chosen["Airline"], chosen["Price"], label='Price', color='lightcoral')  # plot the airline by the price,
plt.title(f'Airline prices for {destination} in {month}')  # add title to graph
plt.legend()  # add legend to graph
plt.show()  # show

while True:
    best_price_month = input("Would you like to see the "
                             "best price for every month? "
                             "(y for yes, n for no)\n").lower().strip()

    if best_price_month[0] == "y":  # only looks at first char of string
        plt.figure().clear()  # clears figure of previous chart
        print(possible_destinations)  # print possible destinations

        while True:
            destination = input("What destination would you like to go?\n").strip()

            first_letter = destination[0].upper()  # formatting once again
            destination = destination[1:]
            destination = f'{first_letter}{destination}'

            if not possible_destinations['Destination'].eq(destination).any():  # input protection
                print("Invalid destination, try again.")
                continue
            break

        airline_colors = ['firebrick', 'moccasin', 'salmon', 'mediumseagreen',
                          'royalblue', 'lavender', 'aquamarine', 'red', 'blue', 'purple', 'green']  # establish list
        # with various python colors in to be used later
        best = df[(df['Destination'] == destination)]  # set best to the chosen destination

        for idx, i in enumerate(best["Month"]):  # for every index, month in the months column
            best["Month"].iloc[idx] = months_to_numbers[i]  # set that month to number
        best = best.sort_values(by=["Airline", "Month", "Price"])  # sort values based on airline, month then price.
        for idx, i in enumerate(best["Month"]):
            best["Month"].iloc[idx] = numbers_to_months[i]

        airlines = list(best["Airline"].drop_duplicates())  # set airlines list to any airlines found with chosen
        # destination
        airlines_copy = airlines  # create copy of airlines list

        best_copy = best  # create copy of best dataframe

        for idx, i in enumerate(airlines):
            best = df[(df['Destination'] == destination)]  # reset best at start of every loop
            best = best.sort_values(by='Price')  # sort by price
            best = best.drop_duplicates(subset='Month')  # drop duplicate months
            best = best.sort_index()  # sorts by the index, which ends up sorting by the months since that is how the
            # df is originally sorted

            try:
                airlines.pop(idx)  # get rid of current thing from airlines, to be used for scatter
            except IndexError:
                break  # no more airlines left
            plt.plot(best["Month"], best["Price"], color="mediumorchid", label="best")  # plot the best line
            best = best_copy[(best_copy["Airline"] == i)]  # set best to its copy, with only current airline in the
            # dataframe
            plt.scatter(best["Month"], best["Price"], c=airline_colors[randint(0, len(airline_colors) - 1)])
            # plot a scatter graph with every price per month for the specific airline, with a random color.

            plt.legend()
            plt.title(f"price per month for {destination} from {i}")
            plt.show()

            airlines = airlines_copy
        break
    elif best_price_month[0] == "n":
        break
    else:
        print("invalid input, try again.")
        continue

print("and finally, presenting the correlation between the first letter of the destination, the first letter of the "
      "destination and amount of flights!")
dest = []
mont = []

for idx, i in enumerate(df["Destination"]):
    if str(df["Destination"].iloc[idx])[0] == str(df["Month"].iloc[idx])[0]:
        dest.append(f'{str(df["Destination"].iloc[idx])}')
        mont.append(f'{str(df["Month"].iloc[idx])}')

dest.sort()
mont.sort()
