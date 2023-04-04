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


# P = np.array([96.5,86.3, 76.9,68.8,62.4,58.0,55.3,53.6,52.4,51.3,50.3,49.2,48.3,47.5,46.9,46.5,46.6,47.1,48.0,49.3,50.8,52.7,55.6,60.5,68.2,79.2,92.0,104.7,115.7,123.5,128.6,132.0,134.8,137.8,140.7,143.2,144.8,145.3,144.9,143.8,142.3,140.8,139.5,138.5,138.2,138.6,140.1,142.6,146.5,151.5,156.7,160.7,162.3,160.5,156.1,150.2,144.0,138.4,133.6,129.4,125.7,122.4,119.6,117.4,115.7,114.6,114.2,114.6,115.7,117.6,120.3,123.9,128.2,133.2,138.9,145.1,151.5,157.9,163.8,168.3,170.6,170.4,168.3,165.3,162.3,160.1,158.4,156.8,154.8,151.9,147.9,142.5,135.7,127.2,117.5,107.1,96.5])
# t = np.linspace(0, 1440, 97)
# x, y = generate_time_series(P, t, 24*60)
# write_to_database(None, y, 'vdew_test_cubic')

lon, lat, city = sql_modules.get_coordinates(33334, 'database_pv.db')

print(lon)
print(lat)
print(city)
