#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import pickle

import variables as var

#####
def show_tune():
	temp_list = var.yourdata_dic['extracteddata']['temp_list']

	# ウィンドウのレイアウト
	frame_wlf = sg.Frame('Move to 1st guess by WLF',
		      			[
						[sg.Button('Move to WLF',key='-wlf-', size=(20,2))]
						]
						)
	col_select = [
					[sg.Text('Select reference Temperature')],
					[sg.Listbox(temp_list, key='-temp-', size=(8,3)),
					sg.Button('Select and Move',
	                            key='-select-', 
				                size=(20,2), 
				                disabled=True)
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
	shift_window = sg.Window('Tune the shift parameters', 
			                shift_layout, 
			                finalize=True)

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
	c1 = var.wlf_param['c1']
	c2 = var.wlf_param['c2']
	tg = var.wlf_param['tg']
	bt = var.wlf_param['bt']
	col_param = [
					[sg.Text('C1:', size = (4,1)), 
                    sg.InputText(c1, key = '-input_c1-', size = (6,1))], 
					[sg.Text('C2:', size = (4,1)), 
                    sg.InputText(c2, key = '-input_c2-', size = (6,1))],
					[sg.Text('T0:', size = (4,1)), 
                    sg.InputText(tg, key = '-input_tg-', size = (6,1))]
				]
	col_text = [
				[sg.Text('Default parameter are C1 = 17.44 and C2 = 51.6.', 
	            size = (42,1))],
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
			var.wlf_param['c1'] = float(values['-input_c1-'])
			var.wlf_param['c2'] = float(values['-input_c2-'])
			var.wlf_param['tg'] = float(values['-input_tg-'])
			wlf_tg()
			wlf_window['-plot_at-'].update(disabled=False)
			wlf_window['-param-'].update(var.param_list)
		elif event == '-plot_at-':
			plot_at()	
	plt.close('all')		
	wlf_window.close()
	return

def wlf_tg():
	c1 = var.wlf_param['c1']
	c2 = var.wlf_param['c2']
	tg = var.wlf_param['tg']
	bt = var.wlf_param['bt']
	extracteddata = var.yourdata_dic['extracteddata']
	temp_list = var.yourdata_dic['extracteddata']['temp_list']
	fig, ax = plt.subplots()
	for temperature in temp_list:
		at = 10**(-1*c1*(temperature + 273.2 - tg)/(c2 + temperature + 273.2 - tg))
		var.shift_dic[temperature] = {'at': at, 'bt': bt}
		var.param_list.append([temperature, f"{at:.2E}", bt])
		mfreq = [freq*at for freq in extracteddata['extracted_dic'][temperature]['Ang. Freq.']]
		ax.plot(mfreq, extracteddata['extracted_dic'][temperature]['Tan_d'], 
	            label='T='+str(temperature))
	ax.set_xlabel('Freq.')
	ax.set_ylabel(r'Tan $\delta$')
	ax.set_title(f'Guess for all Temperature for Tg={tg:}')
	ax.semilogx(base=10)
	ax.semilogy(base=10)
	ax.legend(borderaxespad=0, ncol=2)
	plt.show(block=False)
	return

def plot_at():
	tg = var.wlf_param['tg']
	temp_list = var.yourdata_dic['extracteddata']['temp_list']
	
	fig, ax = plt.subplots()
	at_list = [var.shift_dic[temp]['at'] for temp in temp_list]
	bt_list = [var.shift_dic[temp]['bt'] for temp in temp_list]
	ax.plot(temp_list, at_list, label=r'a$_{T}$')
	ax.plot(temp_list, bt_list, label=r'b$_{T}$')
	ax.set_xlabel('Temperature')  # x軸ラベル
	ax.set_ylabel(r'a$_{T}$')  # y軸ラベル
	ax.set_title(f'aT for Tg={tg:}') # グラフタイトル
	ax.semilogy(base=10)
	ax.legend(borderaxespad=0, ncol=2)
	plt.show(block=False)
	return

# tune manually
def move_man():
	mod_param()
	ref_temp = var.wlf_param['ref_temp']
	
	frame_reftemp = sg.Frame('Modified Parameters',
							[
								[sg.Text('Reference Temperature = ' 
		                            + str(ref_temp), 
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
	ref_temp = var.wlf_param['ref_temp']
	at_ref = var.shift_dic[ref_temp]["at"]
	mod_shift_dic = {temp:{'at': var.shift_dic[temp]["at"]/at_ref, 
			            'bt': var.shift_dic[ref_temp]["bt"]} for temp in var.shift_dic.keys()}
	var.shift_dic.update(mod_shift_dic)
	var.param_list = [[temp, f'{var.shift_dic[temp]["at"]:.2E}', 
		                var.shift_dic[ref_temp]["bt"]] for temp in var.shift_dic.keys()]
	return

def plot_mod():
	extracteddata = var.yourdata_dic['extracteddata']
	temp_list = var.yourdata_dic['extracteddata']['temp_list']
	ref_temp = var.wlf_param['ref_temp']
	fig, ax = plt.subplots()
	for temperature in temp_list:
		mfreq = [freq*var.shift_dic[temperature]['at'] 
	                for freq in extracteddata['extracted_dic'][temperature]['Ang. Freq.']]
		if temperature == ref_temp:
			ax.plot(mfreq, extracteddata['extracted_dic'][temperature]['Tan_d'], 
	        label='Tr='+str(temperature), lw=3, color='red', ls=':')
		else:
			ax.plot(mfreq, extracteddata['extracted_dic'][temperature]['Tan_d'], 
	        label='T='+str(temperature))
	ax.set_xlabel('Freq.')  # x軸ラベル
	ax.set_ylabel(r'Tan $\delta$')  # y軸ラベル
	ax.set_title(f'Modified based on Tr={ref_temp:}') # グラフタイトル
	ax.semilogx(base=10)
	ax.semilogy(base=10)
	ax.legend(borderaxespad=0, ncol=2)
	plt.show(block=False)
	return

def show_mod_table():

	return

