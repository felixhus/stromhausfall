import matplotlib.pyplot as plt
import pandas as pd
import sql_modules

import source.sql_modules as sql_modules

path = r"C:\Users\felix\Documents\HOME\Uni\02_Master\05_Masterthesis\03_Daten\Tracebase Profiles\complete\Cookingstove\dev_D33097_2012.01.10.csv"
database = r"C:\Users\felix\Documents\HOME\Uni\02_Master\05_Masterthesis\02_Code\05_PowerHouse\source\database_profiles.db"

# read in the CSV file as a DataFrame
df = pd.read_csv(path, header=None, delimiter=";", names=["datetime", "value1", "value2"])

# convert the first column to a datetime object
df["datetime"] = pd.to_datetime(df.iloc[:,0])

# set the datetime column as the index
df.set_index("datetime", inplace=True)

# resample the DataFrame to one-minute intervals
df_resampled = df.resample('1T').mean()
if len(df_resampled['value1']) != 1440:
    print("Not the right length: " + path)
else:
    sql_modules.write_to_database(database, df_resampled['value1'], "stove_2")
    plt.plot(df_resampled)
    plt.show()
