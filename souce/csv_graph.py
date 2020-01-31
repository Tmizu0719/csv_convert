"""
January 28th 2020
            Author T.Mizumoto
"""

#! python 3
# ver.01.00
# csv_graph.py

import numpy as np
import matplotlib.pyplot as plt
from csv_convert import CsvConvert
from Gui import FilePath
from fun_ConvertFilename import fun_basename
from graph import Graph

## param
filetype = "csv"
# number of base(x-axis) column
base = 0
xlabel = "time $\it{t}$ [-]"
ylabel = "volum $\it{v}$ [-]"
xmin, xmax = 0, 5
ymin, ymax = -2, 2 

## main
# get file path
gui = FilePath()
gui.path(filetype, filetype)
if len(gui.filepath_list) >= 1:    
    for i in gui.filepath_list:
        # load a file
        basename, directory = fun_basename(i, filetype)
        csv = CsvConvert()
        header, data = csv.convert_np(i)
        basedata = data[:, base]
        data = np.delete(data, base, axis = 1)
        header = np.delete(header, base)

        # draw a figure
        fig = Graph()
        fig.label = header
        for j in range(data.shape[1]):
            fig.line(basedata, data[:, j], j)
        fig.axis_label(xlabel, ylabel)
        fig.lim(xmin, xmax, ymin, ymax)
        plt.legend()
        fig.save_graph(directory + "/fig_" + basename)
        plt.show()
else:
    print("File Path was not Selected.")