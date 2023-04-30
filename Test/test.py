import sqlite3

# Connect to the original database
source_conn = sqlite3.connect(r"C:\Users\felix\Documents\HOME\Uni\02_Master\05_Masterthesis\02_Code\05_PowerHouse\source\database_profiles.db")
source_cursor = source_conn.cursor()

# Connect to the new database
dest_conn = sqlite3.connect(r"C:\Users\felix\Documents\HOME\Uni\02_Master\05_Masterthesis\02_Code\05_PowerHouse\source\database_profiles.db")
dest_cursor = dest_conn.cursor()

# Get the column names and types from the original table
source_cursor.execute("PRAGMA table_info(device_preset_old)")
columns = source_cursor.fetchall()

# Build the CREATE TABLE statement for the new table
create_table_statement = "CREATE TABLE device_preset ("
for i, column in enumerate(columns):
    if i == 1:
        create_table_statement += "device_type TEXT,"
    create_table_statement += f"{column[1]} {column[2]},"
create_table_statement = create_table_statement[:-1] + ")"
dest_cursor.execute(create_table_statement)

# Copy the data from the original table to the new table
insert_statement = f"INSERT INTO device_preset ({','.join([column[1] for column in columns])}) VALUES ({','.join(['?' for column in columns])})"
data = source_cursor.execute("SELECT * FROM device_preset_old")
dest_cursor.executemany(insert_statement, data)

device_types = [('Refrigerator_Big', 'refrigerator'), ('Refrigerator_Small_New', 'refrigerator'), ('Refrigerator_Small_Old', 'refrigerator'),
                ('water_boiler', 'boiler'), ('lamp_01', 'lamp'), ('lamp_02', 'lamp'), ('lamp_03', 'lamp'), ('lamp_04', 'lamp'),
                ('desktop_pc_4h', 'desktop_pc'), ('desktop_pc_8h', 'desktop_pc'), ('desktop_pc_12h', 'desktop_pc')]

for profile in device_types:
    query = f"UPDATE device_preset SET device_type = '{profile[1]}' WHERE series_id = '{profile[0]}'"
    dest_cursor.execute(query)

# Commit and close the connections
dest_conn.commit()
dest_conn.close()
source_conn.close()
