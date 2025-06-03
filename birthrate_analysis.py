import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("/content/births.csv")

df.head()

df.tail()

df.columns

df.info()

df.head()

df["day"] < 0

df["day"].dtype

df.isnull()

df.isna()

# df["day"] = df["day"].fillna(0, inplace=True)
# df["day"] = df["day"].astype(int)

df.head()

df["decade"] = 10 * (df["year"]//10)
df.pivot_table(df, index='decade', columns='gender', aggfunc='sum')
df.head()

sns.set()
b_decades = df.pivot_table(df,index="decade", columns="gender", aggfunc="sum")
b_decades.plot()
plt.ylabel("Total Birth per Year")
plt.show()

quartiles = np.percentile(df["births"],[25,50,75])
mean = quartiles[1]
sigma = 0.74 * (quartiles[2]-quartiles[0])

births = df.query('(births > @mean - 5 * @sigma) & (births < @mean + 5 * @sigma)')
births.index = pd.to_datetime(10000 * births.year + 100 * births.month + births.day,
                              format='%Y%m%d')
births['day of week'] = births.index.dayofweek

# # Remove outliers using boolean indexing instead of .query()
# lower_bound = mean - 5 * sigma
# upper_bound = mean + 5 * sigma
# births = df[(df['births'] > lower_bound) & (df['births'] < upper_bound)]

# # Create a datetime index using pd.to_datetime with a dictionary
# births['date'] = pd.to_datetime(dict(year=births.year, month=births.month, day=births.day))
# births.set_index('date', inplace=True)

# # Add day of week
# births['day of week'] = births.index.dayofweek

births_day = births.pivot_table('births', index='day of week',
                                columns='decade', aggfunc='mean')
births_day.index = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
births_day.plot()
plt.ylabel("Average Births by Day")
plt.show()

births_month = births.pivot_table('births', [births.index.month, births.index.day])
print(births_month.head())

births_month.index = [pd.Timestamp(2012, month, day)
                      for (month, day) in births_month.index]
print(births_month.head())

fig, ax = plt.subplots(figsize=(12,4))
births_month.plot(ax=ax)
plt.show()

