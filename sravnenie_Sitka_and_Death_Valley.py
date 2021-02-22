import csv
from datetime import datetime

from matplotlib import pyplot as plt


def get_weather_data(filename, dates, highs, lows):
    """Получение высоких и низких температур из файла данных."""
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        date_index = header_row.index('DATE')
        high_index = header_row.index('TMAX')
        low_index = header_row.index('TMIN')
        name_index = header_row.index('NAME')

        # dates, highs, lows = [], [], []
        for row in reader:
            try:
                current_date = datetime.strptime(row[date_index], "%Y-%m-%d")
                high = int(row[high_index])
                low = int(row[low_index])
            except ValueError:
                print(current_date, 'missing data')
            else:
                dates.append(current_date)
                highs.append(high)
                lows.append(low)


def get_weather_data_for_death_valley(filename, dates, highs, lows):
    """Получение высоких и низких температур из файла данных."""
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        # dates, highs, lows = [], [], []
        for row in reader:
            try:
                current_date = datetime.strptime(row[2], "%Y-%m-%d")
                high = int(row[4])
                low = int(row[5])
            except ValueError:
                print(current_date, 'missing data')
            else:
                dates.append(current_date)
                highs.append(high)
                lows.append(low)


# Get weather data for Sitka.
plt.style.use('seaborn')
dates, highs, lows = [], [], []
get_weather_data_for_sitka('D://pyy/data/sitka_weather_2018_simple.csv', dates, highs, lows)

# Plot Sitka weather data.
fig = plt.figure(dpi=128, figsize=(10, 6))
plt.plot(dates, highs, c='red', alpha=0.6)
plt.plot(dates, lows, c='blue', alpha=0.6)
plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.15)

# Get Death Valley data.
dates, highs, lows = [], [], []
get_weather_data_for_death_valley('D://pyy/data/death_valley_2018_simple.csv', dates, highs, lows)

# Add Death Valley data to current plot.
plt.plot(dates, highs, c='red', alpha=0.3)
plt.plot(dates, lows, c='blue', alpha=0.3)
plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.05)

# Format plot.
title = "Daily high and low temperatures - 2018"
title += "\nSitka, AK and Death Valley, CA"
plt.title(title, fontsize=20)
plt.xlabel('', fontsize=16)
fig.autofmt_xdate()
plt.ylabel("Temperature (F)", fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.ylim(10, 130)

plt.show()
