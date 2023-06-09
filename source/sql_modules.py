"""
sql_modules.py contains all modules to get different kind of data out of different SQL databases.
"""
import sqlite3
from datetime import timedelta

import numpy as np
from scipy import interpolate


def dict_factory(cursor, row):  # To get dictionary from sql query
    """
    Define row factory for cursor

    :param cursor: SQLite cursor
    :param row:
    :return: Row factory for cursor
    """

    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_coordinates(plz, database):
    """
    Get longitude and latitude coordinates of given postcode. The function also returns the city name.

    :param plz: postcode
    :type plz: int
    :param database: path of database
    :type database: str
    :return: lon, lat, city name
    """

    conn = sqlite3.connect(database)  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object
    # Select the row of values from the table
    data = cursor.execute(f"SELECT lon, lat, city FROM plz_data WHERE postcode = {plz}").fetchone()
    data = list(data)  # convert to a list
    # Close the cursor and database connection
    cursor.close()
    conn.close()
    return data[0], data[1], data[2]  # return lon and lat and city name


def get_load_profile(table_name: str, key: str, database: str):
    """
    Loads a power profile with a given key from a given database and table. Cuts away null values.

    :param table_name: Name of the table to get profile from
    :type table_name: str
    :param key: Key of the profile to fetch
    :type key: str
    :param database: Database to read from
    :type key: str
    :return: Load profile
    :rtype: list
    """

    conn = sqlite3.connect(database)  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object
    # Select the row of values from the table
    row = cursor.execute(f"SELECT * FROM {table_name} WHERE series_id = ?", (key,)).fetchone()
    row = list(row[2:])  # remove series_id and type and convert to a list
    end_index = 0
    # The SQL query gets all 1440 values from the database, also the many null values which are not filled by a profile
    for index, value in enumerate(reversed(row)):   # Iterate backwards throw the list
        if value is not None:                       # Find the last value of the profile
            end_index = len(row) - index
            break
    row = row[:end_index]                           # Cut away the null part
    # Close the cursor and database connection
    cursor.close()
    conn.close()
    return row


def write_to_database(database, values, series_id):
    # connect to the database
    conn = sqlite3.connect(database)
    c = conn.cursor()
    values = values.tolist()
    # Build the SQL query to insert the row
    query = f"INSERT INTO load_profiles_day (series_id, {' ,'.join([f'step_{i}' for i in range(1440)])}) VALUES (?, {'?,' * 1439}?)"
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


def check_postcode(postcode, database):
    """
    Check whether a given postcode exist in database.

    :param postcode: Postcode to check
    :type postcode: int
    :param database: Database to connect to
    :type database: str
    :return: Result of check if postcode exists
    :rtype: bool
    """

    if postcode is None:  # If the postcode is missing
        return False
    # connect to the database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    # Build the SQL query to check for postcode
    data = cursor.execute(f"SELECT postcode FROM plz_data WHERE postcode = {postcode}").fetchone()
    # close connection
    conn.close()
    if data:
        return True
    else:
        return False


def get_household_profile(database, profile_number, date_start, date_stop):
    """
    Load a power profile from the given database. The profile-number is provided with the start and end date.

    :param database: Database to fetch from
    :type database: str
    :param profile_number: Number of the profile, out of a predefined selection of profile numbers
    :type profile_number: int
    :param date_start: Start date of timeframe to fetch
    :type date_start: date
    :param date_stop: End date of timeframe to fetch
    :type date_stop: date
    :return: Power profile
    :rtype: list
    """

    if date_start.month > date_stop.month:
        # If it is week 1 of the year so some days are in the december before, use week 2
        date = date_start + timedelta(weeks=1)
    else:
        date = date_start
    conn = sqlite3.connect(database)  # connect to the database
    cursor = conn.cursor()
    power = []
    profile = "profile_" + str(profile_number)
    for day in range(7):
        data_day = cursor.execute(
            f"SELECT {profile} FROM load_1min WHERE day = {date.day} and month = {date.month}").fetchall()
        data_day = [d[0] for d in data_day]
        power += data_day
        date = date + timedelta(days=1)
    conn.close()  # close connection
    return power


def get_button_dict(database):
    """
    Load all devices from table "devices" of database, which have a standard room defined.

    :param database: path of sql-database
    :type database: str
    :return: list of devices from database
    :rtype: list
    """

    conn = sqlite3.connect(database)  # connect to the database

    query = "SELECT * FROM devices WHERE standard_room IS NOT NULL"     # Get all devices with a standard room
    devices = conn.execute(query).fetchall()
    return devices


def get_all_devices(database):
    """
    Get all devices that are stored in the database given.

    :param database: Database to fetch from
    :return: List of devices
    """

    conn = sqlite3.connect(database)  # connect to the database

    query = "SELECT * FROM devices"  # Get all devices
    devices = conn.execute(query).fetchall()
    return devices


def get_device(database, device_type):
    """
    Get device from SQL database

    :param database: Database to fetch from
    :param device_type: Type of device to fetch
    :return: List of devices
    """

    conn = sqlite3.connect(database)  # connect to the database
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    query = f"SELECT * FROM devices WHERE type = '{device_type}'"  # Get all devices
    device = cursor.execute(query).fetchall()
    return device
