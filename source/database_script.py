import random
import sqlite3

# connect to the database
conn = sqlite3.connect('database_profiles.db')
c = conn.cursor()

# create table with 1440 numbered columns
# columns = ", ".join(f"step_{i} float" for i in range(1440))
# c.execute(f"CREATE TABLE load_profiles_day (series_id TEXT PRIMARY KEY, {columns})")

values = [random.randint(0, 1000) for i in range(1440)]
series_id = "device_C"

# Build the SQL query to insert the row
query = f"INSERT INTO load_profiles_day (series_id, {' ,'.join([f'step_{i}' for i in range(1440)])}) VALUES (?, {'?,'*1439}?)"

# Execute the query with the values
c.execute(query, [series_id] + values)

# commit changes and close connection
conn.commit()
conn.close()
