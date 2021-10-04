import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('Sunspots.csv')


def draw(dataset):
    date = list(dataset.Date)
    series = list(dataset['Monthly_Mean_Total_Sunspot_Number'])
    plt.figure(figsize=(40, 10))
    plt.plot(date, series)
    plt.scatter(date, series)  # график разброса
    # plt.xlim(0, 100)#строит только часть данных: от 0 до 100
    plt.xlabel("Months since Jan 1749.")
    plt.ylabel("No. of Sun spots")
    # plt.show()


def predict(series):
    n = 25
    result = pd.DataFrame(series)
    rolling_mean = result.rolling(window=n).mean()
    plt.plot(rolling_mean, color='r')
    plt.show()


draw(data)
predict(data['Monthly_Mean_Total_Sunspot_Number'])
