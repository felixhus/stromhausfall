import sqlite3

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def plot_all_izes():
    # Define variables for start and end rows of each series
    series1_start = 40320   # KW 4
    series1_end = 50400
    series2_start = 292320  # KW 29
    series2_end = 302400

    pdf_path = r"C:\Users\felix\Documents\HOME\Uni\02_Master\05_Masterthesis\02_Code\05_PowerHouse\source\plots_izes.pdf"

    pdf = PdfPages(pdf_path)

    print("Start")
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
        ax.plot(series1, label='KW 4')
        ax.plot(series2, label='KW 29')
        ax.legend()
        ax.set_title(column)

        pdf.savefig(fig)
        plt.close(fig)

    # Show all the plots
    # plt.show()

    # Close the database connection
    conn.close()
    pdf.close()
    print("Done")


def move_columns_izes():
    to_remove = [46, 4, 7, 9, 14, 15, 16, 17, 18, 19, 20, 22, 23, 27, 28, 32, 33, 39, 41, 73, 42, 45, 47, 58, 61, 62, 65]
    path_destination = r"C:\Users\felix\Documents\HOME\Uni\02_Master\05_Masterthesis\02_Code\05_PowerHouse\source\database_izes_reduced.db"
    print("Start")

    # Connect to the destination database
    dest_conn = sqlite3.connect(path_destination)
    dest_cursor = dest_conn.cursor()

    table = "load_1min"

    for i in range(74):
        if i + 1 not in to_remove:
            column = "profile_" + str(i+1)
            query = f"ALTER TABLE {table} DROP COLUMN {column}"
            dest_cursor.execute(query)

    dest_conn.commit()
    dest_conn.close()

    print("Done")

move_columns_izes()
