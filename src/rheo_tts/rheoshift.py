#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import csv
import numpy as np
import variables as var
import matplotlib.pyplot as plt
import pickle
#####
def main():
	# Main Window
	main_window = make_mainwindow()
	# Main Loop
	while True:
		event, values = main_window.read()
		### Main Window Procedure
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		#
		elif event == '-select_org-':
			var.csvfile = sg.popup_get_file('get file', file_types=(("CSV Files", ".csv"),))
			with open(var.csvfile, encoding='utf8') as f:
				var.csvlist = list(csv.reader(f))
			main_window['-orgdata-'].update(var.csvfile)
			main_window['-show_org-'].update(disabled=False)
		elif event == '-show_org-' and var.csvfile != '':
			main_window.hide()
			show_orgdata()
			main_window.un_hide()
			if var.binaryfile != '':
				main_window['-exdata-'].update(var.binaryfile)
				main_window['-show_ext-'].update(disabled=False)
		#
		elif event == '-load-':
			var.binaryfile = sg.popup_get_file('get file', file_types=(("Binary Data File", ".pcl"),))
			if var.binaryfile:
				with open(var.binaryfile, mode='rb') as f:
					var.moddata = pickle.load(f)
				main_window['-exdata-'].update(var.binaryfile)
				main_window['-show_ext-'].update(disabled=False)
				main_window['-tune-'].update(disabled=False)
		elif event == '-show_ext-':
			var.temp_list = sorted(list(var.moddata.keys()))
			show_extracted()
		#
		elif event == '-tune-':
			if var.binaryfile:
				with open(var.binaryfile, mode='rb') as f:
					var.moddata = pickle.load(f)
			var.temp_list = sorted(list(var.moddata.keys()))
			main_window.hide()
			show_tune()
			main_window.un_hide()
	main_window.close()

	return

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
							sg.Button('Show Data', key='-show_org-', disabled=True)]
							]
						)
	
	frame_extracted = sg.Frame('Extracted Data File',[
							[#sg.Text('Extracted File:', size = (12,1)), 
							sg.Text('not extracted yet', key = '-exdata-', relief=sg.RELIEF_RAISED, border_width=2, size = (60,1))],
							[sg.Button('Load Data File', key='-load-'),
							sg.Button('Show Extracted', key='-show_ext-', disabled=True)]
							]
						)

	frame_shift = sg.Frame('Tune Shift Parameters',[
							[sg.Text('not made yet', key = '-shiftdata-', relief=sg.RELIEF_RAISED, border_width=2, size = (60,1))],
							[sg.Button('Tune parameters', key='-tune-', disabled=True)]
							]
						)

	main_layout = [
					[frame_fileselect],
					[frame_extracted],
					[frame_shift],
					[sg.Button('Exit', key = '-exit-')]
				]
	return sg.Window('Main Window', main_layout)



#####
# Show Original Data 
#####
def show_orgdata():
	ncolm_list = [str(x) for x in range(len(var.csvlist[0]))]
	cond_label = list(var.datalabel_dic.keys())
	cond_data = [[var.datalabel_dic[key] for key in list(var.datalabel_dic.keys())]]

	frame_table = sg.Frame(
		'Selected Data Table', [
			[sg.Text('Selected Data File:'), sg.Text(var.csvfile)],
			[sg.Table(var.csvlist, headings=ncolm_list, display_row_numbers=True, def_col_width=6, auto_size_columns=False, vertical_scroll_only=False, num_rows=20)]
		]
	)
	frame_extract = sg.Frame(
		'Extract Data', [
			[sg.Table(cond_data, headings=cond_label, def_col_width=16, justification='center', auto_size_columns=False, num_rows=1)],
			[sg.Text('Skip Columns:', size=(10,1)), sg.Text(var.skip, size=(4,1))],
			[sg.Button("Extract", key='-extract-')]
		]
	)
	layout_orgtable = [
			[frame_table],
			[frame_extract],
			[sg.Button('Exit', key = '-exit-')]
	]
	orgdata_window = sg.Window('Selected Data', layout_orgtable, finalize=True, size=(800,600), resizable=True)

	while True:
		event, values = orgdata_window.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == '-extract-':
			extract_csv()
			show_extracted()
			break
	orgdata_window.close()
	return

#####
# Extract data
#####
def extract_csv():
	for i, line in enumerate(var.csvlist):
		if set(var.datalabel_dic.values()).issubset(set(line)) :
			c_label = i
			count = c_label + var.skip + 1
			tmp_dic = {}
			for k, v in var.datalabel_dic.items():
				pos = var.csvlist[c_label].index(v)
				tmp = []
				for dataline in var.csvlist[count:]:
					if dataline[pos] != '':
						tmp.append(float(dataline[pos]))
					else:
						break
				tmp_dic[k] = tmp
				if k == 'Temp.':
					temp = round(sum(tmp)/len(tmp), 1)
					var.temp_list.append(temp)
			
			horizontal = []
			vertical = list(tmp_dic.values())
			for col in range(len(vertical[0])):
				horizontal.append([vertical[i][col] for i in range(np.array(vertical).shape[0])])
			var.moddata[temp] = [horizontal, tmp_dic]

def show_extracted():
	fig = ''
	# ウィンドウのレイアウト
	frame_exfile = sg.Frame(
		'Extracted data file', [
									[sg.Text('Extracted File:', size = (12,1)), 
     								sg.Text('not extracted yet', key = '-exdata-', relief=sg.RELIEF_RAISED, border_width=2, size = (66,1))],
								    [sg.Button('Save Data', key = '-save-', size=(10,2))]
								]
							)
	frame_table = sg.Frame(
		'Extracted data table', [
									[
									sg.Column(
										[
										[sg.Listbox(var.temp_list, key='-temp-', size=(8,3))],
										[sg.Button('Select',key='-select-', size=(8,2))]
										]),
									sg.Table(
										[[None for i in list(var.datalabel_dic.keys())]], headings=list(var.datalabel_dic.keys()), key='-table-', def_col_width=12, auto_size_columns=False, vertical_scroll_only=False, num_rows = len(var.moddata[var.temp_list[0]][0]))
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
					'Draw Graph', [ 
						[
						sg.Button('Draw Selected Graph', key = '-draw-', disabled=True, size=(20,5)), 
						sg.Column(col_sel, justification='l')
						]
					])
	extracted_layout=[
				[frame_exfile],
				[frame_table],
				[frame_all, frame_sel],
				[sg.Button('Exit', key = '-exit-', size=(10,2))]
				]
	ex_window = sg.Window('Check and Draw Graph for Extracted data', extracted_layout, finalize=True)

	if var.binaryfile:
		ex_window['-exdata-'].update(var.binaryfile)

	while True:
		event, values = ex_window.read()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == '-select-':
			if values['-temp-'] != []:
				temperature = values['-temp-'][0]
				ex_window['-table-'].update(var.moddata[temperature][0])
				#
				ex_window['-save-'].update(disabled=False)
				ex_window['-draw-'].update(disabled=False)
			else:
				sg.popup_error('Proper Temperature is not selected')
		elif event == '-save-':
			var.binaryfile = sg.popup_get_file('save', save_as=True, file_types=(("Binary Data File", ".pcl"),))
			save_binary()
			ex_window['-exdata-'].update(var.binaryfile)
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
			draw_siglegraph(target, temperature)
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
			draw_allgraphs(target)

	ex_window.close()

def save_binary():
	with open(var.binaryfile, mode='wb') as f:
		pickle.dump(var.moddata, f)
	return

def draw_siglegraph(target, temperature):
	if target == 'tand':
		fig, ax = plt.subplots()
		ax.plot(var.moddata[temperature][1]['Ang. Freq.'], var.moddata[temperature][1]['Tan_d'], label=r'Tan $\delta$', c="r")
		ax.set_ylabel(r'Tan $\delta$')  # y軸ラベル
		ax.set_xlabel('Freq.')  # x軸ラベル
		ax.set_title('Measured Raw Data for T=' + str(temperature)) # グラフタイトル
		ax.semilogx(base=10)
		ax.semilogy(base=10)
		ax.legend(borderaxespad=0)
	elif target == 'both':
		fig, ax = plt.subplots()
		ax.plot(var.moddata[temperature][1]['Ang. Freq.'], var.moddata[temperature][1]['Str. Mod.'], label="G'", c="r")
		ax.plot(var.moddata[temperature][1]['Ang. Freq.'], var.moddata[temperature][1]['Loss Mod.'], label= 'G"', c="g")
		ax.set_ylabel('Storage and Loss Moduli')  # y軸ラベル
		ax.set_xlabel('Freq.')  # x軸ラベル
		ax.set_title('Measured Raw Data for T=' + str(temperature)) # グラフタイトル
		ax.semilogx(base=10)
		ax.semilogy(base=10)
		ax.legend(borderaxespad=0)
	elif target == 'all':
		fig, ax1 = plt.subplots()
		ax2 = ax1.twinx()
		ax1.plot(var.moddata[temperature][1]['Ang. Freq.'], var.moddata[temperature][1]['Str. Mod.'], label="G'", c="r")
		ax1.plot(var.moddata[temperature][1]['Ang. Freq.'], var.moddata[temperature][1]['Loss Mod.'], label= 'G"', c="g")
		ax2.plot(var.moddata[temperature][1]['Ang. Freq.'], var.moddata[temperature][1]['Tan_d'], label=r'Tan $\delta$', c="b")
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
	return

def draw_allgraphs(target):
	fig, ax = plt.subplots()

	for temp in var.temp_list:
		ax.plot(var.moddata[temp][1]['Ang. Freq.'], var.moddata[temp][1][target], label='T='+str(temp))
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
	return

#####
#
#####
def show_tune():
	# ウィンドウのレイアウト
	frame_wlf = sg.Frame('Move to 1st guess by WLF',
		      			[
						[sg.Button('Move to WLF',key='-wlf-', size=(20,2))]
						]
						)
	col_select = [
					[sg.Text('Select reference Temperature')],
					[sg.Listbox(var.temp_list, key='-temp-', size=(8,3)),
					sg.Button('Select and Move',key='-select-', size=(20,2), disabled=True)
					]
				]
	frame_mantune = sg.Frame('select',
			  				[
							[sg.Column(col_select, justification='l')]
							]
							)
	
	shift_layout=[
				[frame_wlf],
				[frame_mantune],
				[sg.Button('Exit', key = '-exit-', size=(8,1))]
				]
	shift_window = sg.Window('Tune the shift parameters', shift_layout, finalize=True)

	while True:
		event, values = shift_window()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == "-wlf-":
			shift_window['-select-'].update(disabled=False)
			shift_window.hide()
			sub_wlf_window()
			shift_window.un_hide()
		elif event == '-select-':
			shift_window.hide()
			var.ref_temp = values['-temp-'][0]
			move_man()
			shift_window.un_hide()
	shift_window.close()
	return




# sub
def sub_wlf_window():
	col_param = [
					[sg.Text('C1:', size = (4,1)), sg.InputText(var.c1, key = '-input_c1-', size = (6,1))], 
					[sg.Text('C2:', size = (4,1)), sg.InputText(var.c2, key = '-input_c2-', size = (6,1))],
					[sg.Text('T0:', size = (4,1)), sg.InputText(var.tg, key = '-input_tg-', size = (6,1))]
				]
	col_text = [
				[sg.Text('Default parameter are C1 = 17.44 and C2 = 51.6.', size = (42,1))],
				[sg.Text('With above parameters, T0 should be set as Tg in Kervin.', size = (42,1))]
				]
	wlf_layout = [
				[sg.Column(col_param, justification='l'), sg.Column(col_text, justification='l')],
				[sg.Button('Set Parameters', key = '-wlf-', size=(16,2)),
				sg.Button('Plot "aT vs. Temp."', key = '-plot_at-', size=(16,2), disabled=True),
				sg.Button('Exit', key = '-exit-', size=(16,2))
				],
				[sg.Table(
					[[None for i in range(3)]], headings=['Temperature', 'aT', 'bT'], key='-param-', def_col_width=16, auto_size_columns=False, vertical_scroll_only=True, num_rows = 20, justification='center')
				]
				]
	wlf_window = sg.Window('1st guess by WLF', wlf_layout, finalize=True)
	
	while True:
		event, values = wlf_window()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == '-wlf-':
			var.c1 = float(values['-input_c1-'])
			var.c2 = float(values['-input_c2-'])
			var.tg = float(values['-input_tg-'])
			wlf_tg()
			wlf_window['-plot_at-'].update(disabled=False)
			wlf_window['-param-'].update(var.param_list)
		elif event == '-plot_at-':
			plot_at()	
	plt.close('all')		
	wlf_window.close()
	return

def wlf_tg():
	bt=1.0
	var.param_list = []
	fig, ax = plt.subplots()
	for temp in var.temp_list:
		at = 10**(-1*var.c1*(temp + 273.2 - var.tg)/(var.c2 + temp +273.2 - var.tg))
		var.shift_dic[temp] = {'at': at, 'bt': bt}
		var.param_list.append([temp, f"{at:.2E}", bt])
		mfreq = [freq*at for freq in var.moddata[temp][1]['Ang. Freq.']]
		ax.plot(mfreq, var.moddata[temp][1]['Tan_d'], label='T='+str(temp))
	ax.set_xlabel('Freq.')  # x軸ラベル
	ax.set_ylabel(r'Tan $\delta$')  # y軸ラベル
	ax.set_title(f'Guess for all Temperature for Tg={var.tg:}') # グラフタイトル
	ax.semilogx(base=10)
	ax.semilogy(base=10)
	ax.legend(borderaxespad=0, ncol=2)
	plt.show(block=False)
	return

def plot_at():
	fig, ax = plt.subplots()
	at_list = [var.shift_dic[temp]['at'] for temp in var.temp_list]
	bt_list = [var.shift_dic[temp]['bt'] for temp in var.temp_list]
	ax.plot(var.temp_list, at_list, label=r'a$_{T}$')
	ax.plot(var.temp_list, bt_list, label=r'b$_{T}$')
	ax.set_xlabel('Temperature')  # x軸ラベル
	ax.set_ylabel(r'a$_{T}$')  # y軸ラベル
	ax.set_title(f'aT for Tg={var.tg:}') # グラフタイトル
	ax.semilogy(base=10)
	ax.legend(borderaxespad=0, ncol=2)
	plt.show(block=False)
	return

# tune manually
def move_man():
	mod_param()
	frame_reftemp = sg.Frame('Modified Parameters',
							[
								[sg.Text('Reference Temperature = ' + str(var.ref_temp), 
		  						relief=sg.RELIEF_RAISED, 
								border_width=2, 
								size = (30,1))],
								[sg.Table(
								var.param_list, 
								headings=['Temperature', 'aT', 'bT'], 
								key='-param-', 
								def_col_width=16, auto_size_columns=False, 
								vertical_scroll_only=True, 
								num_rows = 20, 
								justification='center'
								)],
							]	
			  				)
	frame_move = sg.Frame('Tune shift parameter manually!',
			     			[
							[sg.Text("Fine", size=(5,1)),
							sg.Slider(range=(1.0,9.99),
									default_value = 1.0,
									resolution=0.01,
									orientation='h',
									size=(50, 4),
									enable_events=True,
									key='-slider1-')],
							[sg.Text("Rough", size=(5,1)),
								sg.Slider(range=(-50,50),
									default_value =0,
									resolution=1,
									orientation='h',
									size=(50, 6),
									enable_events=True,
									key='-slider2-')],
							[ sg.InputText(1.0, size=(5,1), key='-input1-'), 
							sg.Text("E", size=(1,1)),
							sg.InputText(0.0, size=(6,1), key='-input2-')]
							]
							)
	move_layout=[
				[frame_reftemp],
				[frame_move],
				[sg.Button('plot', key = '-plot-', size=(8,1))],
				[sg.Button('Exit', key = '-exit-', size=(8,1))]
				]
	move_window = sg.Window('Tune the shift parameters', move_layout, finalize=True)

	while True:
		event, values = move_window()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == '-plot-':
			plot_mod()
	
		# elif event == "-slider1-" or event == "-slider2-":
		# 	shift_window['-input1-']. Update(values['-slider1-'])
		# 	shift_window['-input2-']. Update(values['-slider2-'])
		# 	val1 = float(values['-slider1-'])*10**float(values['-slider2-'])
		# 	print(f'{val1:.2e}')
			
	move_window.close()
	return

def mod_param():
	at_ref = var.shift_dic[var.ref_temp]["at"]
	mod_shift_dic = {temp:{'at': var.shift_dic[temp]["at"]/at_ref, 'bt': var.shift_dic[var.ref_temp]["bt"]} for temp in var.shift_dic.keys()}
	var.shift_dic.update(mod_shift_dic)
	var.param_list = [[temp, f'{var.shift_dic[temp]["at"]:.2E}', var.shift_dic[var.ref_temp]["bt"]] for temp in var.shift_dic.keys()]
	return

def plot_mod():
	fig, ax = plt.subplots()
	for temp in var.temp_list:
		mfreq = [freq*var.shift_dic[temp]['at'] for freq in var.moddata[temp][1]['Ang. Freq.']]
		if temp == var.ref_temp:
			ax.plot(mfreq, var.moddata[temp][1]['Tan_d'], label='Tr='+str(temp), lw=3, color='red', ls=':')
		else:
			ax.plot(mfreq, var.moddata[temp][1]['Tan_d'], label='T='+str(temp))
	ax.set_xlabel('Freq.')  # x軸ラベル
	ax.set_ylabel(r'Tan $\delta$')  # y軸ラベル
	ax.set_title(f'Modified based on Tr={var.ref_temp:}') # グラフタイトル
	ax.semilogx(base=10)
	ax.semilogy(base=10)
	ax.legend(borderaxespad=0, ncol=2)
	plt.show(block=False)
	return

def show_mod_table():

	return




if __name__ == '__main__':
	main()