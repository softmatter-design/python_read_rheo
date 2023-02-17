#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
# import os
import pickle

import ShowOriginal as org
import YourData as you
import Extract as ext
import variables as var

#####
# Main Window
#####
def make_mainwindow():
	# Menu
	menu_def = [
			['&OriginalData', 
				['&ReadOriginal  Ctrl+o',
				'&ShowOriginal  Ctrl+w'
				],
			],
     		['&SaveData',
				['&LoadYourData  Ctrl+l',
				'&SaveYourData  Ctrl+s',
				'Show&YourData  Ctrl+s'
				],
			],
			['&Extract', 
				['&Extract     Ctrl+e', 
				'&ShowExtact  Ctrl+w'
				]
			],
			['&TuneShift', 
				['&Tune     Ctrl+t', 
				'&ShowParameter  Ctrl+p'
				]
			],
			['&Help', 
    			['&About']
			],
			['E&xit',  
    			['&Exit  Ctrl+x']
			]
			]
	# Widgets
	frame_fileselect = sg.Frame('Original Data File',[
							[sg.Text('Original File:', size=(16,1), justification='c'),
							sg.Text('not selected yet.', 
							key = '-orgdata-', 
							relief=sg.RELIEF_RAISED, 
							border_width=2, 
							size = (30,1),
							justification='c')
							],
							[sg.Button('Read Original', 
		  					key='-read_org-', 
							size=(14,1)),
							sg.Button('Show Original', 
		 					key='-show_org-', 
							disabled=True, 
							size=(14,1)),
							]
							]
						)
	frame_savedatafile = sg.Frame('Your Data File',[
							[sg.Text('Your Data File:', size=(16,1), justification='c'),
							sg.Text('not saved yet.', 
							key = '-yourdata-', 
							relief=sg.RELIEF_RAISED, 
							border_width=2, 
							size = (30,1),
							justification='c')
							],
							[sg.Button('Load Data', 
		  					key='-load_data-', 
							size=(14,1)),
							sg.Button('Save Data', 
		 					key='-save_data-', 
							size=(14,1)),
							sg.Button('Show Data', 
		 					key='-show_data-', 
							size=(14,1))
							]
							]
						)
	frame_extracted = sg.Frame('Extract Data',[
							[
							sg.Text('Extracted Data:', size=(16,1), justification='c'),
							sg.Text('not extracted yet.', 
							key = '-extdata-', 
							relief=sg.RELIEF_RAISED, border_width=2, 
							size = (30,1),
							justification='c')],
							[sg.Button('Extract Data', 
		 					key='-extract-', 
							disabled=True, 
							size=(14,1))]
							]
						)
	frame_shift = sg.Frame('Tune Shift Parameters',[
							[sg.Text('Parameters:', size=(16,1), justification='c'),
							sg.Text('not made yet.', 
							key = '-shiftdata-', 
							relief=sg.RELIEF_RAISED, 
							border_width=2, 
							size = (30,1), 
							justification='c')],
							[sg.Button('Tune parameters', 
		  					key='-tune-', 
							disabled=True, 
							size=(14,1)
							)]
							]
						)
	# Main Window
	main_layout = [
					[sg.MenuBar(menu_def)],
					[frame_fileselect,
					frame_savedatafile],
					[frame_extracted,
					frame_shift],
					[sg.Button('Exit', 
					key = '-exit-',
					size=(14,1))]
				]
	#
	window = sg.Window('Main Window', main_layout, finalize=True)
	window.bind("<Control-Key-o>", "ReadOriginal  Ctrl+o")
	window.bind("<Control-Key-w>", "ReadOriginal  Ctrl+w")


	window.bind("<Control-Key-l>", "ReadOriginal  Ctrl+l")
	window.bind("<Control-Key-s>", "ReadOriginal  Ctrl+s")

	window.bind("<Control-Key-x>", "ReadOriginal  Ctrl+x")

	window.bind("<Control-Key-c>", "ReadOriginal  Ctrl+c")
	
	window.bind("<Control-Key-t>", "ReadOriginal  Ctrl+t")
	
	window.bind("<Control-Key-y>", "ReadOriginal  Ctrl+y")
	window.bind("<Control-Key-z>", "ReadOriginal  Ctrl+z")
	window.bind("<Control-Key-g>", "ReadOriginal  Ctrl+g")
	window.bind("<Control-Key-j>", "ReadOriginal  Ctrl+j")
	window.bind("<Control-Key-k>", "ReadOriginal  Ctrl+k")

	window.bind("<Control-Key-i>", "ReadOriginal  Ctrl+i")
	return window

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

		# Concerning Original Data File
		elif event == '-read_org-':
			main_window.hide()
			org.select_original()
			flag(main_window)
			main_window.un_hide()
		elif event == '-show_org-':
			main_window.hide()
			org.show_original()
			main_window.un_hide()
			
		# Target Data file
		elif event == '-load_data-':
			main_window.hide()
			you.load_binary()
			flag(main_window)
			main_window.un_hide()
		elif event == '-save_data-':
			main_window.hide()
			you.save_binary()
			flag(main_window)
			main_window.un_hide()
		elif event == '-show_data-':
			main_window.hide()
			you.show_yours()
			main_window.un_hide()

		# Extract Data from Original
		elif event == '-extract-':
			main_window.hide()
			# var.temp_list = sorted(list(var.moddata.keys()))
			ext.extract()
			main_window.un_hide()
		# Modify Shift Parameters
		elif event == '-tune-':
			main_window.hide()
			tune_parameters(main_window, event, values)
			main_window.un_hide()
	main_window.close()
	return

def flag(main_window):
	if var.yourdata_dic['originaldata']['originaldata_list'] !=[]:
		main_window['-orgdata-'].update('Already Selected !', text_color='red')
		main_window['-show_org-'].update(disabled=False)
		main_window['-extract-'].update(disabled=False)
	if var.binaryfile != '':
		main_window['-yourdata-'].update('Already Selected !', text_color='red')
	if var.yourdata_dic['extracteddata']['extracted_dic'] !=[]:
		main_window['-extdata-'].update('Already Extracted !', text_color='red')
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