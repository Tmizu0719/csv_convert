"""
January 30th 2020
            Author T.Mizumoto
"""

#! python 3
# ver.01.00
# csv_connect.py

import numpy as np
from csv_convert import CsvConvert
from Gui import FilePath
from graph import Graph
import matplotlib.pyplot as plt
from fun_ConvertFilename import fun_basename
from fun_rms import fun_rms
import re

## param
filetype = "csv"
# column    base = x-axis, volum = y-axis(multiple OK)
base = 0
volum = [2]
xlabel = "distance $\it{l}$ [m]"
ylabel = "volum $\it{C_d}$ [-]"
xmin, xmax = 0, 5
ymin, ymax = 0, 0.3 


## main
# get file path
gui = FilePath()
gui.path(filetype, filetype)
first_name, directory = fun_basename(gui.filepath_list[0], filetype)
first_name = re.findall(r"\d+", first_name)
end_name, directory = fun_basename(gui.filepath_list[-1], filetype)
end_name = re.findall(r"\d+", end_name)
print("Got " + str(len(gui.filepath_list)) + " file path.")

# load files
csv = CsvConvert()
print("Now Connecting...")
header, data = csv.D3_connect(gui.filepath_list)
print("Successful!")
# average
print("Now Averaging...")
count = 0
for i in volum:
    if count == 0:
        mean_data = np.mean(data[:, i, :], axis = 1)
    else:
        mean = np.mean(data[:, i, :], axis = 1)
        mean_data = np.stack([mean_data, mean], axis = 1)
    count += 1
print("Successful!")
# rms
print("Now RMS calculating...")
count = 0
for i in volum:
    data_T = data[:, i, :].T
    if count == 0:
        if len(mean_data.shape) == 1:
            rms_data = fun_rms(data_T, mean_data[count].T)
        else:
            rms_data = fun_rms(data_T, mean_data[:, count].T)
    else:
        rms = fun_rms(data_T, mean_data[:, count].T)
        rms_data = np.stack([rms_data, rms], axis = 0)
    count += 1
rms_data = rms_data.T
print("Successful!")

# save csv
saveheader = header[base]
if len(volum) == 1:
    savedata = np.stack((data[:, base, 0], mean_data, rms_data), axis = 1)
    saveheader = header[base] + " " + "mean_" + header[volum[0]] + " " + "rms_" + header[volum[0]]
else:
    savedata = np.concatenate((data[:, base, 0].reshape(-1, 1), mean_data, rms_data), axis = 1)
np.savetxt(directory + "MandF_" + str(first_name[0]) + "_" + str(end_name[0]) + ".csv", savedata, \
    delimiter = ",", header = saveheader, comments = "")

# draw a figure
fig_mean = Graph()
fig_mean.label = [header[i] for i in volum]
for i in range(len(volum)):
    if len(volum) == 1:
        fig_mean.line(data[:, base, 0], mean_data, i)
    else:
        fig_mean.line(data[:, base, 0], mean_data[:, i], i)
fig_mean.axis_label(xlabel, ylabel)
fig_mean.lim(xmin, xmax, ymin, ymax)
fig_mean.legend()
fig_mean.save_graph(directory + "/mean_" + str(first_name[0]) + "_" + str(end_name[0]))
plt.show()