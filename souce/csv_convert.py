"""
January 4th 2020
            Author T.Mizumoto
"""
#! python 3
# ver.01.10
# csv_convert.py  -  this program converts .csv file to matrix

import numpy as np
import sys

class CsvConvert:
    delimiter = ","

    def convert_np(self, path):
        # header
        with open(path, "r") as file:
            lines = list(file)
        header = lines[0].strip().split(self.delimiter)
        # data
        data = np.genfromtxt(path, delimiter = self.delimiter, skip_header = 1)
        judge = np.isnan(data)
        count = 1
        for i in judge:
            if True in i:
                print("There is a missing value on line " + str(count) + ".")
            count += 1
        return header, data

    def delete_nanrow(self, data):
        judge = np.isnan(data)
        count = 1
        del_list = []
        for i in judge:
            if True in i:
                del_list.append(count)
            count += 1
        del_data = np.delete(data, del_list, 0)
        print("Lines" + str(del_list) + "deleted.")
        return del_data

    def replace_nan(self, data, nan):
        replace_data = np.nan_to_num(data, nan = nan)
        return replace_data

    def D3_connect(self, pathlist):
        count = 0
        for i in pathlist:
            if count == 0:
                header, data = self.convert_np(i)
            else:
                h_tmp, d_tmp = self.convert_np(i)
                if not header == h_tmp:
                    print("ERROR: The header is different.")
                    print("error file path: " + i)
                    sys.exit(1)
                else:
                    data = np.dstack([data, d_tmp])
            count += 1
        return header, data


if __name__ == "__main__":
    CC = CsvConvert()
    header, data = CC.convert_np("test_data.csv")
    print(header)
    print(data)
    print(CC.delete_nanrow(data))
    print(CC.replace_nan(data, 0))