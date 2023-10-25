#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 12:43:07 2023

@author: napi
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


def lineplot(df, headers):
    """ Function to create a lineplot. Arguments:
        A dataframe with a column "x" and other columns to be taken as y.
        A list containing the headers of the columns to plot.
        
        This is a very general version. You do not need to do something
        like that. A simple plot function will do. But transferring the data 
        as argument would be nice. Scoping (= having no arguments and pulling variables from the 
        main program) should better be avoided for simple programs. 
        It can be a source of hard to find errors.
    """

    plt.figure()

    #
    for head in headers:
        plt.plot(df["x"], df[head], label=head)

    # labelling
    plt.xlabel("x")
    plt.ylabel("f(x)")

    # removing white space left and right. Both standard and pandas min/max
    # can be used
    plt.xlim(min(df["x"]), df["x"].max())

    plt.legend()
    # save as png
    plt.savefig("linplot.png")
    plt.show()

    return  # Functions should finish with return


# create x array with 1000 points (usually enough for smooth lines)
x = np.linspace(-np.pi, np.pi, 1000)
# create dataframe from x;
# note that the columns argument needs to be a list even if only column
df_xy = pd.DataFrame(x, columns=["x"])

# calculate the sine and cosine and store in new columns
df_xy["sin"] = np.sin(df_xy["x"])
df_xy["cos"] = np.cos(df_xy["x"])
print(df_xy)

# calling lineplot with a list of the columns to be plotted.
lineplot(df_xy, ["sin", "cos"])
