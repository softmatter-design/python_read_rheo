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
			if var.binaryfile:
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
				[sg.Radio("Storage Modulus", group_id='item', key='-storage_a-')],
				[sg.Radio("Loss Modulus", group_id='item', key='-loss_a-')],
				[sg.Radio("tan_d", group_id='item', key='-tan_d_a-', default=True)]
				]
	col_sel = [
				[sg.Checkbox("Storage Modulus", key='-storage_s-')],
				[sg.Checkbox("Loss Modulus", key='-loss_s-')],
				[sg.Checkbox("tan_d", key='-tan_d_s-', default=True)]
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
				var.temperature = values['-temp-'][0]
				ex_window['-table-'].update(var.moddata[var.temperature][0])
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
			target = []
			if values['-storage_s-'] == True:
				target.append('Str. Mod.')
			if values['-loss_s-'] == True:
				target.append('Loss. Mod.')
			if values['-tan_d_s-'] == True:
				target.append('Tan_d')
			print(target)
			# 
			draw_siglegraph(target)
		elif event == '-draw_all-':
			target = []
			if values['-storage_a-'] == True:
				target.append('Str. Mod.')
			if values['-loss_a-'] == True:
				target.append('Loss. Mod.')
			if values['-tan_d_a-'] == True:
				target.append('Tan_d')
			print(target)
			draw_allgraphs(target)
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

def draw_allgraphs(target):
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