import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('train.csv')
data[data['Survived'] == 1].groupby('Sex').size().plot(kind='pie')
plt.show()
