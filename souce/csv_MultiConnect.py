"""
February 6th 2020
            Author T.Mizumoto
"""

#! python 3
# ver.01.00
# csv_MultiConnect.py

import numpy as np
from csv_convert import CsvConvert
from Gui import FilePath
from graph import Graph
import matplotlib.pyplot as plt
from fun_ConvertFilename import fun_basename
from fun_rms import fun_rms
import re

## param
data_name = ["set1", "set2", "set3"]
filetype = "csv"
# column    base = x-axis, volum = y-axis(multiple OK)
base = 0
volum = [4]
# if you use japanese to label, you should change "jp"
# else "en"
language = "jp"
xlabel = "データ数 $\it{N}$ [個]"
ylabel = "ランダムデータ(0-1) $\it{r}$ [-]"
xmin, xmax = 0, 5
ymin, ymax = 0, 1.0


## function
# fun load files
def load_csvfile(pathlist):
    csv = CsvConvert()
    print("Now Connecting...")
    header, data = csv.D3_connect(gui.filepath_list)
    print("Successful!")
    return header, data

def average(data, volum):
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
    return mean_data

def rms(data, volum):
    mean_data = average(data, volum)
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
    return mean_data, rms_data


## main
dic_data = {}
for i in range(len(data_name)):
    # get file path
    gui = FilePath()
    gui.path(filetype, filetype)
    first_name, directory = fun_basename(gui.filepath_list[0], filetype)
    first_name = re.findall(r"\d+", first_name)
    end_name, directory = fun_basename(gui.filepath_list[-1], filetype)
    end_name = re.findall(r"\d+", end_name)
    print("Got " + str(len(gui.filepath_list)) + " file path.")

    # load file
    header, data = load_csvfile(gui.filepath_list)
    # calculate mean and rms
    mean_data, rms_data = rms(data, volum)

    # save csv
    saveheader = header[base]
    if len(volum) == 1:
        savedata = np.stack((data[:, base, 0], mean_data, rms_data), axis = 1)
        saveheader = header[base] + " " + "mean_" + header[volum[0]] + " " + "rms_" + header[volum[0]]
    else:
        savedata = np.concatenate((data[:, base, 0].reshape(-1, 1), mean_data, rms_data), axis = 1)
    np.savetxt(directory + "MandF_" + str(first_name[0]) + "_" + str(end_name[0]) + ".csv", savedata, \
        delimiter = ",", header = saveheader, comments = "")

    # in to dictionary
    dic_data[data_name[i]] = savedata

# draw a figure
fig_mean = Graph()
fig_mean.label = data_name
fig_mean.language = language
for i in range(len(data_name)):
    ins_data = dic_data[data_name[i]]
    if len(volum) == 1:
            fig_mean.line(ins_data[:, 0], ins_data[:, 1], i)
    else:
        ins_name = fig_mean.label[i]
        ins_header = [header[x] + "@" + ins_name for x in volum]
        for j in range(1, 1 + len(volum)):
            fig_mean.line_NUL(ins_data[:, 0], ins_data[:, j], j, ins_header[j-1])
fig_mean.axis_label(xlabel, ylabel)
fig_mean.lim(xmin, xmax, ymin, ymax)
fig_mean.legend()
fig_mean.save_graph("mean_" + data_name[0] + "_" + data_name[-1])
plt.show()