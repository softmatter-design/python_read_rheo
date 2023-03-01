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
import Shift as sft
import variables as var

############################################################################
# Main Window
############################################################################
def mainwindow():
	# dpi conditioning
	make_dpi_aware()
	# Main Window
	main_window = make_mainwindow()
	# Main Loop
	while True:
		event, values = main_window.read()
		### Main Window Procedure
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		
		# Target Data file
		elif event in ['-load_data-', '-save_data-', '-show_data-']:
			main_window.hide()
			you.select_yours(event)
			flag(main_window)
			main_window.un_hide()

		# Concerning Original Data File
		elif event == '-show_org-':
			main_window.hide()
			org.show_original()
			flag(main_window)
			main_window.un_hide()
			
		# Extract Data from Original
		elif event == '-extract-':
			main_window.hide()
			ext.extract()
			flag(main_window)
			main_window.un_hide()

		# Modify Shift Parameters
		elif event == '-tune-':
			main_window.hide()
			sft.show_tune()
			main_window.un_hide()

	main_window.close()
	return

def make_dpi_aware():
  import ctypes
  import platform
  if int(platform.release()) >= 8:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)

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
	frame_savedatafile = sg.Frame('Your Data File',
			       				[
									[
									# sg.Text('Your Data File:', size=(16,1), justification='c'),
									sg.Text('not saved yet.', 
									key = '-yourdata-', 
									relief=sg.RELIEF_RAISED, 
									border_width=2, 
									size = (30,1),
									justification='c')
									],
									[sg.Button('Load Data', 
									key='-load_data-', 
									size=(30,1))],
									[sg.Button('Save Data', 
									key='-save_data-', 
									size=(30,1))],
									[sg.Button('Show Data', 
									key='-show_data-', 
									size=(30,1))
									],
								],
							# border_width = 0
							)
	frame_fileselect = sg.Frame('Original Data File',
								[
									[
									# sg.Text('Original File:', size=(16,1), justification='c'),
									sg.Text('not selected yet.', 
									key = '-orgdata-', 
									relief=sg.RELIEF_RAISED, 
									border_width=2, 
									size = (30,1),
									justification='c')
									],
									[sg.Button('Select & Show Original', 
									key='-show_org-', 
									# disabled=True, 
									size=(30,1)),
									]
								],
							# border_width = 0
						)
	frame_extracted = sg.Frame('Extract Data',[
							[
							# sg.Text('Extracted Data:', size=(16,1), justification='c'),
							sg.Text('not extracted yet.', 
							key = '-extdata-', 
							relief=sg.RELIEF_RAISED, 
							border_width=2, 
							size = (30,1),
							justification='c')],
							[sg.Button('Extract from Original Data', 
		 					key='-extract-', 
							disabled=True, 
							size=(30,1))]
							]
						)
	frame_shift = sg.Frame('Tune Shift Parameters',[
							[
							# sg.Text('Parameters:', size=(16,1), justification='c'),
							sg.Text('not made yet.', 
							key = '-shiftdata-', 
							relief=sg.RELIEF_RAISED, 
							border_width=2, 
							size = (30,1), 
							justification='c')],
							[sg.Button('Tune Parameters', 
		  					key='-tune-', 
							disabled=True, 
							size=(30,1)
							)]
							]
						)
	layout_frame1 = [[frame_savedatafile],
						[sg.Button('Exit', 
						key = '-exit-',
						size=(30,1), 
						pad=((10,10), (20,10)))]
		  			]
	layout_frame2= [
						[frame_fileselect],
						[frame_extracted],
						[frame_shift]
					]
	# Main Window
	main_layout = [
					# [sg.MenuBar(menu_def)],
					[sg.Frame('Your Data', layout_frame1, size=(280, 280)),
						sg.Frame('Modify Your Data', layout_frame2, size=(280, 280), 
						title_location=sg.TITLE_LOCATION_TOP)
					]
					]
	#
	window = sg.Window('Main Window', main_layout, finalize=True)

	window.bind("<Control-Key-c>", "ReadOriginal  Ctrl+c")
	window.bind("<Control-Key-g>", "ReadOriginal  Ctrl+g")
	window.bind("<Control-Key-i>", "ReadOriginal  Ctrl+i")
	window.bind("<Control-Key-j>", "ReadOriginal  Ctrl+j")
	window.bind("<Control-Key-k>", "ReadOriginal  Ctrl+k")
	window.bind("<Control-Key-l>", "ReadOriginal  Ctrl+l")
	window.bind("<Control-Key-o>", "ReadOriginal  Ctrl+o")
	window.bind("<Control-Key-s>", "ReadOriginal  Ctrl+s")
	window.bind("<Control-Key-t>", "ReadOriginal  Ctrl+t")
	window.bind("<Control-Key-w>", "ReadOriginal  Ctrl+w")
	window.bind("<Control-Key-x>", "ReadOriginal  Ctrl+x")
	window.bind("<Control-Key-y>", "ReadOriginal  Ctrl+y")
	window.bind("<Control-Key-z>", "ReadOriginal  Ctrl+z")

	return window

def flag(main_window):
	if var.originaldata['originaldata_list'] != []:
		main_window['-orgdata-'].update('Already Selected !', text_color='red')
		main_window['-show_org-'].update(disabled=False)
		main_window['-extract-'].update(disabled=False)
	if var.binaryfile != '':
		main_window['-yourdata-'].update('Already Selected !', text_color='red')
	if var.extracteddata['temp_list'] != []:
		main_window['-extdata-'].update('Already Extracted !', text_color='red')
		main_window['-tune-'].update(disabled=False)
	return

############################################################################
# End of Main Window
############################################################################








if __name__ == '__main__':
	mainwindow()


