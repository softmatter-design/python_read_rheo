#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import csv
import numpy as np
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
		if event == '-select1-':
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

	main_layout = [
					[
						sg.Text('Original Data File:', size = (15,1)), 
						sg.Text('not selected yet', key = '-orgdata-', relief=sg.RELIEF_RAISED, border_width=5, size = (60,1)),
						sg.Button('Select', key='-select1-'),
						sg.Button('Show', key='-show_org-')
					],
					[
						sg.Text('Modified Data File:', size = (15,1)), 
						sg.Text('not made yet', key = '-moddata-', relief=sg.RELIEF_RAISED, border_width=5, size = (60,1)),
						sg.Button('Select', key='-select2-')
					],
					[sg.Button('Exit', key = '-exit-')]
				]
	return sg.Window('Main Window', main_layout)

def show_orgdata(csvfile, csvlist):
	ncolm_list = [str(x) for x in range(len(csvlist[0]))]
	sublayout1 = [
			[sg.Text('Selected Data File:'), sg.Text(csvfile)],
			[sg.Button("Extract", key='-extract-')],
			[sg.Table(csvlist, headings=ncolm_list, display_row_numbers=True, def_col_width=6, auto_size_columns=False, vertical_scroll_only=False, num_rows=30)]
			
	]
	orgdata_window = sg.Window('Selected Data', sublayout1,finalize=True, size=(800,460), resizable=True)

	res = None

	while True:
		event, values = orgdata_window.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		if event == '-extract-':
			extract_csv(csvlist)
			res = True
			break

	orgdata_window.close()

	return res







#####
# Cut out
#####
def extracted_window(datalabel, templist):
	
	# ウィンドウのレイアウト
	extracted_layout=[
			[sg.Text('Select Temp.:', size=(12,1)), sg.Listbox(templist, key='-temp-', size=(None, 3)),sg.Button('Select',key='-select-')],
			[sg.Table([[None, None, None, None]], headings=datalabel[1:], key='-table-', def_col_width=10, auto_size_columns=False, vertical_scroll_only=False, num_rows=20)]
			]
	return sg.Window('Extracted data table !', extracted_layout, resizable = True, finalize=True)

def extract_csv(csvlist):
	datalabel = ['温度', '角周波数', '貯蔵弾性率', '損失弾性率', '損失正接']
	skip = 1

	temp_list = []
	cut_vertical = []
	cut_horizontal = []
	for i, line in enumerate(csvlist):
		if datalabel[0] in line and datalabel[1] in line:
			start = i
			pos = []
			for item in datalabel:
				pos.append(csvlist[start].index(item))
			count = start + skip + 1
			tmp = []
			for dataline in csvlist[count:]:
				if dataline[0] != '':
					tmp.append([float(dataline[col]) for col in pos])
				else:
					break
			dataarray= np.array(tmp)

			# 温度の列を平均
			temperature = round(np.mean(dataarray[:, 0]), 1)
			# 0 列にある温度の列を ax=1 として除去
			del_data = np.delete(dataarray, 0, 1) 
			# horizontal list を作成
			horiz = []
			horiz.append(temperature)
			horiz.append(del_data.tolist())
			cut_horizontal.append(horiz)
			# vertical list を作成
			vert = []
			for k in range(del_data.shape[1]):
				vert.append(list(del_data[:, k]))
			cut_vertical.append([temperature, vert])
	
	templist = [cut_horizontal[i][0] for i in range(len(cut_horizontal))]

	ex_window = extracted_window(datalabel, templist)
	while True:
		event, values = ex_window.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		if event == '-select-':
			ex_window['-table-'].update(cut_horizontal[0][1])

	ex_window.close()

if __name__ == '__main__':
	main()