#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import openpyxl
import csv
import os
import pickle

import ShowOriginal as org
import variables as var

# Your Data
def load_binary():
	var.binaryfile = sg.popup_get_file('Load', 
				    file_types=(("Binary Data File", ".pcl"),), 
                    size=(60,10))
	if var.binaryfile:
		with open(var.binaryfile, mode='rb') as f:
			var.yourdata_dic = pickle.load(f)
	return

def save_binary():
	var.binaryfile = sg.popup_get_file('Save', 
				    save_as=True, 
				    file_types=(("Binary Data File", ".pcl"),), 
                    size=(60,10))
	with open(var.binaryfile, mode='wb') as f:
		pickle.dump(var.yourdata_dic, f)
	return

# Show Your Data 
def show_yours():

	rclick_table = ["",
				["Copy"]
				]
	rclick_comment = ["",
				["Paste"]
				]
	frame_original = sg.Frame(
		'Original Data', [
			[sg.Text('Original Data:', 
			size = (10,1)), 
    		sg.Text('', 
			size = (60,1))],
			[sg.Button('Show_Original', 
	     	key = '-show_org-', 
			size = (16,1))]
				]
			)
	frame_extracted = sg.Frame(
		'Extracted Data', [
			[sg.Text('Extracted Data:', 
			size = (10,1)), 
    		sg.Text('', 
			size = (60,1))],
			[sg.Button('Show_Extracted', 
	     	key = '-show_ext-', 
			size = (16,1))]
				]
			)
	frame_parameters = sg.Frame(
		'Shift Parameters', [
			[sg.Text('Shift Parameters:', 
			size = (10,1)), 
    		sg.Text('', 
			size = (60,1))],
			[sg.Button('Show_Parameters', 
	     	key = '-show_param-', 
			size = (16,1))]
				]
			)
	layout_yours = [
			[frame_original],
			[frame_extracted],
			[frame_parameters],
			[
			sg.Button('Exit', 
	     	key = '-exit-', 
			size = (16,1))]
	]
	yours_window = sg.Window('Your Data', layout_yours, finalize=True, resizable=True)
	
	while True:
		event, values = yours_window.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			# var.yourdata_dic['originaldata']['comment'] = values['-comment-']
			break
		elif event == '-show_org-':
			org.show_original()
		# elif event == 'Copy':
		# 	copytext = ''
		# 	for num in values['-data_table-']:
		# 		for cell in datalist[num]:
		# 			if cell not in ['', None]:
		# 				copytext += str(cell) + '\t'
		# 		copytext += '\n'
		# 	sg.clipboard_set(copytext)
		# elif event == 'Paste':
		# 	orgdata_window['-comment-'].Widget.insert("insert", sg.clipboard_get())
		# elif event == '-comment-':
		# 	var.yourdata_dic['originaldata']['comment'] = values['-comment-']
	yours_window.close()
	return