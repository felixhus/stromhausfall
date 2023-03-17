import sqlite3


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
