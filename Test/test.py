import pandas as pd

# your original python list of values
values_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

# convert the list to a pandas series
values_series = pd.Series(values_list)

# your new pandas series to replace the values in the original list
new_values = pd.Series([100, 200, 300, 400])

# the minute value at which you want to replace the values
minute_value = 10

# get the index position of the minute value
index_pos = minute_value - 1

# override the values in the original list with the values from the new series
values_list[index_pos:index_pos+len(new_values)] = new_values.values

print(values_list)
