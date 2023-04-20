import sqlite3

import matplotlib.pyplot as plt

# Define variables for start and end rows of each series
series1_start = 1000
series1_end = 5000
series2_start = 20000
series2_end = 25000

# Connect to SQLite database
conn = sqlite3.connect(r"C:\Users\felix\Documents\HOME\Uni\02_Master\05_Masterthesis\02_Code\05_PowerHouse\source\database_izes.db")
c = conn.cursor()

# Get the column names from the database
c.execute("SELECT * FROM load_1min LIMIT 1")
columns = [description[0] for description in c.description]

# Loop through each column in the database
for column in columns:
    # Get the values for the first series
    c.execute(f"SELECT {column} FROM load_1min WHERE rowid >= {series1_start} AND rowid <= {series1_end}")
    series1 = [row[0] for row in c.fetchall()]

    # Get the values for the second series
    c.execute(f"SELECT {column} FROM load_1min WHERE rowid >= {series2_start} AND rowid <= {series2_end}")
    series2 = [row[0] for row in c.fetchall()]

    # Create a new plot for this column
    fig, ax = plt.subplots()
    ax.plot(series1, label='Series 1')
    ax.plot(series2, label='Series 2')
    ax.legend()
    ax.set_title(column)

# Show all the plots
plt.show()

# Close the database connection
conn.close()
