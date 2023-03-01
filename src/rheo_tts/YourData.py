#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import os
import pickle

import ShowOriginal as org
import Extract as ext
import variables as var


def select_yours(event):
	if event == '-load_data-':
		load_binary()
	elif event == '-save_data-':
		save_binary()
	elif event == '-show_data-':
		show_yourdata()
	return

def load_binary():
	var.binaryfile = sg.popup_get_file('Load', 
				    file_types=(("Binary Data File", ".pcl"),), 
                    size=(60,10))
	if var.binaryfile:
		var.fileroot = os.path.splitext(var.binaryfile)[0]
		with open(var.binaryfile, mode='rb') as f:
			var.yourdata_dic = pickle.load(f)
		var.originaldata = var.yourdata_dic['originaldata']
		var.extracteddata = var.yourdata_dic['extracteddata']
		var.shiftdata = var.yourdata_dic['shiftdata']
	return

def save_binary():
	var.binaryfile = sg.popup_get_file('Save', 
				    save_as=True, 
				    file_types=(("Binary Data File", ".pcl"),), 
                    size=(60,10))
	if var.binaryfile:
		var.fileroot = os.path.splitext(var.binaryfile)[0]
		with open(var.binaryfile, mode='wb') as f:
			pickle.dump(var.yourdata_dic, f)
	return

# Show Your Data 
def show_yourdata():
	yours_window = make_yourwindow()
	if var.originaldata['targetfile'] != '':
		yours_window['-show_org-'].Update(disabled=False)
	if var.extracteddata['temp_list'] != []:
		yours_window['-show_ext-'].Update(disabled=False)
	if var.shiftdata['shift_list'] != []:
		yours_window['-show_param-'].Update(disabled=False)
	
	while True:
		event, values = yours_window.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == '-show_org-':
			org.show_original()
		elif event == '-show_ext-':
			ext.show_extracted()
		elif event == '-show_param-':
			pass
	yours_window.close()
	return

def make_yourwindow():
	frame_original = sg.Frame(
		'Original Data', [
			[sg.Text('Original Data:', 
			size = (16,1)), 
    		sg.Text('', 
			size = (60,1))],
			[sg.Button('Show_Original', 
	     	key = '-show_org-', 
		    disabled=True,
			size = (16,1))]
				]
			)
	frame_extracted = sg.Frame(
		'Extracted Data', [
			[sg.Text('Extracted Data:', 
			size = (16,1)), 
    		sg.Text('', 
			size = (60,1))],
			[sg.Button('Show_Extracted', 
	     	key = '-show_ext-', 
		    disabled=True, 
			size = (16,1))]
				]
			)
	frame_parameters = sg.Frame(
		'Shift Parameters', [
			[sg.Text('Shift Parameters:', 
			size = (16,1)), 
    		sg.Text('', 
			size = (60,1))],
			[sg.Button('Show_Parameters', 
	     	key = '-show_param-', 
		    disabled=True, 
			size = (16,1))]
				]
			)
	layout_yours = [
			[frame_original],
			[frame_extracted],
			[frame_parameters],
			[
			sg.Button('Back to MAIN', 
	     	key = '-exit-', 
			size = (16,1))]
	]
	window = sg.Window('Your Data', layout_yours, finalize=True, resizable=True)
	return window

