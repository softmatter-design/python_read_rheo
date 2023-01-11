#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import csv
import os
import platform
import subprocess

import numpy as np
import matplotlib.pyplot as plt
import variables as var
#####

#####
def readcsv():
	csv_read(var.csvfile)
	for line in var.datalist:
		freq = []
		tand = []
		for dataline in line[1][1:]:
			freq.append(float(dataline[0]))
			tand.append(float(dataline[3]))
		var.axdata.append([int(line[0]), freq, tand])

	plot()
	# set_shift(datalist, base_temp)

	# make_datafiles(datalist)

	# repeat = len(datalist)
	# make_multi_graph(repeat)
	return

def csv_read(csvfile):
	with open(csvfile, encoding='utf8') as f:
		csvread = list(csv.reader(f))
	datalist = make_datalist(csvread)
	return datalist

def make_datalist(csvread):
	for i, line_csvread in enumerate(csvread):
		tmp = [[[] for i in var.cols] for j in range(var.n_data+1)]
		if line_csvread[0] == '測定点数':
			temp = float(csvread[i+2][2])
			for col, item in enumerate(var.cols):
				tmp[0][col] = line_csvread[item]
				for j in range(var.n_data):
					tmp[j+1][col] = csvread[i+2+j][item]
			var.datalist.append([round(temp), tmp])
	return

# def makecolor(num):
# 	col_list = []
# 	ind = 0
# 	value = [0., 0.5, 1.0]
# 	# [0., 0.25, 0.5, 0.75, 1.0]
# 	while ind < num:
# 		for red, green, blue in itertools.product(value, value, value):
# 			col_list.append([red, green, blue])
# 			ind+=1
# 			if ind >= num:
# 				break
# 	return col_list

def plot():
	fig, ax = plt.subplots()

	for i, data in enumerate(var.axdata):
		ax.plot(data[1], data[2], label='T='+str(data[0]))

	ax.set_xlabel('Freq.')  # x軸ラベル
	ax.set_ylabel('Tan d')  # y軸ラベル
	ax.set_title('Measured Raw Data') # グラフタイトル
	ax.semilogx(base=10)
	ax.legend(borderaxespad=0, ncol=2)
	plt.pause(1)
	
	inp = input('input "q" to quit  ')
	if inp == 'q':
		return
	else:
		os.system('cls')
		plt.cla()

	inp = ''
	while inp != 'q':
		
		for i, data in enumerate(var.axdata):
			temp = data[0]
			at = 10**(-1*var.c1*(temp - var.ts)/(var.c2 + temp - var.ts))
			print(temp, at)
			mfreq = [i*at for i in data[1]]
			ax.plot(mfreq, data[2], label='T='+str(temp))

		ax.set_xlabel('Freq.')  # x軸ラベル
		ax.set_ylabel('Tan d')  # y軸ラベル
		ax.set_title('Shifted by AT') # グラフタイトル
		# ax.grid()            # 罫線
		ax.loglog(base=10)
		ax.legend(borderaxespad=0, ncol=2)
		
		plt.pause(0.01)

		inp = input('input "q" to quit ')
		os.system('cls')
		plt.cla()
	return

if __name__ == '__main__':
	readcsv()