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

from scipy.optimize import leastsq
#####
def make_master():
	readcsv()
	adjust()
	tune()
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
		tmplist = []
		for data in var.axdata:
			temp = data[0]
			at = 10**(-1*var.c1*(temp - var.ts)/(var.c2 + temp - var.ts))
			tmplist.append([temp, at, 1.])
			var.shift_list = tmplist
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

		inp = input('to exit input "q"')
		if inp == 'q':
			set_shift()
			os.system('cls')
			plt.close()
		else:
			os.system('cls')
			plt.cla()
	return

def tune():
	fig, ax = plt.subplots()

	
	inp = ''
	while inp != 'q':
		with open('shift.csv', encoding='utf8') as f:
			tmp_shift = list(csv.reader(f))
			print(tmp_shift)

		for i, data in enumerate(var.axdata):
			temp = data[0]
			if temp != float(tmp_shift[i][0]):
				exit()
			else:
				at = float(tmp_shift[i][1])
				mfreq = [j*at for j in data[1]]
				ax.plot(mfreq, data[2], label='T='+str(temp))

		ax.set_xlabel('Freq.')  # x軸ラベル
		ax.set_ylabel(r'Tan $\delta$')  # y軸ラベル
		ax.set_title('Shifted by AT') # グラフタイトル
		# ax.grid()            # 罫線
		ax.loglog(base=10)
		ax.legend(borderaxespad=0, ncol=2)
		
		plt.pause(1)

		# modts= input("T_ref is set to " + str(var.ts) + '\nPut new data')
		# if modts != '' and modts.isnumeric:
		# 	var.ts = float(modts)

		inp = input('to exit input "q"')
		if inp == 'q':
			print()
			# set_shift()
		else:
			os.system('cls')
			plt.cla()
	return

def func(prm, x, y):
	a, b, c, d = prm[0], prm[1], prm[2], prm[3]
	residual = y-(a*x**3+b*x**2+c*x+d)
	# a, b, c = prm[0], prm[1], prm[2]
    # residual = y-(a*x**2+b*x+c)
	return residual

def plot3():
	fig, ax = plt.subplots()
	for data in var.axdata:
		# data = var.axdata[8]
		x = np.array(data[1])
		y = np.array(data[2])
		temp = data[0]
		ax.plot(x, y, label='T='+str(temp))

		ax.set_xlabel('Freq.')  # x軸ラベル
		ax.set_ylabel(r'Tan $\delta$')  # y軸ラベル
		ax.set_title('Shifted by AT') # グラフタイトル
		# ax.grid()            # 罫線
		# ax.loglog(base=10)
		ax.legend(borderaxespad=0, ncol=2)
		
		prm = [1, 1., 1, 1]
		# prm = [1., 1., 1.]
		result = leastsq(func, prm, args=(x, y))

		ax.plot(x, result[0][0]*x**3+result[0][1]*x**2+result[0][2]*x+result[0][3])
		# ax.plot(x, result[0][0]*x**2+result[0][1]*x+result[0][2])

		plt.pause(1)
		inp = input('input "q" to quit  ')
		if inp == 'q':
			exit()
		else:
			os.system('cls')
			plt.cla()
	os.system('cls')
	plt.cla()
	return


def set_shift():
	with open('shift.csv','w') as f:
		for each in var.shift_list:
			f.write(f'{each[0]:}, {each[1]:.2e}, {each[2]:.2f} \n')
	return
	
if __name__ == '__main__':
	make_master()