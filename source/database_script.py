import csv
import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sql_modules
from scipy import interpolate


def generate_time_series(power, timesteps, number_steps):
    f_inter = interpolate.interp1d(timesteps, power, kind='cubic')

    x_new = np.linspace(0, number_steps, num=number_steps, endpoint=True)
    y_new = f_inter(x_new)

    plt.plot(timesteps, power, 'o', label='Original')
    plt.plot(x_new, y_new, '.-', label='Interpolated')
    plt.legend()
    plt.show()

    return x_new, y_new


def write_to_database(database, values, series_id):
    # connect to the database
    conn = sqlite3.connect('database_profiles.db')
    c = conn.cursor()
    values = values.tolist()

    # Build the SQL query to insert the row
    query = f"INSERT INTO load_profiles_day (series_id, {' ,'.join([f'step_{i}' for i in range(1440)])}) VALUES (?, {'?,' * 1439}?)"

    # Execute the query with the values
    c.execute(query, [series_id] + values)

    # commit changes and close connection
    conn.commit()
    conn.close()


def izes_csv_to_sqlite():
    p1_csv_path = "C:/Users/felix/Documents/HOME/Uni/02_Master/05_Masterthesis/03_Daten/IZES_Profile/CSV_74_Loadprofiles_1min_W_var/PL1.csv"
    p2_csv_path = "C:/Users/felix/Documents/HOME/Uni/02_Master/05_Masterthesis/03_Daten/IZES_Profile/CSV_74_Loadprofiles_1min_W_var/PL2.csv"
    p3_csv_path = "C:/Users/felix/Documents/HOME/Uni/02_Master/05_Masterthesis/03_Daten/IZES_Profile/CSV_74_Loadprofiles_1min_W_var/PL3.csv"
    Path('database_izes.db').touch()
    conn = sqlite3.connect('database_izes.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE load_1min (date text)''')
    for i in range(1, 75):
        column = "profile_" + str(i)
        cursor.execute(f"ALTER TABLE load_1min ADD {column} int")

    p1_data = pd.read_csv(p1_csv_path, header=None)
    p2_data = pd.read_csv(p2_csv_path, header=None)
    p3_data = pd.read_csv(p3_csv_path, header=None)

    date = datetime(2023, 1, 1)

    for i in range(len(p1_data)):
        # get the corresponding rows from the other dataframes
        row1 = p1_data.iloc[i]
        row2 = p2_data.iloc[i]
        row3 = p3_data.iloc[i]

        # add up the rows elementwise
        row_sum = row1 + row2 + row3

        placeholders = ",".join(["?"] * 74)
        query = f"INSERT INTO load_1min VALUES ({date.strftime('%Y-%m-%d')}, {placeholders})"

        if i % 1000 == 0:
            percent = "%.2f" % (i/525600*100)
            print(f"Wrote {i} rows ({percent}%)")

        cursor.execute(query, tuple(row_sum))
        date = date + timedelta(minutes=1)
        # BESSER: Zwei Spalten, eine mit Tag und eine mit Monat.

    conn.commit()
    conn.close()

izes_csv_to_sqlite()
