#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import csv
import numpy as np
import variables as var
import matplotlib.pyplot as plt
import pickle
#####
def main():
	# Main Window
	main_window = make_mainwindow()
	# Main Loop
	while True:
		event, values = main_window.read()
		### Main Window Procedure
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == '-select_org-':
			var.csvfile = sg.popup_get_file('get file', file_types=(("CSV Files", ".csv"),))
			with open(var.csvfile, encoding='utf8') as f:
				var.csvlist = list(csv.reader(f))
			main_window['-orgdata-'].update(var.csvfile)
			main_window['-show_org-'].update(disabled=False)
		elif event == '-show_org-' and var.csvfile != '':
			main_window.hide()
			res = show_orgdata()
			main_window.un_hide()
			if var.binaryfile != '':
				main_window['-exdata-'].update(var.binaryfile)
				main_window['-show_ext-'].update(disabled=False)
		elif event == '-load-':
			var.binaryfile = sg.popup_get_file('get file', file_types=(("Binary Data File", ".pcl"),))
			with open(var.binaryfile, mode='rb') as f:
				var.moddata = pickle.load(f)
			main_window['-exdata-'].update(var.binaryfile)
			main_window['-show_ext-'].update(disabled=False)
		elif event == '-show_ext-':
			show_extracted()
	main_window.close()

	return

#####
# Main Window
#####
def make_mainwindow():
	frame_fileselect = sg.Frame('Select Data File',[
							[#sg.Text('Original Data File:', size = (12,1)), 
							sg.Text('not selected yet', key = '-orgdata-', relief=sg.RELIEF_RAISED, border_width=2, size = (60,1))],
							[sg.Text('', key = '-worksheet-')],
							[sg.Button('Select File', key='-select_org-'),
							sg.Button('Show Data', key='-show_org-', disabled=True)]
							]
						)
	
	frame_extracted = sg.Frame('Extracted Data File',[
							[#sg.Text('Extracted File:', size = (12,1)), 
							sg.Text('not extracted yet', key = '-exdata-', relief=sg.RELIEF_RAISED, border_width=2, size = (60,1))],
							[sg.Button('Load Data File', key='-load-'),
							sg.Button('Show Extracted', key='-show_ext-', disabled=True)]
							]
						)

	frame_shift = sg.Frame('Tune Shift Parameters',[
							[sg.Text('not extracted yet', key = '-orgdata-', relief=sg.RELIEF_RAISED, border_width=2, size = (60,1))],
							[sg.Button('Select', key='-select1-', disabled=True),
							sg.Button('Show', key='-show_org-', disabled=True)]
							]
						)

	main_layout = [
					[frame_fileselect],
					[frame_extracted],
					[sg.Button('Exit', key = '-exit-')]
				]
	return sg.Window('Main Window', main_layout)



#####
# Show Original Data 
#####
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

	res = None
	while True:
		event, values = orgdata_window.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == '-extract-':
			extract_csv()
			show_extracted()

		elif event == '-ok-':
			res = True
			break

	orgdata_window.close()
	return res

#####
# Extract data
#####
def extract_csv():
	# datalabel = list(var.datalabel_dic.keys())

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
					temp = round(np.mean(tmp), 1)
					var.temp_list.append(temp)
			
			horizontal = []
			vertical = list(tmp_dic.values())
			for col in range(len(vertical[0])):
				horizontal.append([vertical[i][col] for i in range(np.array(vertical).shape[0])])
			var.moddata[temp] = [horizontal, tmp_dic]

def show_extracted():
	var.temp_list = sorted(list(var.moddata.keys()))
	# ウィンドウのレイアウト
	frame_graph = sg.Frame(
					'Draw Graph', [
					[sg.Button('Draw Selected Graph', key = '-draw-', disabled=True),
					sg.Button('Draw All Graph', key = '-draw_all-'), 
					sg.Button('Clear Graph', key = '-clear-')],
					[sg.Radio("Storage Modulus", group_id='item', key='-storage-')],
					[sg.Radio("Loss Modulus", group_id='item', key='-loss-')],
					[sg.Radio("tan_d", group_id='item', key='-tan_d-', default=True)],
					[sg.Radio("Both Moduli", group_id='item', key='-both-')],
					[sg.Radio("All data", group_id='item', key='-all-')]
					])
	extracted_layout=[
			[sg.Spin(var.temp_list, key='-temp-'),
			sg.Button('Select',key='-select-')],
			[sg.Table([[None for i in list(var.datalabel_dic.keys())]], headings=list(var.datalabel_dic.keys()), key='-table-', def_col_width=10, auto_size_columns=False, vertical_scroll_only=False, num_rows = len(var.moddata[var.temp_list[0]][0]))],
			[frame_graph],
			[sg.Button('Save Data', key = '-save-', disabled=True), sg.Button('Exit', key = '-exit-')]
			]
	ex_window = sg.Window('Extracted data table !', extracted_layout, resizable = True, finalize=True)

	while True:
		event, values = ex_window.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == '-select-':
			if values['-temp-'] != []:
				var.temperature = values['-temp-'][0]
				ex_window['-table-'].update(var.moddata[var.temperature][0])
				#
				ex_window['-save-'].update(disabled=False)
				ex_window['-draw-'].update(disabled=False)
			else:
				value = sg.popup_error('Proper Temperature is not selected')
		elif event == '-save-':
			var.binaryfile = sg.popup_get_file('save', save_as=True, file_types=(("Binary Data File", ".pcl"),))
			save_binary()
		elif event == '-draw-':
			# Select
			if values['-storage-'] == True:
				target = 
			# 
			draw_siglegraph(target)
			
		elif event == '-draw_all-':
			draw_allgraphs()
		elif event == '-clear-' and var.fig != '':
			plt.close()

	ex_window.close()

def save_binary():
	with open(var.binaryfile, mode='wb') as f:
		pickle.dump(var.moddata, f)
	return

def draw_siglegraph(target):
	var.fig, ax = plt.subplots()

	ax.plot(var.moddata[var.temperature][1]['Ang. Freq.'], var.moddata[var.temperature][1]['Tan_d'], label='T='+str(var.temperature))
	ax.set_xlabel('Freq.')  # x軸ラベル
	ax.set_ylabel(r'Tan $\delta$')  # y軸ラベル
	ax.set_title('Measured Raw Data for T=' + str(var.temperature)) # グラフタイトル
	ax.semilogx(base=10)
	ax.legend(borderaxespad=0, ncol=2)

	plt.show(block=False)

	return

def draw_allgraphs():
	var.fig, ax = plt.subplots()

	for temp in var.temp_list:
		ax.plot(var.moddata[temp][1]['Ang. Freq.'], var.moddata[temp][1]['Tan_d'], label='T='+str(temp))
	ax.set_xlabel('Freq.')  # x軸ラベル
	ax.set_ylabel(r'Tan $\delta$')  # y軸ラベル
	ax.set_title('Measured Raw Data ALL') # グラフタイトル
	ax.semilogx(base=10)
	ax.legend(borderaxespad=0, ncol=2)

	plt.show(block=False)

	return

if __name__ == '__main__':
	main()