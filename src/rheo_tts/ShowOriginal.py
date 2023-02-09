#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import csv
import numpy as np
import matplotlib.pyplot as plt
import pickle

import variables as var
# Show Original Data 
def show_orgdata():
	ncolm_list = [str(x) for x in range(len(var.csvlist[0]))]
	cond_label = list(var.datalabel_dic.keys())
	cond_data = [[var.datalabel_dic[key] for key in list(var.datalabel_dic.keys())]]

	frame_table = sg.Frame(
		'Selected Data Table', [
			[sg.Text('Selected Data File:'), sg.Text(var.csvfile)],
			[sg.Table(var.csvlist, headings=ncolm_list, display_row_numbers=True, def_col_width=6, auto_size_columns=False, vertical_scroll_only=False, num_rows=20)]
		]
	)
	frame_extract = sg.Frame(
		'Extract Data', [
			[sg.Table(cond_data, headings=cond_label, def_col_width=16, justification='center', auto_size_columns=False, num_rows=1)],
			[sg.Text('Skip Columns:', size=(10,1)), sg.Text(var.skip, size=(4,1))],
			[sg.Button("Extract", key='-extract-')]
		]
	)
	layout_orgtable = [
			[frame_table],
			[frame_extract],
			[sg.Button('Exit', key = '-exit-')]
	]
	orgdata_window = sg.Window('Selected Data', layout_orgtable, finalize=True, size=(800,600), resizable=True)

	while True:
		event, values = orgdata_window.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == '-extract-':
			extract_csv()
			show_extracted()
			break
	orgdata_window.close()
	return

#####
# Extract data
#####
def extract_csv():
	for i, line in enumerate(var.csvlist):
		if set(var.datalabel_dic.values()).issubset(set(line)) :
			c_label = i
			count = c_label + var.skip + 1
			tmp_dic = {}
			for k, v in var.datalabel_dic.items():
				pos = var.csvlist[c_label].index(v)
				tmp = []
				for dataline in var.csvlist[count:]:
					if dataline[pos] != '':
						tmp.append(float(dataline[pos]))
					else:
						break
				tmp_dic[k] = tmp
				if k == 'Temp.':
					temp = round(sum(tmp)/len(tmp), 1)
					var.temp_list.append(temp)
			
			horizontal = []
			vertical = list(tmp_dic.values())
			for col in range(len(vertical[0])):
				horizontal.append([vertical[i][col] for i in range(np.array(vertical).shape[0])])
			var.moddata[temp] = [horizontal, tmp_dic]