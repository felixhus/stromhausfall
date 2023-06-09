import csv
import random
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sql_modules
from scipy import interpolate


def izes_csv_to_sqlite():
    p1_csv_path = "C:/Users/felix/Documents/HOME/Uni/02_Master/05_Masterthesis/03_Daten/IZES_Profile/CSV_74_Loadprofiles_1min_W_var/PL1.csv"
    p2_csv_path = "C:/Users/felix/Documents/HOME/Uni/02_Master/05_Masterthesis/03_Daten/IZES_Profile/CSV_74_Loadprofiles_1min_W_var/PL2.csv"
    p3_csv_path = "C:/Users/felix/Documents/HOME/Uni/02_Master/05_Masterthesis/03_Daten/IZES_Profile/CSV_74_Loadprofiles_1min_W_var/PL3.csv"
    Path('database_izes.db').touch()
    conn = sqlite3.connect('database_izes.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE load_1min (month int, day int)''')
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
        query = f"INSERT INTO load_1min VALUES ({date.month}, {date.day}, {placeholders})"

        if i % 1000 == 0:
            percent = "%.2f" % (i/525600*100)
            print(f"Wrote {i} rows ({percent}%)")

        cursor.execute(query, tuple(row_sum))
        date = date + timedelta(minutes=1)

    conn.commit()
    conn.close()


def write_to_database(database, values, series_id, device_type):
    """
    Module to write a preset device load profile to the corresponding database.

    :param database: Database name
    :type database: str
    :param values: List of power values, 1440 steps
    :type values: list[int]
    :param series_id: Unique series_id of the profile
    :type series_id: str
    :param device_type: Type of device which can use this profile
    :type device_type: str
    :return: None
    """

    # connect to the database
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # values = values.tolist()

    # Build the SQL query to insert the row
    query = f"INSERT INTO device_preset (series_id, type, {' ,'.join([f'step_{i}' for i in range(1440)])}) VALUES (?, ?, {'?,' * 1439}?)"

    # Execute the query with the values
    c.execute(query, [series_id, device_type] + values)

    # commit changes and close connection
    conn.commit()
    conn.close()


def write_part_profile_to_database(start_index, end_index, values, series_id, device_type, standby):
    """
    Module to write a custom device load profile to the corresponding database.

    :param start_index: Minute of the day on which the profile snippet starts (corresponding to the input file)
    :type start_index: int
    :param end_index: Minute of the day on which the profile snippet ends (corresponding to the input file)
    :type end_index: int
    :param values: Complete load profile as
    :type values: list[int]
    :param series_id: Unique series_id of the profile
    :type series_id: str
    :param device_type: Type of device which can use this profile
    :type device_type: str
    :param standby: Standby power of the device for times outside the used profile snippet
    :type standby: int
    :return: None
    """

    # Connect to the database
    conn = sqlite3.connect('database_profiles.db')
    cursor = conn.cursor()

    # Build the SQL statement
    columns = ', '.join(['step_' + str(i) for i in range(end_index - start_index + 1)])
    placeholders = ', '.join(['?' for i in range(start_index, end_index + 1)])
    query = f"INSERT INTO device_custom (series_id, type, standby_power, {columns}) VALUES (?, ?, ?, {placeholders})"

    # Get the range of values to insert
    range_of_values = values[start_index:end_index + 1]

    # Execute the SQL statement
    cursor.execute(query, [series_id, device_type, standby] + range_of_values)
    conn.commit()

    # Close the database connection
    conn.close()


def add_device_to_database(device_type, standard_room, device_name, menu_type, icon, power_options):
    """
    Module to add a new device to the sql database.

    :param device_type: Unique type of device which should be added
    :type device_type: str
    :param standard_room: The standard room of the device, where it automatically appears in the menu
    :type standard_room: str
    :param device_name: Displayed Device name
    :type device_name: str
    :param menu_type: Type of device, 'device_preset' or 'device_custom'
    :type menu_type: str
    :param icon: Iconify icon name reference
    :type icon: str
    :param power_options: Dictionary of options for power profiles
    :type power_options: dict
    :return: None
    """

    # Connect to the database
    conn = sqlite3.connect('database_profiles.db')
    cursor = conn.cursor()

    # Build the SQL statement

    query = f"INSERT INTO devices (type, standard_room, name, menu_type, icon, power_options) VALUES (?, ?, ?, ?, ?, ?)"

    # Execute the SQL statement
    cursor.execute(query, [device_type, standard_room, device_name, menu_type, icon, power_options])
    conn.commit()

    # Close the database connection
    conn.close()


# print("Start")
# filepath = r""
# # Read values from csv-file, formatted for tracebase dataset
# df = pd.read_csv(filepath, header=None, delimiter=";", names=["datetime", "value1", "value2"])
# df["datetime"] = pd.to_datetime(df.iloc[:, 0])
# df.set_index("datetime", inplace=True)
# df_resampled = df.resample('1T').mean()
#
# # Take second value column
# values = df_resampled['value2'].tolist()
# power_options_device = {'Router': {'key': 'router_standard', 'icon': ''}}
# # power_options_device = json.dumps(power_options_device)
# # write_part_profile_to_database(556, 565, values, 'printer_print', 'printer', 0)
# # write_to_database('database_profiles.db', values, 'router_standard', 'router')
# add_device_to_database('router_2', 'office', 'Router', 'device_preset', 'tabler:router', power_options_device)
# print("Done")
