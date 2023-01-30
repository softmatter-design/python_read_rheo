#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import csv
import numpy as np
import variables as var
#####
def main():
	# Main Window
	main_window = make_mainwindow()

	csvfile = ''
	# Main Loop
	while True:
		event, values = main_window.read()

		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		
		### Main Window Procedure
		if event == '-select_org-':
			csvfile = sg.popup_get_file('get file', file_types=(("CSV Files", ".csv"),))
			with open(csvfile, encoding='utf8') as f:
				csvlist = list(csv.reader(f))
			main_window['-orgdata-'].update(csvfile)
		if event == '-show_org-' and csvfile != '':
			main_window.hide()
			res = show_orgdata(csvfile, csvlist)
			print(res)
			main_window.un_hide()

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
							sg.Button('Show Data', key='-show_org-')]
							]
						)
	
	frame_extracted = sg.Frame('Extracted Data File',[
							[#sg.Text('Extracted File:', size = (12,1)), 
							sg.Text('not extracted yet', key = '-orgdata-', relief=sg.RELIEF_RAISED, border_width=2, size = (60,1))],
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
def show_orgdata(csvfile, csvlist):
	ncolm_list = [str(x) for x in range(len(csvlist[0]))]
	cond_label = list(var.datalabel_dic.keys())
	cond_data = [[var.datalabel_dic[key] for key in list(var.datalabel_dic.keys())]]
	print(cond_label)
	print(cond_data)

	frame_table = sg.Frame(
		'Selected Data Table', [
			[sg.Text('Selected Data File:'), sg.Text(csvfile)],
			[sg.Table(csvlist, headings=ncolm_list, display_row_numbers=True, def_col_width=6, auto_size_columns=False, vertical_scroll_only=False, num_rows=20)]
		]
	)
	frame_extract = sg.Frame(
		'Extract Data', [
			[sg.Table(cond_data, headings=cond_label, def_col_width=16, justification='center', auto_size_columns=False, num_rows=2)],
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
			extract_csv(csvlist)

		elif event == '-ok-':
			res = True
			break

	orgdata_window.close()
	return res

#####
# Extract data
#####
def extract_csv(csvlist):
	datalabel = list(var.datalabel_dic.keys())

	moddata = {}
	temp_list = []
	for i, line in enumerate(csvlist):
		if set(var.datalabel_dic.values()).issubset(set(line)) :
			c_label = i
			count = c_label + var.skip + 1
			tmp_dic = {}
			for k, v in var.datalabel_dic.items():
				pos = csvlist[c_label].index(v)
				tmp = []
				for dataline in csvlist[count:]:
					if dataline[pos] != '':
						tmp.append(float(dataline[pos]))
					else:
						break
				tmp_dic[k] = tmp
				if k == 'Temp.':
					temperature = round(np.mean(tmp), 1)
					temp_list.append(temperature)
			
			horizontal = []
			vertical = list(tmp_dic.values())
			for col in range(len(vertical[0])):
				horizontal.append([vertical[i][col] for i in range(np.array(vertical).shape[0])])
			moddata[temperature] = [horizontal, tmp_dic]

	# ウィンドウのレイアウト
	extracted_layout=[
			[sg.Text('Selected Temp.:', size=(12,1)), 
			sg.Text('not selected yet', key = '-selectedtemp-', relief=sg.RELIEF_RAISED, border_width=2, size = (8,1))], 
			[sg.Listbox(temp_list, key='-temp-', size=(None, 3)),sg.Button('Select',key='-select-')],
			[sg.Table([[None for i in datalabel]], headings=datalabel, key='-table-', def_col_width=10, auto_size_columns=False, vertical_scroll_only=False, num_rows=16)]
			]
	ex_window = sg.Window('Extracted data table !', extracted_layout, resizable = True, finalize=True)

	while True:
		event, values = ex_window.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		if event == '-select-':
			temperature = values['-temp-'][0]
			ex_window['-table-'].update(moddata[temperature][0])
			ex_window['-selectedtemp-'].update(temperature)
	ex_window.close()

if __name__ == '__main__':
	main()