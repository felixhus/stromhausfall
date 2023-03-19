import random
import sqlite3

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate


def generate_time_series(power, timesteps, number_steps):
    f_inter = interpolate.interp1d(timesteps, power, kind='previous')

    x_new = np.linspace(0, number_steps, num=number_steps, endpoint=True)
    y_new = f_inter(x_new)
    return x_new, y_new


def write_to_database(database, values, series_id):
    # connect to the database
    conn = sqlite3.connect('database_profiles.db')
    c = conn.cursor()
    values = values.tolist()

    # Build the SQL query to insert the row
    query = f"INSERT INTO load_profiles_day (series_id, {' ,'.join([f'step_{i}' for i in range(1440)])}) VALUES (?, {'?,'*1439}?)"

    # Execute the query with the values
    c.execute(query, [series_id] + values)

    # commit changes and close connection
    conn.commit()
    conn.close()


P = np.array([0, 1000, 0, 1500, 1000, 500, 0, 0])
t = np.array([0, 120, 240, 480, 540, 600, 720, 1440])
x, y = generate_time_series(P, t, 24*60)
write_to_database(None, y, 'testreihe')
