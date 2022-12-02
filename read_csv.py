#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import csv
import platform
import subprocess
#####
csvfile = "datafile.csv"
cols = [3, 9, 10, 12]
n_data = 11
base_temp = 130
#####
def readcsv():
	datalist= csv_read(csvfile)

	set_shift(datalist, base_temp)

	make_datafiles(datalist)

	repeat = len(datalist)
	make_multi_graph(repeat)
	return
#####
def csv_read(csvfile):
	with open(csvfile, encoding='utf8') as f:
		csvread = list(csv.reader(f))
	datalist = make_datalist(csvread)
	return datalist

def make_datalist(csvread):
	datalist = []
	for i, line_csvread in enumerate(csvread):
		tmp = [[[] for i in cols] for j in range(n_data+1)]
		if line_csvread[0] == '測定点数':
			temp = float(csvread[i+2][2])
			for col, item in enumerate(cols):
				tmp[0][col] = line_csvread[item]
				for j in range(n_data):
					tmp[j+1][col] = csvread[i+2+j][item]
			datalist.append([round(temp), tmp])
	return datalist

def set_shift(datalist, base_temp):
	shift_dic = {each[0]:10**((base_temp - float(each[0]))/10) for each in datalist}
	with open('shift.dat','w') as f:
		f.write('#\tTemp\taT\tbT\n')
		for each in sorted(datalist):
			f.write(f'{each[0]}\t{shift_dic[each[0]]:.1e}\t1.0\n')
	return

def make_datafiles(datalist):
	shift_dic = read_shift()
	with open('data.dat','w') as f:
		for each in sorted(datalist):
			at = shift_dic[str(each[0])][0]
			bt = shift_dic[str(each[0])][1]
			f.write(f'# Temp = {each[0]}\t{at}\t{bt}\n# ')
			for item in each[1][0]:
				f.write(str(item) +'\t')
			f.write('\n\n')
			for line in each[1][1:]:
				f.write(f'{float(line[0])*float(at):.2e}\t')
				for data in line[1:3]:
					f.write(f'{float(data)*float(bt):.2e}\t')
				f.write(str(line[3]) + '\n')
			f.write('\n\n')
	return

def read_shift():
	shift_dic = {}
	with open('shift.dat', 'r') as f:
		shift_list = f.readlines()
		for line in shift_list:
			line_list = line.replace('\n', '').split('\t')
			if line_list[0] != '#':
				shift_dic[line_list[0]] = [line_list[1], line_list[2]]
	return shift_dic

# グラフを作成
def make_multi_graph(repeat):
	make_multi_script(repeat)
	if platform.system() == "Windows":
		subprocess.call('plot.plt', shell=True)
	elif platform.system() == "Linux":
		subprocess.call('gnuplot ' + 'plot.plt', shell=True)
	return

# 必要なスクリプトを作成
def make_multi_script(repeat):
	with open('plot.plt', 'w') as f:
		script = multi_script_content(repeat)
		f.write(script)
	return

# スクリプトの中身
def multi_script_content(repeat):
	script = 'set term pngcairo font "Arial,14" \nset colorsequence classic \n'
	script += '# \ndata = "data.dat" \nset output "plot.png"\n'
	script += '#\nset size square\nset y2tics\nset logscale xyy2\n\n'
	script += '#\n#set xrange [1e-2:1e5]\nset yrange [1e4:2e9]\nset y2range [1e-2:1e1]\n\n'
	script += '#\nset xlabel "Freq."\nset ylabel "G"\nset y2label "tan{/Symbol d}"\n\n'
	#
	script += 'plot '
	for i in range(repeat):
		script += 'data ind ' + str(i) + ' u 1:4 axis x1y2 w l lc ' + str(i) + ' noti, \\\n'
	script += '\n\nreset'
	return script


if __name__ == '__main__':
	readcsv()