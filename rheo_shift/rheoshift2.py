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
# Extract data
#####
def extracted_window(datalabel, templist):
	
	# ウィンドウのレイアウト
	extracted_layout=[
			[sg.Text('Selected Temp.:', size=(12,1)), 
			sg.Text('not selected yet', key = '-selectedtemp-', relief=sg.RELIEF_RAISED, border_width=2, size = (8,1))], 
			[sg.Listbox(templist, key='-temp-', size=(None, 3)),sg.Button('Select',key='-select-')],
			[sg.Table([[None for i in datalabel]], headings=datalabel, key='-table-', def_col_width=10, auto_size_columns=False, vertical_scroll_only=False, num_rows=16)]
			]
	return sg.Window('Extracted data table !', extracted_layout, resizable = True, finalize=True)
	
def extract_csv(csvlist):
	datalabel_dic = {
			'Temp.':'温度', 
			'Ang. Freq.':'角周波数', 
			'Str. Mod.':'貯蔵弾性率', 
			'Loss. Mod.':'損失弾性率', 
			'Tan_d':'損失正接',
			}
	skip = 1

	datalabel = list(datalabel_dic.keys())

	moddata = {}
	temp_list = []
	for i, line in enumerate(csvlist):
		if set(datalabel_dic.values()).issubset(set(line)) :
			c_label = i
			count = c_label + skip + 1
			tmp_dic = {}
			for k, v in datalabel_dic.items():
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

	ex_window = extracted_window(datalabel, temp_list)
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