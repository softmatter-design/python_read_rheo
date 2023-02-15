#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import openpyxl
import csv
import os
import pickle
import variables as var

# Your Data
def load_binary(main_window):
	var.binaryfile = sg.popup_get_file('Load', 
				    file_types=(("Binary Data File", ".pcl"),), 
                    size=(60,10))
	if var.binaryfile:
		with open(var.binaryfile, mode='rb') as f:
			var.yourdata_dic = pickle.load(f)
		main_window['-yourdata-'].update('Already Selected !', text_color='red')
	return

def save_binary(main_window):
	var.binaryfile = sg.popup_get_file('Save', 
				    save_as=True, 
				    file_types=(("Binary Data File", ".pcl"),), 
                    size=(60,10))
	with open(var.binaryfile, mode='wb') as f:
		pickle.dump(var.yourdata_dic, f)
	main_window['-yourdata-'].update('Already Selected !', text_color='red')
	return