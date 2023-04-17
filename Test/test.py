import sqlite3

# Connect to the database
conn = sqlite3.connect('database_profile.db')
cursor = conn.cursor()

# Define the start and end indices of the range to insert
start_index = 10
end_index = 20

# Define the list of values
values = [1.23, 4.56, 7.89, 0.12, 3.45, 6.78, 9.01, 2.34, 5.67, 8.90, 1.23, 4.56, 7.89, 0.12, 3.45, 6.78, 9.01, 2.34, 5.67, 8.90, ...]

# Build the SQL statement
columns = ', '.join(['step_' + str(i) for i in range(start_index, end_index+1)])
placeholders = ', '.join(['?' for i in range(start_index, end_index+1)])
query = f"INSERT INTO profile_custom ({columns}) VALUES ({placeholders})"

# Get the range of values to insert
range_of_values = values[start_index:end_index+1]

# Execute the SQL statement
cursor.execute(query, range_of_values)
conn.commit()

# Close the database connection
conn.close()
