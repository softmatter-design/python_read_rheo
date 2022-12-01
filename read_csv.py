#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

csvfile = "datafile.csv"
csvfile_open = open(csvfile,"r",encoding="utf-8")
csvfile_csvread =list(csv.reader(csvfile_open))
csvfile_open.close()

cols = [3, 9, 10, 12]
n_data = 11

datalist = []

for i, i_csvfile_csvread in enumerate(csvfile_csvread):
    tmp = [[[] for i in cols] for j in range(n_data+1)]
    if i_csvfile_csvread[0] == '測定点数':
        temp = float(csvfile_csvread[i+2][2])
        for col, item in enumerate(cols):
            tmp[0][col] = i_csvfile_csvread[item]
            for j in range(n_data):
                # print(csvfile_csvread[i+2+j][item])
                tmp[j+1][col] = csvfile_csvread[i+2+j][item]
        datalist.append([round(temp), tmp])

with open('data.dat','w') as f:
    for each in sorted(datalist):
        f.write('# Temp = ' + str(each[0]) +'\n')
        for item in each[1][0]:
            f.write('# ' + str(item) +'\t')
        f.write('\n\n')
        for line in each[1][1:]:
            for data in line:
                f.write(str(data) + '\t')
            f.write('\n')
        f.write('\n\n')



