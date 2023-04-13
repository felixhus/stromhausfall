import os

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

directory = r"C:\Users\felix\Documents\HOME\Uni\02_Master\05_Masterthesis\03_Daten\Tracebase Profiles\synthetic"
counter = 0
all_files = 330

for dir in os.listdir(directory):
    dir_working = os.path.join(directory, dir)
    plot_name = 'plots_' + os.path.basename(dir) + '.pdf'
    pdf_path = os.path.join(dir_working, plot_name)

    pdf = PdfPages(pdf_path)
    for filename in os.listdir(dir_working):
        file = os.path.join(dir_working, filename)
        if os.path.isfile(file) and filename[:5] != 'plots':
            df = pd.read_csv(file, header=None, delimiter=";", names=["datetime", "value1", "value2"])
            df["datetime"] = pd.to_datetime(df.iloc[:, 0])
            df.set_index("datetime", inplace=True)
            df_resampled = df.resample('1T').mean()
            fig = plt.figure()
            plt.plot(df_resampled)
            plt.title(filename + '; Steps: ' + str(len(df_resampled['value1'])))
            # plt.show()
            pdf.savefig(fig)
            plt.close(fig)
            del df_resampled
            del df
            del fig
            counter += 1
            print('Saved ' + filename + f' ({counter/all_files*100:.2f}%)')
    pdf.close()
    print('Done with ' + dir)
print('Done')
