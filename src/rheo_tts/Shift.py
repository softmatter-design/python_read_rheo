#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import pickle

import variables as var

#####
def show_tune():
	fig = ''
	# temp_list = var.yourdata_dic['extracteddata']['temp_list']
	c1 = var.wlf_param['c1']
	c2 = var.wlf_param['c2']
	t0 = var.wlf_param['t0']

	# ウィンドウのレイアウト
	col_param = [
					[sg.Text('C1:', size = (8,1)), 
                    sg.InputText(c1, key = '-input_c1-', size = (6,1))], 
					[sg.Text('C2:', size = (8,1)), 
                    sg.InputText(c2, key = '-input_c2-', size = (6,1))],
					[sg.Text('T0 (K):', size = (8,1)), 
                    sg.InputText(t0, key = '-input_t0-', size = (6,1))]
				]
	col_text = [
				[sg.Text('Default parameter are C1 = 17.44 and C2 = 51.6.', 
	            size = (42,1))],
				[sg.Text('With above parameters, T0 should be set as Tg in Kervin.', size = (42,1))]
				]
	frame_wlf = sg.Frame('Initial Guess by WLF',
						[
							[
							sg.Column(col_param, justification='c'), 
							sg.Column(col_text, justification='l')
							],
							[
							sg.Button('Guess aT with above Parameters', 
		  					key = '-wlf-', 
							size=(28,1)),
							sg.Button('Plot "aT vs. Temp."', 
		 					key = '-plot_at-', 
							size=(28,1), 
							disabled=True)
							]
						]
						)
	frame_parameters = sg.Frame('Updated Parameters',
			     				[
									[sg.Table(
										[[None for i in range(3)]], 
										headings=['Temperature (C)', 'aT', 'bT'], 
										key='-param-', 
										def_col_width=18, 
										auto_size_columns=False, 
										vertical_scroll_only=True, 
										num_rows = len(var.temp_list), 
										justification='center')
									]
								]
								)
	col_select = [
					[
					sg.Text('Select Reference Temperature'),
					sg.Listbox(var.temp_list, key='-temp-', size=(8,3)),
					sg.Button('Select and Move',
	                            key='-select-', 
				                size=(20,2), 
				                disabled=True)
					]
				]
	frame_mantune = sg.Frame('Manually Tune Parameters',
			  				[
							[sg.Column(col_select, justification='l')]
							]
							)
	
	shift_layout=[
				[frame_wlf],
				[frame_parameters],
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
		elif event == '-wlf-':
			if fig != '':
				plt.close()
			var.wlf_param['c1'] = float(values['-input_c1-'])
			var.wlf_param['c2'] = float(values['-input_c2-'])
			var.wlf_param['t0'] = float(values['-input_t0-'])
			fig = wlf_t0()
			shift_window['-plot_at-'].update(disabled=False)
			shift_window['-select-'].update(disabled=False)
			shift_window['-param-'].update(var.param_list)
		elif event == '-plot_at-':
			if fig != '':
				plt.close()
			fig = plot_at()	
		elif event == '-select-' and values['-temp-'] != []: 
			if fig != '':
				plt.close()
			shift_window.hide()
			var.ref_temp = values['-temp-'][0]
			move_man()
			shift_window.un_hide()
	plt.close('all')
	shift_window.close()
	return

def wlf_t0():
	c1 = var.wlf_param['c1']
	c2 = var.wlf_param['c2']
	t0 = var.wlf_param['t0']
	extracteddata = var.yourdata_dic['extracteddata']
	# temp_list = var.yourdata_dic['extracteddata']['temp_list']
	var.param_list = []

	fig, ax = plt.subplots()
	for temperature in var.temp_list:
		at = 10**(-1*c1*(temperature + 273.2 - t0)/(c2 + temperature + 273.2 - t0))
		var.shift_dic[temperature] = {'at': at, 'bt': var.bt}
		var.param_list.append([temperature, f"{at:.2E}", var.bt])
		mfreq = [freq*at for freq in extracteddata['extracted_dic'][temperature]['Ang. Freq.']]
		ax.plot(mfreq, extracteddata['extracted_dic'][temperature]['Tan_d'], 
	            label='T='+str(temperature))
	ax.set_xlabel('Freq.')
	ax.set_ylabel(r'Tan $\delta$')
	ax.set_title(f'Guess for all Temperature for T0={t0:}')
	ax.semilogx(base=10)
	ax.semilogy(base=10)
	ax.legend(borderaxespad=0, ncol=2)
	plt.show(block=False)
	return fig

def plot_at():
	# temp_list = var.yourdata_dic['extracteddata']['temp_list']
	t0 = var.wlf_param['t0']

	fig, ax = plt.subplots()
	at_list = [var.shift_dic[temp]['at'] for temp in var.temp_list]
	bt_list = [var.shift_dic[temp]['bt'] for temp in var.temp_list]
	ax.plot(var.temp_list, at_list, label=r'a$_{T}$')
	ax.plot(var.temp_list, bt_list, label=r'b$_{T}$')
	ax.set_xlabel('Temperature')  # x軸ラベル
	ax.set_ylabel(r'a$_{T}$')  # y軸ラベル
	ax.set_title(f'aT for T0={t0:}') # グラフタイトル
	ax.semilogy(base=10)
	ax.legend(borderaxespad=0, ncol=2)
	plt.show(block=False)
	return fig

# tune manually
def move_man():
	mod_param()
	# temp_list = var.yourdata_dic['extracteddata']['temp_list']
	lower_temp = [x for x in var.temp_list if x < var.ref_temp]
	upper_temp = [x for x in var.temp_list if x > var.ref_temp]

	frame_reftemp = sg.Frame('Modified Parameters',
							[
								[sg.Text('Reference Temperature = ' 
		                            + str(var.ref_temp), 
		  						relief=sg.RELIEF_RAISED, 
								border_width=2, 
								size = (30,1))],
								[sg.Table(
								var.param_list, 
								headings=['Temperature (C)', 'aT', 'bT'], 
								key='-param-', 
								def_col_width=18, auto_size_columns=False, 
								vertical_scroll_only=True, 
								num_rows = len(var.param_list), 
								justification='center'
								)],
							]	
			  				)
	col_upper = [
					[
					sg.Text('Upper'),
					sg.Listbox(upper_temp, key='-temp_u-', size=(8,3)),
					sg.Button('Move Upper Data', key='-upper-', size=(10,1))
					]
				]
	col_lower = [
					[
					sg.Text('Lower'),
      				sg.Listbox(lower_temp, key='-temp_l-', size=(8,3)),
					sg.Button('Move Lower Data', key='-lower-', size=(10,1))
					]
				]
	frame_target = sg.Frame('Target Temperature',
								[
									[
									sg.Column(col_upper),
	  								sg.Column(col_lower)
									]
								]
							)
	frame_move = sg.Frame('Tune shift parameter manually !!',
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
				[frame_target],
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
		elif event == '-upper-' and values['-temp_u-'] !=[]:
			target = values['-temp_u-'][0]

			plot_mod(target)
		# elif event == "-slider1-" or event == "-slider2-":
		# 	shift_window['-input1-']. Update(values['-slider1-'])
		# 	shift_window['-input2-']. Update(values['-slider2-'])
		# 	val1 = float(values['-slider1-'])*10**float(values['-slider2-'])
		# 	print(f'{val1:.2e}')
			
	move_window.close()
	return

def mod_param():
	# ref_temp = var.wlf_param['ref_temp']
	at_ref = var.shift_dic[var.ref_temp]["at"]
	mod_shift_dic = {temp:{'at': var.shift_dic[temp]["at"]/at_ref, 
			            'bt': var.shift_dic[var.ref_temp]["bt"]} for temp in var.shift_dic.keys()}
	var.shift_dic.update(mod_shift_dic)
	var.param_list = [[temp, f'{var.shift_dic[temp]["at"]:.2E}', 
		                var.shift_dic[var.ref_temp]["bt"]] for temp in var.shift_dic.keys()]
	return 

def plot_mod(target):
	extracteddata = var.yourdata_dic['extracteddata']
	# temp_list = var.yourdata_dic['extracteddata']['temp_list']
	# ref_temp = var.wlf_param['ref_temp']
	print(target)
	target_range = [x for x in var.temp_list if x <= target and x >= var.ref_temp]
	fig, ax = plt.subplots()
	for temperature in target_range:
		mfreq = [freq*var.shift_dic[temperature]['at'] 
	                for freq in extracteddata['extracted_dic'][temperature]['Ang. Freq.']]
		if temperature == var.ref_temp:
			ax.plot(mfreq, extracteddata['extracted_dic'][temperature]['Tan_d'], 
	        label='Tr='+str(temperature), lw=3, color='red', ls=':')
		else:
			ax.plot(mfreq, extracteddata['extracted_dic'][temperature]['Tan_d'], 
	        label='T='+str(temperature))
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

