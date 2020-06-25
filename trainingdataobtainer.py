import os
import pandas as pd
from read_qdp import read_qdp
import matplotlib.pyplot as plt
from pathlib import Path

# initialise variables
rootdir = r'C:\Users\arnol\Desktop\newproject\SAFARI TES data\Selection'
Path(rootdir + r"\Plots").mkdir(parents=True, exist_ok=True)
save_plots_to = rootdir + r'\Plots'
filelocationlist = []

extensions = '.qdp'
iandv = pd.DataFrame()
features = pd.DataFrame()
expnr = 1
errorcount = 0

# extract df, iandv, features, expnr from .qdp files
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file[0] == 'I':  # if starting with I to make sure other files are excluded
            ext = os.path.splitext(file)[-1].lower()
            if ext == '.qdp':
                filelocation = os.path.join(subdir, file)
                # if file cannot be read, display error
                try:
                    df, iandv, features, expnr, filelocationlist = read_qdp(filelocation, iandv, features, expnr, filelocationlist, make_excel=False)
                except (pd.errors.ParserError, pd.errors.EmptyDataError):
                    errorcount += 1
                    print(filelocation)

print(
    "The above " + str(errorcount) + " file(s) were invalid and skipped, please check formats manually. Continuing...")

# output filelocationlist.txt
filelocationlistfile = open('filelocationlist.txt', 'w')
for filelocation in filelocationlist:
    filelocationlistfile.write(filelocation)
    filelocationlistfile.write('\n')
filelocationlistfile.close()

# convert to .xlsx files
iandv.to_excel('iandv.xlsx', index=False)
features.columns = ['mean', 'std', 'skewness', 'kurtosis', 'grad mean', 'grad std', 'grad skewness', 'grad kurtosis']
features = (features - features.mean()) / features.std()
features.to_excel('features.xlsx', index=False)

# plot where the i + 1 means you can more easily compare rows in .xlsx files with plots as headers are in row 1
for i in range(1, expnr):
    iandv.plot(kind='scatter', x='Current ' + str(i + 1) + ' (I)', y='V_fb ' + str(i + 1) + ' (V)', color='red')
    plt.savefig(save_plots_to + r'\row ' + str(i + 1) + '.png', dpi=300)
    plt.close('all')
