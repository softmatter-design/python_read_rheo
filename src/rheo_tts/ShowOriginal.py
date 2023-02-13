#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import openpyxl
import csv
import os
import variables as var

# Read Original Data 
def select_original(main_window):
	main_window.hide()
	isfile = readfile()
	main_window.un_hide()
	if isfile:
		main_window['-orgdata-'].update('Already Selected !', text_color='red')
		main_window['-show_org-'].update(disabled=False)
	return

def readfile():
	targetfile = sg.popup_get_file('Select Original Datafile !', file_types=(("Excel Files", ".xlsx"),("CSV Files", ".csv")), size=(60,10))

	if targetfile:
		if os.path.splitext(targetfile)[1] == '.xlsx':
			wb = openpyxl.load_workbook(targetfile)
			sheetlist = wb.sheetnames
			worksheet =selectsheet(sheetlist)
			ws = wb[worksheet]
			for row in ws.rows:
				var.datalist.append([cell.value for cell in row])
			var.filename = [targetfile, worksheet]
		elif os.path.splitext(targetfile)[1] == '.csv':
			with open(targetfile, encoding='utf8') as f:
				var.datalist = list(csv.reader(f))
			var.filename = [targetfile, '']
		return True
	else:
		return False

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
def show_original(main_window):
	main_window.hide()
	show_orgdata()
	main_window.un_hide()
	if var.binaryfile != '':
		main_window['-exdata-'].update(var.binaryfile)
		main_window['-show_ext-'].update(disabled=False)
	return

def show_orgdata():
	ncolm_list = [str(x) for x in range(len(var.datalist[0]))]
	rclick_menu = ["menu",
				["Copy"]
				]
	frame_table = sg.Frame(
		'Selected Original Data Table', [
			[sg.Text('Selected File:', 
			size = (12,1)), 
    		sg.Text(var.filename[0], 
	      	relief=sg.RELIEF_RAISED, 
			border_width=2, 
			size = (60,1))],
			[sg.Text('Sheet name:', 
			size = (12,1)), 
    		sg.Text(var.filename[1], 
	      	relief=sg.RELIEF_RAISED, 
			border_width=2, 
			size = (40,1))],
			
			[sg.Table(var.datalist, 
	     	headings=ncolm_list, 
			display_row_numbers=True, 
			def_col_width=6, 
			auto_size_columns=False, 
			vertical_scroll_only=False, 
			num_rows=30,
			enable_events=True, 
			select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
			key='-data_table-', 
			right_click_menu=rclick_menu)]
		]
	)
	col_submit = [
				[sg.Text('Comment')], 
    			[sg.Text('not submitted yet.', 
				key='-com_submit-',
	      		relief=sg.RELIEF_RAISED, 
				border_width=2, 
				size = (18,1),
				justification='c')],
				[sg.Button("Submit", 
	       		key='-submit-', 
				size = (18,1))],
				[sg.Button("Paste", 
	       		key='-paste-', 
				size = (18,1))]
				]
	frame_savecommennt = sg.Frame(
		'Make Comment', [
			[sg.Multiline(default_text='You can erase and input multi lines Comment here!\nYou can hit return key for new line', size=(100, 10), key='-comment-'),
			sg.Column(col_submit, justification='l')]
		]
	)
	layout_orgtable = [
			[frame_table],
			[frame_savecommennt],
			[sg.Button("Save Data file", 
			key='-save-', 
			size = (16,1)),
			sg.Button('Exit', 
	     	key = '-exit-', 
			size = (16,1))]
	]
	orgdata_window = sg.Window('Selected Data', layout_orgtable, finalize=True, resizable=True, size=(900,850))

	while True:
		event, values = orgdata_window.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == '-submit-':
			comment = values['-comment-']
			orgdata_window['-com_submit-'].update('   Submitted !', text_color='red')
		elif event == '-paste-':
			newtext = values['-comment-'] + '\n' + copytext
			orgdata_window['-comment-'].update(newtext)
		elif event == 'Copy':
			copytext = ''
			for num in values['-data_table-']:
				for cell in var.datalist[num]:
					if cell not in ['', None]:
						copytext += str(cell) + '\t'
				copytext += '\n'
			print(copytext)
	orgdata_window.close()
	return

