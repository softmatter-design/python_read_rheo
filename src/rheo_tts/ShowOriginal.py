#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import openpyxl
import csv
import os
import variables as var

# Show Original Data 
def show_original():
	if var.originaldata['targetfile'] == '':
		select_original()
	else:
		original_initialize()
	# Make Window
	orgdata_window = make_original_window()
	# Main Loop
	while True:
		event, values = orgdata_window.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == 'Copy':
			copytext = ''
			for num in values['-data_table-']:
				for cell in var.originaldata_list[num]:
					if cell not in ['', None]:
						copytext += str(cell) + '\t'
				copytext += '\n'
			sg.clipboard_set(copytext)
		elif event == 'Paste':
			orgdata_window['-comment-'].Widget.insert("insert", sg.clipboard_get())
		elif event == '-change-':
			select_original()
			orgdata_window['-file-'].Update(var.targetfile)
			orgdata_window['-ws-'].Update(var.worksheet)
			orgdata_window['-data_table-'].Update(var.originaldata_list)
			orgdata_window['-comment-'].Update('')
	
	var.originaldata['comment'] = values['-comment-']
	var.yourdata_dic['originaldata'] = var.originaldata
	orgdata_window.close()
	return

# Read Original Data 
def select_original():
	var.targetfile = sg.popup_get_file('Select Original Datafile !', 
				file_types=(("Excel Files", ".xlsx"),("CSV Files", ".csv")), 
				size=(60,10))
	if var.targetfile not in ['', None]:
		if os.path.splitext(var.targetfile)[1] == '.xlsx':
			wb = openpyxl.load_workbook(var.targetfile)
			sheetlist = wb.sheetnames
			if len(sheetlist) >1:
				selectsheet(sheetlist)
			else:
				var.worksheet = sheetlist[0]
			ws = wb[var.worksheet]
			for row in ws.rows:
				var.originaldata_list.append([cell.value for cell in row])
		elif os.path.splitext(var.targetfile)[1] == '.csv':
			with open(var.targetfile, encoding='utf8') as f:
				var.originaldata_list = list(csv.reader(f))
			var.worksheet = ''
		#
		var.originaldata['targetfile'] = var.targetfile
		var.originaldata['worksheet'] = var.worksheet
		var.originaldata['originaldata_list'] = var.originaldata_list
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
			var.worksheet = values['-sheet-'][0]
			# x, y = sub_selectwindow.current_location()
			value = sg.popup(f'Selected work sheet: "{var.worksheet}"', 
		    				# location = (x+200, y-100), 
							no_titlebar = True
							)
			if value == 'OK':
				break
	sub_selectwindow.close()
	return

def original_initialize():
	var.targetfile= var.originaldata['targetfile']
	var.worksheet = var.originaldata['worksheet']
	var.originaldata_list = var.originaldata['originaldata_list']
	var.comment = var.originaldata['comment']
	return

def make_original_window():
	ncolm_list = [str(x) for x in range(len(var.originaldata_list[0]))]
	rclick_table = ["",
				["Copy"]
				]
	rclick_comment = ["",
				["Paste"]
				]
	frame_table = sg.Frame('Selected Original Data Table', 
			 [
				[sg.Text('Selected File:', 
				size = (10,1)), 
				sg.Text(var.targetfile, 
				size = (80,1),
				key='-file-')],
				[sg.Text('Sheet name:', 
				size = (10,1)), 
				sg.Text(var.worksheet, 
				size = (30,1),
				key='-ws-')],
				[sg.Button('Change File', 
				key = '-change-', 
				size = (20,1))],
				[sg.Table(var.originaldata_list, 
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
	frame_savecommennt = sg.Frame('Make Comment', [
					[sg.Multiline(var.comment, 
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
				[sg.Button('Back to MAIN', 
				key = '-exit-', 
				size = (20,1))]
		]
	window = sg.Window('Selected Data', layout_orgtable, finalize=True, resizable=True)
	# , size=(900,850))

	return window
