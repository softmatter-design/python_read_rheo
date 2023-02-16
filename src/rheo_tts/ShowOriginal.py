#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import openpyxl
import csv
import os
import variables as var

# Read Original Data 
def select_original():
	datalist = []
	targetfile = sg.popup_get_file('Select Original Datafile !', 
				file_types=(("Excel Files", ".xlsx"),("CSV Files", ".csv")), 
				size=(60,10))
	if targetfile not in ['', None]:
		if os.path.splitext(targetfile)[1] == '.xlsx':
			wb = openpyxl.load_workbook(targetfile)
			sheetlist = wb.sheetnames
			worksheet =selectsheet(sheetlist)
			ws = wb[worksheet]
			for row in ws.rows:
				datalist.append([cell.value for cell in row])
		elif os.path.splitext(targetfile)[1] == '.csv':
			with open(targetfile, encoding='utf8') as f:
				datalist = list(csv.reader(f))
			worksheet = ''
		#
		var.yourdata_dic['originaldata']['filename'] = targetfile
		var.yourdata_dic['originaldata']['sheetname'] = worksheet
		var.yourdata_dic['originaldata']['originaldata_list'] = datalist
	return

def selectsheet(sheetlist):
	layout = [
			[sg.Text('Select sheet from listbox below')],
			[sg.Listbox(sheetlist, key = '-sheet-', size=(40, len(sheetlist)))],
			[sg.Button('Select', key='-select-', size=(20,1))]
			]
	sub_selectwindow = sg.Window('Select sheet', layout)

	while True:
		event, values = sub_selectwindow.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == '-select-':
			worksheet = values['-sheet-'][0]
			x, y = sub_selectwindow.current_location()
			value = sg.popup(f'Selected work sheet: "{worksheet}"', location = (x+200, y-100), no_titlebar=True)
			if value == 'OK':
				break
	sub_selectwindow.close()
	return worksheet



# Show Original Data 
def show_original():
	filename = var.yourdata_dic['originaldata']['filename']
	sheetname = var.yourdata_dic['originaldata']['sheetname']
	datalist = var.yourdata_dic['originaldata']['originaldata_list']
	comment =  var.yourdata_dic['originaldata']['comment']

	if datalist == []:
		sg.popup_error('Proper Original data is not selected yet !!\nBack to main menu !!', title='Error')
		return

	ncolm_list = [str(x) for x in range(len(datalist[0]))]
	rclick_table = ["",
				["Copy"]
				]
	rclick_comment = ["",
				["Paste"]
				]
	frame_table = sg.Frame(
		'Selected Original Data Table', [
			[sg.Text('Selected File:', 
			size = (10,1)), 
    		sg.Text(filename, 
			size = (60,1))],
			[sg.Text('Sheet name:', 
			size = (10,1)), 
    		sg.Text(sheetname, 
			size = (30,1))],
			
			[sg.Table(datalist, 
	     	headings=ncolm_list, 
			display_row_numbers=True, 
			def_col_width=6, 
			auto_size_columns=False, 
			vertical_scroll_only=False, 
			num_rows=30,
			enable_events=True, 
			select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
			key='-data_table-', 
			right_click_menu=rclick_table)]
		]
	)
	frame_savecommennt = sg.Frame(
		'Make Comment', [
				[sg.Multiline(comment, 
				size=(130, 10), 
				key='-comment-',
				enable_events=True, 
				right_click_menu=rclick_comment)
				]
			]
	)
	layout_orgtable = [
			[frame_table],
			[frame_savecommennt],
			[
			sg.Button('Exit', 
	     	key = '-exit-', 
			size = (16,1))]
	]
	orgdata_window = sg.Window('Selected Data', layout_orgtable, finalize=True, resizable=True, size=(900,850))
	
	while True:
		event, values = orgdata_window.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			var.yourdata_dic['originaldata']['comment'] = values['-comment-']
			break
		elif event == 'Copy':
			copytext = ''
			for num in values['-data_table-']:
				for cell in datalist[num]:
					if cell not in ['', None]:
						copytext += str(cell) + '\t'
				copytext += '\n'
			sg.clipboard_set(copytext)
		elif event == 'Paste':
			orgdata_window['-comment-'].Widget.insert("insert", sg.clipboard_get())
		elif event == '-comment-':
			var.yourdata_dic['originaldata']['comment'] = values['-comment-']
	orgdata_window.close()
	return

