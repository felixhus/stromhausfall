import sqlite3

import pandas as pd

# create the connection to the database
conn = sqlite3.connect('example.db')

# create the tables in the database
conn.execute('CREATE TABLE IF NOT EXISTS table1 (a INTEGER, b INTEGER, c INTEGER)')
conn.execute('CREATE TABLE IF NOT EXISTS table2 (a INTEGER, b INTEGER, c INTEGER)')
conn.execute('CREATE TABLE IF NOT EXISTS table3 (a INTEGER, b INTEGER, c INTEGER)')
conn.execute('CREATE TABLE IF NOT EXISTS result (a INTEGER, b INTEGER, c INTEGER)')

# create example dataframes
df1 = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]})
df2 = pd.DataFrame({'a': [2, 3, 4], 'b': [5, 6, 7], 'c': [8, 9, 10]})
df3 = pd.DataFrame({'a': [3, 4, 5], 'b': [6, 7, 8], 'c': [9, 10, 11]})

# iterate over the rows of the dataframes and insert the resulting row to the database
for i, row in enumerate(df1.iterrows()):
    # get the corresponding rows from the other dataframes
    row2 = df2.iloc[i]
    row3 = df3.iloc[i]

    # add up the rows elementwise
    result_row = row[1] + row2 + row3

    # insert the row to the database
    conn.execute('INSERT INTO result (a, b, c) VALUES (?, ?, ?)', tuple(result_row))

# commit the changes to the database
conn.commit()

# close the connection to the database
conn.close()
