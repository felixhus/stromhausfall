import sqlite3

import numpy as np
from scipy import interpolate


def get_load_profile(table_name, key, database):
    conn = sqlite3.connect(database)    # Connect to the database
    cursor = conn.cursor()  # Create a cursor object
    # Select the row of values from the table
    row = cursor.execute(f"SELECT * FROM {table_name} WHERE series_id = ?", (key,)).fetchone()
    row = list(row[1:])  # remove series_id and convert to a list
    # Close the cursor and database connection
    cursor.close()
    conn.close()
    return row


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


def generate_time_series(power, timesteps, number_steps):
    f_inter = interpolate.interp1d(timesteps, power, kind='previous')
    x_new = np.linspace(0, number_steps, num=number_steps, endpoint=True)
    y_new = f_inter(x_new)
    return x_new, y_new


def check_postcode(postcode):
    # connect to the database
    conn = sqlite3.connect('database_profiles.db')
    c = conn.cursor()
    # Build the SQL query to insert the row
    query = f"SELECT "
    # Execute the query with the values
    c.execute(query, [series_id] + values)
    # commit changes and close connection
    conn.commit()
    conn.close()
