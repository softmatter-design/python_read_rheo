#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import pickle

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
		######
		# https://note.com/nssystems/n/n737db19ee190
		#######
		elif event == '-draw-':
			if fig != '':
				plt.close()
			
			target = ''
			if values['-both-'] == True:
				target = 'both'
			if values['-all-'] == True:
				target = 'all'
			if values['-tan_d_s-'] == True:
				target = 'tand'
			fig = draw_siglegraph(target, temperature)


		elif event == '-draw_all-':
			if fig != '':
				plt.close()
			target = ''
			if values['-storage_a-'] == True:
				target = 'Str. Mod.'
			if values['-loss_a-'] == True:
				target = 'Loss Mod.'
			if values['-tan_d_a-'] == True:
				target = 'Tan_d'
			fig = draw_allgraphs(target)
	plt.close('all')
	ext_window.close()
	return

def make_extwindow():
	# ウィンドウのレイアウト
	cond_label = list(var.datalabel_dic.keys())
	cond_data = [[var.datalabel_dic[key] for key in list(var.datalabel_dic.keys())]]

	frame_extract = sg.Frame(
		'Extract Conditions', [
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
								[
									[
									col_temp,
									sg.Table(
												[
													[None for i in list(var.datalabel_dic.keys())]
												], 
												headings=list(var.datalabel_dic.keys()), 
												key='-table-', 
												def_col_width=12, 
												auto_size_columns=False, 
												vertical_scroll_only=False, 
												num_rows = len(var.extracted_h_dic[var.temp_list[0]])
											)
									]
								]
							)
	col_all = [
				[sg.Radio("Storage Modulus", group_id='all', key='-storage_a-')],
				[sg.Radio("Loss Modulus", group_id='all', key='-loss_a-')],
				[sg.Radio("tan_d", group_id='all', key='-tan_d_a-', default=True)]
				]
	col_sel = [
				[sg.Radio("Both Moduli", group_id='select', key='-both-')],
				[sg.Radio("All", group_id='select', key='-all-')],
				[sg.Radio("tan_d", group_id='select', key='-tan_d_s-', default=True)]
				]
	frame_all = sg.Frame(
					'Draw Graph', [
						[
						sg.Button('Draw All Graph', key = '-draw_all-', size=(20,5)), 
	  					sg.Column(col_all, justification='l')
						]
					])
	frame_sel = sg.Frame(
					'Draw Graph for Selected Temp.', [ 
						[
						sg.Button('Draw Selected Graph', key = '-draw-', disabled=True, size=(20,5)), 
						sg.Column(col_sel, justification='l')
						]
					])
	extracted_layout=[
				[frame_extract],
				[frame_table],
				[frame_all, frame_sel],
				[sg.Button('Back to MAIN', key = '-exit-', size=(20,1))]
				]
	window = sg.Window('Check and Draw Graph for Extracted data', extracted_layout, finalize=True)
	return window







def draw_siglegraph(target, temperature):
	if target == 'tand':
		fig, ax = plt.subplots()
		ax.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
	  			var.extracted_dic[temperature]['Tan_d'], 
				label=r'Tan $\delta$', 
				c="r")
		ax.set_ylabel(r'Tan $\delta$')  # y軸ラベル
		ax.set_xlabel('Freq.')  # x軸ラベル
		ax.set_title('Measured Raw Data for T=' + str(temperature)) # グラフタイトル
		ax.semilogx(base=10)
		ax.semilogy(base=10)
		ax.legend(borderaxespad=0)
	elif target == 'both':
		fig, ax = plt.subplots()
		ax.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
	  			var.extracted_dic[temperature]['Str. Mod.'], 
				label="G'", 
				c="r")
		ax.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
	  			var.extracted_dic[temperature]['Loss Mod.'], 
				label= 'G"', 
				c="g")
		ax.set_ylabel('Storage and Loss Moduli')  # y軸ラベル
		ax.set_xlabel('Freq.')  # x軸ラベル
		ax.set_title('Measured Raw Data for T=' + str(temperature)) # グラフタイトル
		ax.semilogx(base=10)
		ax.semilogy(base=10)
		ax.legend(borderaxespad=0)
	elif target == 'all':
		fig, ax1 = plt.subplots()
		ax2 = ax1.twinx()
		ax1.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
	   			var.extracted_dic[temperature]['Str. Mod.'], 
				label="G'", c="r")
		ax1.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
	   			var.extracted_dic[temperature]['Loss Mod.'], 
				label= 'G"', c="g")
		ax2.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
	   			var.extracted_dic[temperature]['Tan_d'], 
				label=r'Tan $\delta$', c="b")
		ax1.set_ylabel('Storage and Loss Moduli')  # y軸ラベル
		ax2.set_ylabel(r'Tan $\delta$')  # y軸ラベル
		ax1.set_xlabel('Freq.')  # x軸ラベル
		ax1.set_title('Measured Raw Data for T=' + str(temperature)) # グラフタイトル
		ax1.semilogx(base=10)
		ax1.semilogy(base=10)
		ax2.semilogy(base=10)
		h1, l1 = ax1.get_legend_handles_labels()
		h2, l2 = ax2.get_legend_handles_labels()
		ax1.legend(h1 + h2, l1 + l2, borderaxespad=0)

	plt.show(block=False)
	return fig

def draw_allgraphs(target):
	fig, ax = plt.subplots()
	for temperature in var.temp_list:
		ax.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
				var.extracted_dic[temperature][target], 
				label='T='+str(temperature))
	ax.set_xlabel('Freq.')  # x軸ラベル
	if target == 'Tan_d':
		ax.set_ylabel(r'Tan $\delta$')  # y軸ラベル
	elif target == 'Str. Mod.':
		ax.set_ylabel('Storage Modulus')  # y軸ラベル
	elif target == 'Loss Mod.':
		ax.set_ylabel('Loss Modulus')  # y軸ラベル
	ax.set_title('Measured Raw Data for all Temperature') # グラフタイトル
	ax.semilogx(base=10)
	ax.semilogy(base=10)
	ax.legend(borderaxespad=0, ncol=2)

	plt.show(block=False)
	return fig




def draw_graph(target, temp_list):
	fig, ax1 = plt.subplots()
	for temperature in temp_list:
		if target == 'tand':
			ax1.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
					var.extracted_dic[temperature]['Tan_d'], 
					label=r'Tan $\delta$', 
					c="r")
			ax1.set_ylabel(r'Tan $\delta$')  # y軸ラベル
			ax1.legend(borderaxespad=0)
		elif target == 'both':
			ax1.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
					var.extracted_dic[temperature]['Str. Mod.'], 
					label="G'", 
					c="r")
			ax1.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
					var.extracted_dic[temperature]['Loss Mod.'], 
					label= 'G"', 
					c="g")
			ax1.set_ylabel('Storage and Loss Moduli')  # y軸ラベル
			ax1.legend(borderaxespad=0)
		elif target == 'all':
			ax2 = ax1.twinx()
			ax1.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
					var.extracted_dic[temperature]['Str. Mod.'], 
					label="G'", c="r")
			ax1.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
					var.extracted_dic[temperature]['Loss Mod.'], 
					label= 'G"', c="g")
			ax2.plot(var.extracted_dic[temperature]['Ang. Freq.'], 
					var.extracted_dic[temperature]['Tan_d'], 
					label=r'Tan $\delta$', c="b")
			ax1.set_ylabel('Storage and Loss Moduli')  # y軸ラベル
			ax2.set_ylabel(r'Tan $\delta$')  # y軸ラベル
			ax2.semilogy(base=10)
			h1, l1 = ax1.get_legend_handles_labels()
			h2, l2 = ax2.get_legend_handles_labels()
			ax1.legend(h1 + h2, l1 + l2, borderaxespad=0)

		ax1.set_xlabel('Freq.')  # x軸ラベル
		ax1.set_title('Measured Raw Data for T=' + str(temperature)) # グラフタイトル
		ax1.semilogx(base=10)
		ax1.semilogy(base=10)

	plt.show(block=False)
	return fig