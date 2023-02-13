#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
# import openpyxl
# import csv
import numpy as np
import matplotlib.pyplot as plt
# import os
import pickle

import ShowOriginal as org
import variables as var

#####
# Main Window
#####
def make_mainwindow():
	frame_fileselect = sg.Frame('Original Data File',[
							[sg.Text('Original File:', size=(16,1), justification='c'),
							sg.Text('not selected yet.', 
							key = '-orgdata-', 
							relief=sg.RELIEF_RAISED, 
							border_width=2, 
							size = (30,1),
							justification='c')
							],
							[sg.Button('Read File', 
		  					key='-read_org-', 
							size=(15,1)),
							sg.Button('Show Data', 
		 					key='-show_org-', 
							disabled=True, size=(15,1)),
							]
							]
						)
	frame_savedatafile = sg.Frame('Data File',[
							[sg.Text('Data File:', size=(16,1), justification='c'),
							sg.Text('not saved yet.', 
							key = '-savedata-', 
							relief=sg.RELIEF_RAISED, 
							border_width=2, 
							size = (30,1),
							justification='c')
							],
							[sg.Button('Load Data', 
		  					key='-load_data-', 
							size=(15,1)),
							sg.Button('Save Data', 
		 					key='-save_data-', 
							disabled=True, size=(15,1)),
							]
							]
						)
	frame_extracted = sg.Frame('Extract Data',[
							[
							sg.Text('Extracted Data:', size=(16,1), justification='c'),
							sg.Text('not extracted yet.', 
							key = '-exdata-', 
							relief=sg.RELIEF_RAISED, border_width=2, 
							size = (30,1),
							justification='c')],
							[sg.Button('Show Extracted', 
		 					key='-show_ext-', 
							disabled=True, size=(15,1))]
							]
						)
	frame_shift = sg.Frame('Tune Shift Parameters',[
							[sg.Text('Parameters:', size=(16,1), justification='c'),
							sg.Text('not made yet.', 
							key = '-shiftdata-', 
							relief=sg.RELIEF_RAISED, 
							border_width=2, 
							size = (30,1), 
							justification='c')],
							[sg.Button('Tune parameters', 
		  					key='-tune-', 
							disabled=True, size=(15,1)
							)]
							]
						)
	main_layout = [
					[frame_fileselect],
					[frame_savedatafile],
					[frame_extracted],
					[frame_shift],
					[sg.Button('Exit', 
					key = '-exit-',
					size=(15,1))]
				]
	return sg.Window('Main Window', main_layout)

#####
def mainwindow():
	# Main Window
	main_window = make_mainwindow()
	# Main Loop
	while True:
		event, values = main_window.read()
		### Main Window Procedure
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		# Concerning Original Data File
		elif event == '-read_org-':
			org.select_original(main_window)
		elif event == '-show_org-' and var.datalist != '':
			org.show_original(main_window)
		# Target Data file
		elif event == '-load-':
			load_binary(main_window, event, values)
		# Extract Data from Original
		elif event == '-show_ext-':
			var.temp_list = sorted(list(var.moddata.keys()))
			show_extracted()
		# Modify Shift Parameters
		elif event == '-tune-':
			tune_parameters(main_window, event, values)
	main_window.close()
	return



















# def show_original(main_window):
# 	main_window.hide()
# 	show_orgdata()
# 	main_window.un_hide()
# 	if var.binaryfile != '':
# 		main_window['-exdata-'].update(var.binaryfile)
# 		main_window['-show_ext-'].update(disabled=False)
# 	return

# def show_orgdata():
# 	ncolm_list = [str(x) for x in range(len(var.datalist[0]))]
# 	cond_label = list(var.datalabel_dic.keys())
# 	cond_data = [[var.datalabel_dic[key] for key in list(var.datalabel_dic.keys())]]

# 	frame_table = sg.Frame(
# 		'Selected Data Table', [
# 			[sg.Text('Selected File:'), sg.Text(var.filename[0])],
# 			[sg.Text('Sheet name:'), sg.Text(var.filename[1])],
# 			[sg.Table(var.datalist, headings=ncolm_list, display_row_numbers=True, def_col_width=6, auto_size_columns=False, vertical_scroll_only=False, num_rows=20)]
# 		]
# 	)
# 	frame_extract = sg.Frame(
# 		'Extract Data', [
# 			[sg.Table(cond_data, headings=cond_label, def_col_width=16, justification='center', auto_size_columns=False, num_rows=1)],
# 			[sg.Text('Skip Columns:', size=(10,1)), sg.Text(var.skip, size=(4,1))],
# 			[sg.Button("Extract", key='-extract-')]
# 		]
# 	)
# 	layout_orgtable = [
# 			[frame_table],
# 			[frame_extract],
# 			[sg.Button('Exit', key = '-exit-')]
# 	]
# 	orgdata_window = sg.Window('Selected Data', layout_orgtable, finalize=True, size=(800,600), resizable=True)

# 	while True:
# 		event, values = orgdata_window.read()
# 		if event in [sg.WIN_CLOSED, '-exit-']:
# 			break
# 		elif event == '-extract-':
# 			extract_datalist()
# 			show_extracted()
# 			break
# 	orgdata_window.close()
# 	return



#####
# Extract data
#####
def extract_datalist():
	for i, line in enumerate(var.datalist):
		if set(var.datalabel_dic.values()).issubset(set(line)) :
			c_label = i
			count = c_label + var.skip + 1
			tmp_dic = {}
			for k, v in var.datalabel_dic.items():
				pos = var.datalist[c_label].index(v)
				tmp = []
				for dataline in var.datalist[count:]:
					if dataline[pos] not in ['', None]:
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

def show_extracted():
	fig = ''
	# ウィンドウのレイアウト
	frame_exfile = sg.Frame(
		'Extracted data file', [
									[sg.Text('Extracted File:', size = (12,1)), 
     								sg.Text('not extracted yet', key = '-exdata-', relief=sg.RELIEF_RAISED, border_width=2, size = (66,1))],
								    [sg.Button('Save Data', key = '-save-', size=(10,2))]
								]
							)
	frame_table = sg.Frame(
		'Extracted data table', [
									[
									sg.Column(
										[
										[sg.Listbox(var.temp_list, key='-temp-', size=(8,3))],
										[sg.Button('Select',key='-select-', size=(8,2))]
										]),
									sg.Table(
										[[None for i in list(var.datalabel_dic.keys())]], headings=list(var.datalabel_dic.keys()), key='-table-', def_col_width=12, auto_size_columns=False, vertical_scroll_only=False, num_rows = len(var.moddata[var.temp_list[0]][0]))
									]
								]
							)
	col_all = [
				[sg.Radio("Storage Modulus", group_id='all', key='-storage_a-')],
				[sg.Radio("Loss Modulus", group_id='all', key='-loss_a-')],
				[sg.Radio("tan_d", group_id='all', key='-tan_d_a-', default=True)]
				]
	col_sel = [
				[sg.Radio("Both Moduli", group_id='select', key='-both-')],
				[sg.Radio("All", group_id='select', key='-all-')],
				[sg.Radio("tan_d", group_id='select', key='-tan_d_s-', default=True)]
				]
	frame_all = sg.Frame(
					'Draw Graph', [
						[
						sg.Button('Draw All Graph', key = '-draw_all-', size=(20,5)), 
      					sg.Column(col_all, justification='l')
						]
					])
	frame_sel = sg.Frame(
					'Draw Graph', [ 
						[
						sg.Button('Draw Selected Graph', key = '-draw-', disabled=True, size=(20,5)), 
						sg.Column(col_sel, justification='l')
						]
					])
	extracted_layout=[
				[frame_exfile],
				[frame_table],
				[frame_all, frame_sel],
				[sg.Button('Exit', key = '-exit-', size=(10,2))]
				]
	ex_window = sg.Window('Check and Draw Graph for Extracted data', extracted_layout, finalize=True)

	if var.binaryfile:
		ex_window['-exdata-'].update(var.binaryfile)

	while True:
		event, values = ex_window.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == '-select-':
			if values['-temp-'] != []:
				temperature = values['-temp-'][0]
				ex_window['-table-'].update(var.moddata[temperature][0])
				#
				ex_window['-save-'].update(disabled=False)
				ex_window['-draw-'].update(disabled=False)
			else:
				sg.popup_error('Proper Temperature is not selected')
		elif event == '-save-':
			var.binaryfile = sg.popup_get_file('save', save_as=True, file_types=(("Binary Data File", ".pcl"),))
			save_binary()
			ex_window['-exdata-'].update(var.binaryfile)
		elif event == '-draw-':
			if fig != '':
				plt.close()
			target = ''
			if values['-both-'] == True:
				target = 'both'
			if values['-all-'] == True:
				target = 'all'
			if values['-tan_d_s-'] == True:
				target = 'tand'
			draw_siglegraph(target, temperature)
		elif event == '-draw_all-':
			if fig != '':
				plt.close()
			target = ''
			if values['-storage_a-'] == True:
				target = 'Str. Mod.'
			if values['-loss_a-'] == True:
				target = 'Loss Mod.'
			if values['-tan_d_a-'] == True:
				target = 'Tan_d'
			draw_allgraphs(target)

	ex_window.close()

def save_binary():
	with open(var.binaryfile, mode='wb') as f:
		pickle.dump(var.moddata, f)
	return

def draw_siglegraph(target, temperature):
	if target == 'tand':
		fig, ax = plt.subplots()
		ax.plot(var.moddata[temperature][1]['Ang. Freq.'], var.moddata[temperature][1]['Tan_d'], label=r'Tan $\delta$', c="r")
		ax.set_ylabel(r'Tan $\delta$')  # y軸ラベル
		ax.set_xlabel('Freq.')  # x軸ラベル
		ax.set_title('Measured Raw Data for T=' + str(temperature)) # グラフタイトル
		ax.semilogx(base=10)
		ax.semilogy(base=10)
		ax.legend(borderaxespad=0)
	elif target == 'both':
		fig, ax = plt.subplots()
		ax.plot(var.moddata[temperature][1]['Ang. Freq.'], var.moddata[temperature][1]['Str. Mod.'], label="G'", c="r")
		ax.plot(var.moddata[temperature][1]['Ang. Freq.'], var.moddata[temperature][1]['Loss Mod.'], label= 'G"', c="g")
		ax.set_ylabel('Storage and Loss Moduli')  # y軸ラベル
		ax.set_xlabel('Freq.')  # x軸ラベル
		ax.set_title('Measured Raw Data for T=' + str(temperature)) # グラフタイトル
		ax.semilogx(base=10)
		ax.semilogy(base=10)
		ax.legend(borderaxespad=0)
	elif target == 'all':
		fig, ax1 = plt.subplots()
		ax2 = ax1.twinx()
		ax1.plot(var.moddata[temperature][1]['Ang. Freq.'], var.moddata[temperature][1]['Str. Mod.'], label="G'", c="r")
		ax1.plot(var.moddata[temperature][1]['Ang. Freq.'], var.moddata[temperature][1]['Loss Mod.'], label= 'G"', c="g")
		ax2.plot(var.moddata[temperature][1]['Ang. Freq.'], var.moddata[temperature][1]['Tan_d'], label=r'Tan $\delta$', c="b")
		ax1.set_ylabel('Storage and Loss Moduli')  # y軸ラベル
		ax2.set_ylabel(r'Tan $\delta$')  # y軸ラベル
		ax1.set_xlabel('Freq.')  # x軸ラベル
		ax1.set_title('Measured Raw Data for T=' + str(temperature)) # グラフタイトル
		ax1.semilogx(base=10)
		ax1.semilogy(base=10)
		ax2.semilogy(base=10)
		h1, l1 = ax1.get_legend_handles_labels()
		h2, l2 = ax2.get_legend_handles_labels()
		ax1.legend(h1 + h2, l1 + l2, borderaxespad=0)

	plt.show(block=False)
	return

def draw_allgraphs(target):
	fig, ax = plt.subplots()

	for temp in var.temp_list:
		ax.plot(var.moddata[temp][1]['Ang. Freq.'], var.moddata[temp][1][target], label='T='+str(temp))
	ax.set_xlabel('Freq.')  # x軸ラベル
	if target == 'Tan_d':
		ax.set_ylabel(r'Tan $\delta$')  # y軸ラベル
	elif target == 'Str. Mod.':
		ax.set_ylabel('Storage Modulus')  # y軸ラベル
	elif target == 'Loss Mod.':
		ax.set_ylabel('Loss Modulus')  # y軸ラベル
	ax.set_title('Measured Raw Data for all Temperature') # グラフタイトル
	ax.semilogx(base=10)
	ax.semilogy(base=10)
	ax.legend(borderaxespad=0, ncol=2)

	plt.show(block=False)
	return



































def load_binary(main_window, event, values):
	var.binaryfile = sg.popup_get_file('get file', file_types=(("Binary Data File", ".pcl"),))
	if var.binaryfile:
		with open(var.binaryfile, mode='rb') as f:
			var.moddata = pickle.load(f)
		main_window['-exdata-'].update(var.binaryfile)
		main_window['-show_ext-'].update(disabled=False)
		main_window['-tune-'].update(disabled=False)
	return

def tune_parameters(main_window, event, values):
	if var.binaryfile:
		with open(var.binaryfile, mode='rb') as f:
			var.moddata = pickle.load(f)
	var.temp_list = sorted(list(var.moddata.keys()))
	main_window.hide()
	show_tune()
	main_window.un_hide()
	return


if __name__ == '__main__':
	mainwindow()