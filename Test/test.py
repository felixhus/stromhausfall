import numpy as np
import pandas as pd

# create the first dataframe with one day in one-minute steps
start = pd.Timestamp('2023-06-01').date()
end = pd.Timestamp('2023-06-02')
index = pd.date_range(start=start, periods=1440, freq='1T')
df1 = pd.DataFrame(index=index)

# create the second dataframe with values at different minutes
df2 = pd.DataFrame({'value': [1, 2, 3]}, index=[
    pd.Timestamp('2023-06-01 00:02:00'),
    pd.Timestamp('2023-06-01 00:05:00'),
    pd.Timestamp('2023-06-01 00:10:00')
])

# merge the two dataframes and fill missing values with zeros
df = pd.merge(df1, df2, how='left', left_index=True, right_index=True)
df['value'] = df['value'].fillna(0)

# print the resulting dataframe
print(df)
