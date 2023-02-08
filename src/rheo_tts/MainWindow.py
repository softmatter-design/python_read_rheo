#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import csv
import numpy as np
import variables as var
import matplotlib.pyplot as plt
import pickle

import variables as var

#####
# Main Window
#####
def make_mainwindow():
	frame_fileselect = sg.Frame('Select Data File',[
							[sg.Text('not selected yet', 
							key = '-orgdata-', 
							relief=sg.RELIEF_RAISED, 
							border_width=2, 
							size = (60,1))],
							[sg.Text('', key = '-worksheet-')],
							[sg.Button('Select File', key='-select_org-'),
							sg.Button('Show Data', 
		 					key='-show_org-', 
							disabled=True)]
							]
						)
	frame_extracted = sg.Frame('Extracted Data File',[
							[sg.Text('not extracted yet', 
							key = '-exdata-', 
							relief=sg.RELIEF_RAISED, border_width=2, 
							size = (60,1))],
							[sg.Button('Load Data File', 
		  					key='-load-'),
							sg.Button('Show Extracted', 
		 					key='-show_ext-', 
							disabled=True)]
							]
						)
	frame_shift = sg.Frame('Tune Shift Parameters',[
							[sg.Text('not made yet', 
							key = '-shiftdata-', 
							relief=sg.RELIEF_RAISED, 
							border_width=2, 
							size = (60,1))],
							[sg.Button('Tune parameters', 
		  					key='-tune-', 
							disabled=True)]
							]
						)
	main_layout = [
					[frame_fileselect],
					[frame_extracted],
					[frame_shift],
					[sg.Button('Exit', 
					key = '-exit-')]
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
		elif event == '-select_org-':
			select_original(main_window, event, values)
		elif event == '-show_org-' and var.csvfile != '':
			show_original(main_window, event, values)
		elif event == '-load-':
			load_binary(main_window, event, values)
		elif event == '-show_ext-':
			var.temp_list = sorted(list(var.moddata.keys()))
			show_extracted()
		elif event == '-tune-':
			tune_parameters(main_window, event, values)
	main_window.close()
	return

def select_original(main_window, event, values):
	var.csvfile = sg.popup_get_file('get file', file_types=(("CSV Files", ".csv"),))
	with open(var.csvfile, encoding='utf8') as f:
		var.csvlist = list(csv.reader(f))
	main_window['-orgdata-'].update(var.csvfile)
	main_window['-show_org-'].update(disabled=False)
	return

def show_original(main_window, event, values):
	main_window.hide()
	show_orgdata()
	main_window.un_hide()
	if var.binaryfile != '':
		main_window['-exdata-'].update(var.binaryfile)
		main_window['-show_ext-'].update(disabled=False)
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