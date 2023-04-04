import random
import sqlite3
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


# Path('database_pv.db').touch()
conn = sqlite3.connect('database_pv.db')
c = conn.cursor()
c.execute('''CREATE TABLE plz_data (loc_id int, postcode int, lon real, lat real, city text)''')
plz = pd.read_csv('plz_coordinates.csv')
# write the data to a sqlite table
plz.to_sql('plz_data', conn, if_exists='append', index=False)
c.close()

lon, lat, city = sql_modules.get_coordinates(33334, 'database_pv.db')

print(lon)
print(lat)
print(city)
