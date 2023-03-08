#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import matplotlib.pyplot as plt

import variables as var

def extract():
	extract_datalist()
	show_extracted()
	return

#####
# Extract data
#####
def extract_datalist():
	datalist = var.originaldata['originaldata_list']
	temperature = []
	for i, line in enumerate(datalist):
		if set(var.datalabel_dic.values()).issubset(set(line)) :
			c_label = i
			count = c_label + var.skip + 1
			tmp_dic = {}
			for k, v in var.datalabel_dic.items():
				pos = datalist[c_label].index(v)
				tmp = []
				for dataline in datalist[count:]:
					if dataline[pos] not in ['', None]:
						tmp.append(float(dataline[pos]))
					else:
						break
				tmp_dic[k] = tmp
				if k == 'Temp.':
					temp = round(sum(tmp)/len(tmp), 1)
					temperature.append(temp)
			# make horizontal list
			extacted_list = []
			vertical = list(tmp_dic.values())
			for col in range(len(vertical[0])):
				extacted_list.append([vertical[i][col] for i in range(len(vertical))])
			var.extracted_h_dic[temp] = extacted_list
			var.extracted_dic[temp] = tmp_dic
	var.temp_list = sorted(temperature)
	# Finalize
	var.extracteddata['temp_list'] = var.temp_list
	var.extracteddata['extracted_h_dic'] = var.extracted_h_dic
	var.extracteddata['extracted_dic'] = var.extracted_dic
	var.yourdata_dic['extracteddata'] = var.extracteddata
	return

def show_extracted():
	fig = ''
	ext_window = make_extwindow()
	# Main Loop
	while True:
		event, values = ext_window.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		
		elif event == '-temp-':
			temperature = values['-temp-'][0]
			ext_window['-table-'].update(var.extracted_h_dic[temperature])
			ext_window['-draw-'].update(disabled=False)

		elif event == '-draw-':
			if fig != '':
				plt.close()
			
			target = [k for k, v in values.items() if k in ['-storage-', '-loss-', '-tan_d-'] and v == True]
			temp_cond = [k for k, v in values.items() if k in ['-all-', '-selected-', '-region-'] and v == True][0]
			color = [k for k, v in values.items() if k in ['-multi-', '-uni-'] and v == True][0]
			# temp_list = [temperature]
			temp_list = var.temp_list
			fig = draw_graph(target, color, temp_list)

	plt.close('all')
	ext_window.close()
	return

def make_extwindow():
	# ウィンドウのレイアウト
	cond_label = list(var.datalabel_dic.keys())
	cond_data = [[var.datalabel_dic[key] for key in list(var.datalabel_dic.keys())]]

	frame_extract = sg.Frame('Extract Conditions', 
			  					[
								[sg.Table(cond_data, 
								headings=cond_label, 
								def_col_width=14, 
								justification='center', 
								auto_size_columns=False, 
								num_rows=1)],
								[sg.Text('Skip Columns:', 
								size=(10,1)), 
								sg.Text(var.skip, size=(4,1))],
								]
							)
	col_temp = sg.Column(
							[
								[sg.Text('Temp.(°C)', size=(10, 1))],
								[sg.Listbox(var.temp_list, 
								enable_events=True, 
								key='-temp-', 
								size=(8,3))]
							],
						justification='c'
						)
	frame_table = sg.Frame('Extracted data table', 
								[[col_temp,
									sg.Table([
											[None for i in list(var.datalabel_dic.keys())]
											], 
											headings=list(var.datalabel_dic.keys()), 
											key='-table-', 
											def_col_width=12, 
											auto_size_columns=False, 
											vertical_scroll_only=False, 
											num_rows = len(var.extracted_h_dic[var.temp_list[0]])
											)
								]]
							)
	col_target = [
				[sg.Checkbox("Storage Modulus", key='-storage-')],
				[sg.Checkbox("Loss Modulus", key='-loss-')],
				[sg.Checkbox("tan_d", key='-tan_d-', default=True)]
				]
	col_temp = [
				[sg.Radio("All", group_id='temp', key='-all-', default=True)],
				[sg.Radio("Selected", group_id='temp', key='-selected-')],
				[sg.Radio("Region", group_id='temp', key='region-')]
				]
	col_colour = [
				[sg.Radio("Multi Color", group_id='col', key='-multi-', default=True)],
				[sg.Radio("Uni Color", group_id='col', key='-uni-')],
				# [sg.Radio("Region", group_id='select', key='region-', default=True)]
				]
	frame_all = sg.Frame(
					'Draw Graph', [
						[
						sg.Button('Draw Graph', key = '-draw-', size=(20,5)), 
	  					sg.Column(col_target, justification='l'),
						sg.Column(col_temp, justification='l'),
						sg.Column(col_colour, justification='l')
						]
					])
	extracted_layout=[
				[frame_extract],
				[frame_table],
				[frame_all],
				[sg.Button('Back to Prev. Window', key = '-exit-', size=(30,1))]
				]
	window = sg.Window('Check and Draw Graph for Extracted data', extracted_layout, finalize=True)
	return window

def draw_graph(target, color, temp_list):
	fig, ax1 = plt.subplots()
	labeltext = ''
	legendlist = []
	if len(target) == 1:
		for temperature in temp_list:
			if target[0] == '-storage-':
				if color == '-multi-':
					ax1.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
						var.extracted_dic[temperature]['Str. Mod.'], 
						label='T='+str(temperature))
					ax1.legend(borderaxespad=0, ncol=2)
				else:
					ax1.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
							var.extracted_dic[temperature]['Str. Mod.'], 
							c="r")
					ax1.legend(["G'"])
				if len(temp_list) >1:
					ax1.set_title('Plot of Storage Modulus for varied Temperature')
				else:
					ax1.set_title('Plot of Storage Modulus for Temperature = '+ str(temperature))
				ax1.set_ylabel('Storage Modulus')
				
			elif target[0] == '-loss-':
				if color == '-multi-':
					ax1.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
							var.extracted_dic[temperature]['Loss Mod.'], 
							label='T='+str(temperature))
					ax1.legend(borderaxespad=0, ncol=2)
				else:
					ax1.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
							var.extracted_dic[temperature]['Loss Mod.'], 
							label= 'G"', 
							c="g")
					ax1.legend(["G''"])
				if len(temp_list) >1:
					ax1.set_title('Plot of Loss Modulus for varied Temperature')
				else:
					ax1.set_title('Plot of Loss Modulus for Temperature = '+ str(temperature))
				ax1.set_ylabel('Loss Modulus')
				
			elif target[0] == '-tan_d-':
				if color == '-multi-':
					ax1.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
						var.extracted_dic[temperature]['Tan_d'], 
						label='T='+str(temperature))
					ax1.legend(borderaxespad=0, ncol=2)
				else:
					ax1.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
							var.extracted_dic[temperature]['Tan_d'], 
							label=r'Tan $\delta$', 
							c="b")
					ax1.legend([r'Tan $\delta$'])
				if len(temp_list) >1:
					ax1.set_title(r'Plot of Tan $\delta$ for varied Temperature')
				else:
					ax1.set_title(r'Plot of Tan $\delta$ for Temperature = '+ str(temperature))
				ax1.set_ylabel(r'Tan $\delta$') 
	else:
		if '-storage-' in target:
			legendlist.append("G'")
			labeltext += "G', "
		if '-loss-' in target:
			legendlist.append("G''")
			labeltext += "G''"
		if '-tan_d-' in target:
			ax2 = ax1.twinx()
			legendlist.append('Tan $\delta$')
			ax2.set_ylabel(r'Tan $\delta$')
			ax2.semilogy(base=10)

		for temperature in temp_list:
			if '-storage-' in target:
				ax1.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
						var.extracted_dic[temperature]['Str. Mod.'], 
						c="r")
			if '-loss-' in target:
				ax1.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
						var.extracted_dic[temperature]['Loss Mod.'], 
						c="g")
			if '-tan_d-' in target:
				ax2.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
						var.extracted_dic[temperature]['Tan_d'], 
						c="b")
		ax1.legend(legendlist)
		ax1.set_ylabel(labeltext)

	ax1.set_xlabel('Angular Frequency')  # x軸ラベル
	ax1.semilogx(base=10)
	ax1.semilogy(base=10)

	plt.show(block=False)
	return fig