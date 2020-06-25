import pandas as pd
import re
from scipy.stats import describe
import numpy as np


def read_qdp(filelocation, iandv, features, expnr, filelocationlist, make_excel=False):
    """
    Accepts a raw sting literal for the filename and path.
    x and y are strings which name the first 2 columns, default to bias
    and V fb (V)
    If make_excel is set to True then excel file is created in the name
    of the input file.
    Return the a pandas dataframe with the data.
    """

    # name first two cols
    x = 'Current ' + str(expnr + 1) + ' (I)'
    y = 'V_fb ' + str(expnr + 1) + ' (V)'
    cols = {0: x, 1: y}
    header = 0

    # skip amount of rows until a number is found (which is valid data)
    with open(filelocation) as file:
        for line in file:
            if line[0].isdigit():
                break
            header += 1
    df = pd.read_csv(filelocation, sep='\\s+', header=None, skiprows=header, index_col=False, comment='!')

    # make list of col names for df and number ones without labels
    col_names = []
    for i in range(len(df.columns)):
        try:
            col_names.append(cols[i])
        except:  # way too broad exception... again ask Callum
            col_names.append(str(i))
        i += 1

    # set column names and sort by x vals
    df.columns = col_names
    df.sort_values(by=[x], inplace=True)

    # no idea what the purpose of this is, ask Callum
    if df.iloc[:, 0][1] * df.iloc[:, 1][1] < 0:
        df.iloc[:, 1] *= -1

    # make excel file
    if make_excel:
        # find name for excel sheet from end of path
        name_match = re.search(r'(\\?((?:.(?!\\))+)$)', filelocation)  # also no clue what this does, ask Callum
        name = re.sub(r'(\.qdp|\\)', r'', name_match.group(1))
        # write to file and save
        writer = pd.ExcelWriter(str(name) + '.xlsx')
        df.to_excel(writer, 'Sheet1', index=False)
        writer.save()

    # obtain IV columns and select features
    firsttwocol = df.iloc[:, [0, 1]].dropna()

    # check if any of the two columns are empty and check for enough data points, if not obtain data
    if not firsttwocol.empty and len(firsttwocol.index) > 100:
        # make sure the plots aren't skewed, take mean of first and last n points to draw slope
        n = 10
        a = (np.mean(firsttwocol.iloc[(2 * -n):-n, 1]) - np.mean(firsttwocol.iloc[n:(2 * n), 1])) \
            / (np.mean(firsttwocol.iloc[(2 * -n):-n, 0]) - np.mean(firsttwocol.iloc[n:(2 * n), 0]))
        b = firsttwocol.iloc[:, 1] - a * firsttwocol.iloc[:, 0]
        firsttwocol.iloc[:, 1] = firsttwocol.iloc[:, 1] - a * firsttwocol.iloc[:, 0] + b

        # obtain data
        iandv = pd.concat([iandv, firsttwocol], axis=1)
        stats = describe(firsttwocol.iloc[:, 1])
        gradient = np.gradient(firsttwocol.iloc[:, 1])
        statsgrad = describe(gradient)
        features = features.append([(stats.mean, stats.variance, stats.skewness, stats.kurtosis, statsgrad.mean,
                                     statsgrad.variance, statsgrad.skewness, statsgrad.kurtosis)])

        # up the counter
        expnr += 1

        # valid filelocations
        filelocationlist.append(filelocation)

    return df, iandv, features, expnr, filelocationlist
