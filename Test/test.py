import sqlite3

# connect to the database
conn = sqlite3.connect('test_db.db')
c = conn.cursor()

# create table with 1440 numbered columns
columns = ", ".join(f"col{i} float" for i in range(1440))
c.execute(f"CREATE TABLE your_table_name (series_id INTEGER PRIMARY KEY, {columns})")

# commit changes and close connection
conn.commit()
conn.close()
