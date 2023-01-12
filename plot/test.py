#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import csv
import os
import platform
import subprocess

import math
import numpy as np
import matplotlib.pyplot as plt
import variables as var
#####
def make_master():
	readcsv()
	adjust()
	return

def readcsv():
	csv_read(var.csvfile)
	for line in var.datalist:
		freq = []
		tand = []
		for dataline in line[1][1:]:
			freq.append(float(dataline[0]))
			tand.append(float(dataline[3]))
		var.axdata.append([int(line[0])+273.15, freq, tand])
	plot_raw()
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

def plot_raw():
	fig, ax = plt.subplots()

	for i, data in enumerate(var.axdata):
		ax.plot(data[1], data[2], label='T='+str(data[0]))

	ax.set_xlabel('Freq.')  # x軸ラベル
	ax.set_ylabel(r'Tan $\delta$')  # y軸ラベル
	ax.set_title('Measured Raw Data') # グラフタイトル
	ax.semilogx(base=10)
	ax.legend(borderaxespad=0, ncol=2)
	plt.pause(1)
	
	inp = input('input "q" to quit  ')
	if inp == 'q':
		exit()
	else:
		os.system('cls')
		plt.close()
	return

def adjust():
	plot2()
	return


def plot2():
	fig, ax = plt.subplots()

	inp = ''
	while inp != 'q':
		
		for data in var.axdata:
			temp = data[0]
			at = 10**(-1*var.c1*(temp - var.ts)/(var.c2 + temp - var.ts))
			print(temp, at)
			mfreq = [i*at for i in data[1]]
			ax.plot(mfreq, data[2], label='T='+str(temp))

		ax.set_xlabel('Freq.')  # x軸ラベル
		ax.set_ylabel(r'Tan $\delta$')  # y軸ラベル
		ax.set_title('Shifted by AT') # グラフタイトル
		# ax.grid()            # 罫線
		ax.loglog(base=10)
		ax.legend(borderaxespad=0, ncol=2)
		
		plt.pause(1)

		modts= input("T_ref is set to " + str(var.ts) + '\nPut new data')
		if modts != '' and modts.isnumeric:
			var.ts = float(modts)

		inp = input('input "q" to quit ')
		os.system('cls')
		plt.cla()
	return

def savetable():
	return

	
if __name__ == '__main__':
	make_master()